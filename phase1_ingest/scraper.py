import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime

# List of target URLs provided by the user
FUND_URLS = [
    "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
    "https://groww.in/mutual-funds/tata-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/motilal-oswal-large-and-midcap-fund-direct-growth",
    "https://groww.in/mutual-funds/sbi-elss-tax-saver-fund-direct-growth",
    "https://groww.in/mutual-funds/kotak-multicap-fund-direct-growth",
    "https://groww.in/mutual-funds/icici-prudential-retirement-fund-pure-equity-plan-direct-growth",
    "https://groww.in/mutual-funds/bajaj-finserv-nifty-50-index-fund-direct-growth"
]

async def scrape_fund_data(url, browser):
    page = await browser.new_page()
    print(f"Scraping: {url}...")
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Extract Fund Name
        fund_name = soup.find('h1').text.strip() if soup.find('h1') else "N/A"

        # Initialize data dictionary
        data = {
            "fund_name": fund_name,
            "url": url,
            "nav": "N/A",
            "expense_ratio": "N/A",
            "exit_load": "N/A",
            "min_sip": "N/A",
            "risk": "N/A",
            "one_year_return": "N/A",
            "lock_in": "None",
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }

        # NAV Extraction (usually in a large font or specific div)
        nav_span = soup.find('span', string=lambda t: t and 'NAV' in t)
        if nav_span:
            # Look for the preceding or succeeding sibling that contains numbers
            parent = nav_span.parent
            data['nav'] = parent.text.replace('NAV', '').strip()

        # Extract stats from tables or key-value grids
        rows = soup.find_all('tr')
        for row in rows:
            text = row.text.lower()
            if 'expense ratio' in text:
                data['expense_ratio'] = row.find_all('td')[-1].text.strip()
            elif 'exit load' in text:
                data['exit_load'] = row.find_all('td')[-1].text.strip()
            elif 'min. sip' in text or 'minimum sip' in text:
                data['min_sip'] = row.find_all('td')[-1].text.strip()

        # Risk extraction (usually in a specific riskometer component)
        risk_div = soup.find('div', string=lambda t: t and 'risk' in t.lower())
        if risk_div:
            # Often near a text like 'Very High'
            data['risk'] = risk_div.text.strip()

        # 1-Year Return
        return_div = soup.find('div', string=lambda t: t and '1Y' in t)
        if return_div:
            data['one_year_return'] = return_div.parent.find_all('div')[-1].text.strip()

        # ELSS lock-in
        if "elss" in fund_name.lower():
            data['lock_in'] = "3 Years"
        elif "retirement" in fund_name.lower():
            data['lock_in'] = "5 Years (or age 60)"

        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        await page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [scrape_fund_data(url, browser) for url in FUND_URLS]
        results = await asyncio.gather(*tasks)
        await browser.close()

        # Filter out failed results
        final_data = [r for r in results if r]

        # Save to JSON
        output_path = os.path.join(os.path.dirname(__file__), "sample_fund_data.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2)
        
        print(f"Successfully scraped {len(final_data)} funds. Data saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())

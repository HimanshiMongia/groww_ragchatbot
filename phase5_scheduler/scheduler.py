import schedule
import time
import subprocess
import os
import sys
from datetime import datetime

# Paths to relevant scripts
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SCRAPER_SCRIPT = os.path.join(BASE_DIR, "phase1_ingest", "scraper.py")
VECTOR_STORE_SCRIPT = os.path.join(BASE_DIR, "phase2_retrieve", "vector_store.py")

def run_update():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting Scheduled Update...")
    
    try:
        # 1. Run Scraper
        print("Step 1: Running Scraper...")
        subprocess.run([sys.executable, SCRAPER_SCRIPT], check=True)
        print("Scraper completed successfully.")
        
        # 2. Run Vector Store Update
        print("Step 2: Updating Vector Store...")
        subprocess.run([sys.executable, VECTOR_STORE_SCRIPT], check=True)
        print("Vector Store updated successfully.")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Full Update Completed Successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"Update failed during step execution: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Schedule the update every day at 00:00 (Local Time)
schedule.every().day.at("00:00").do(run_update)

# Also schedule a shorter interval for testing/demonstration (e.g., every 6 hours)
schedule.every(6).hours.do(run_update)

if __name__ == "__main__":
    print("Groww Chatbot Scheduler started.")
    print("Scheduled to run data refresh daily at 00:00 and every 6 hours.")
    
    # Run once immediately on startup to ensure data is fresh
    run_update()
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute

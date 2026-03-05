import os
import sys

# Add the project root and all phase directories to the path so internal imports work
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, 'phase3_generate'))
sys.path.append(os.path.join(base_dir, 'phase4_chat_app'))

from phase4_chat_app.main import app

# Vercel looks for the 'app' or 'handler' variable
handler = app

import os
import sys

# Add the project root to sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

# Import the app using absolute project path
try:
    from phase4_chat_app.main import app
    handler = app
except Exception as e:
    print(f"CRITICAL ERROR during app initialization: {e}")
    raise e

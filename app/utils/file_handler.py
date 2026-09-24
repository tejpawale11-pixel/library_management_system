from pathlib import Path 
from datetime import datetime

LOG_FILE = Path("logs/admin_activate.txt")
def log_admin_activity(action: str):
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok = True)
        with open(LOG_FILE,"a",encoding="utf-8") as file: # a = append mode
            timestamp = datetime.now().strftime("%Y-%M-%D %H:%M-%S")
            file.write(f"{timestamp}-{action}\n")
    except PermissionError:
        print("Permission denied while writing activity log.")
    except OSError as e:
        print(f"File handling error: {e}")
        

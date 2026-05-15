import json
from datetime import datetime
import os


LOG_FILE = "audit_logs.json"


def log_event(event_type, details):

    log_entry = {
        "timestamp": str(datetime.now()),
        "event_type": event_type,
        "details": details
    }

    # -----------------------------
    # CREATE FILE IF NOT EXISTS
    # -----------------------------
    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # -----------------------------
    # LOAD EXISTING LOGS
    # -----------------------------
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    # -----------------------------
    # APPEND NEW LOG
    # -----------------------------
    logs.append(log_entry)

    # -----------------------------
    # SAVE UPDATED LOGS
    # -----------------------------
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
import os
from datetime import datetime
from flask import request

class ServerLogger:
    def __init__(self, log_filename: str = "server_activity.txt"):
        self.log_filename = log_filename
        # Create log file with a header if it doesn't exist yet
        if not os.path.exists(self.log_filename):
            with open(self.log_filename, "w", encoding="utf-8") as f:
                f.write(f"--- Server Log Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

    def log_response(self, response):
        """Flask after_request callback to log connection details."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = request.remote_addr or "Unknown IP"
        method = request.method
        route = request.path
        status_code = response.status_code

        log_entry = (
            f"[{timestamp}] "
            f"IP: {client_ip} | "
            f"Method: {method} | "
            f"Route: {route} | "
            f"Result/Status: {status_code}\n"
        )

        try:
            with open(self.log_filename, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[Logger Error] Could not write to log file: {e}")

        return response
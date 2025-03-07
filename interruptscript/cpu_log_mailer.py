#!/usr/bin/env python3
import os
import time
import logging
import smtplib
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Log File from Your Existing Script
LOG_FILE = "/var/log/do_cpu_monitor.log"

# Email Configuration (Using Gmail SMTP)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "quintin.kramer@pdgcreative.com"
EMAIL_PASSWORD = "PASSWORD"  # Remove spaces!
EMAIL_RECEIVER = "quintin.kramer@pdgcreative.com"
SEND_TIME = "23:59"  # Daily send time (24-hour format)

# Prevent Multiple Instances (PID File)
PID_FILE = "/var/run/cpu_log_mailer.pid"

# Configure Logging
logging.basicConfig(filename="/var/log/cpu_log_mailer.log", level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

def check_existing_process():
    """Prevent multiple script instances."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
        if pid and os.path.exists("/proc/" + pid):  # Check if process exists
            logging.error("Script already running with PID %s. Exiting.", pid)
            sys.exit(1)
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

def get_last_100_logs():
    """Reads the last 100 log entries from the CPU monitor log file."""
    if not os.path.exists(LOG_FILE):
        logging.error("Log file not found: %s", LOG_FILE)
        return "No log file found."

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()[-100:]  # Get last 100 lines

    return "".join(logs) if logs else "No logs available."

def send_log_email():
    """Sends the last 100 logs via email."""
    log_content = get_last_100_logs()

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Daily CPU Monitor Log Report"

    msg.attach(MIMEText("Here are the last 100 logs from your CPU monitor script:\n\n{}".format(log_content), "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        logging.info("Daily log email sent successfully.")
    except Exception as e:
        logging.error("Failed to send daily email: %s", e)
if __name__ == "__main__":
    last_email_date = None

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time == SEND_TIME and (last_email_date is None or last_email_date != now.date()):
            send_log_email()
            last_email_date = now.date()

        time.sleep(60)  # Check every 60 seconds if it's time to send the email



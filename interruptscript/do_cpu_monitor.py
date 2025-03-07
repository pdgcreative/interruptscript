#!/usr/bin/env python3
import os
import requests
import subprocess
import time
import logging
from datetime import datetime, timedelta

logging.basicConfig(filename='/var/log/do_cpu_monitor.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

API_TOKEN =  "TOKEN"
DROPLET_ID = "ID"
THRESHOLD = 99.5
BASE_URL = "URL"

def get_cpu_usage():
    now = datetime.utcnow()
    end_time = now.isoformat() + "Z"
    start_time = (now - timedelta(minutes=5)).isoformat() + "Z"
    params = {"host_id": DROPLET_ID, "start": start_time, "end": end_time, "aggregation": "avg"}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("data", {}).get("result", [])
        if results:
            values = results[0].get("values", [])
            if values:
                return float(values[-1][1])
    except Exception as e:
        logging.error("Error retrieving CPU usage: %s", e)
    return None

def restart_mysql():
    try:
        subprocess.check_call(['systemctl', 'restart', 'mysql'])
        logging.info("MySQL restarted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to restart MySQL: %s", e)

def main():
    cpu_usage = get_cpu_usage()
    if cpu_usage is not None:
        logging.info("Current CPU usage: %.2f%%", cpu_usage)
        if cpu_usage > THRESHOLD:
            logging.info("CPU usage (%.2f%%) above threshold (%.2f%%). Restarting MySQL...", cpu_usage, THRESHOLD)
            restart_mysql()
    else:
        logging.error("Could not retrieve CPU usage.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)

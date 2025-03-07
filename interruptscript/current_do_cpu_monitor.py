#!/usr/bin/env python3
import subprocess
import time
import logging
import re

# Configure logging
logging.basicConfig(
    filename='/var/log/do_cpu_monitor.log', 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s:%(message)s'
)

# CPU usage threshold
THRESHOLD = 95

def get_cpu_usage():
    """
    Get the current CPU usage percentage using /proc/stat.
    """
    try:
        with open("/proc/stat", "r") as f:
            first_line = f.readline()
        fields = [float(column) for column in first_line.split()[1:]]  # Ignore 'cpu' prefix

        total_time = sum(fields)
        idle_time = fields[3]  # Idle time is the 4th column

        time.sleep(1)  # Wait 1 second for accurate calculation

        with open("/proc/stat", "r") as f:
            second_line = f.readline()
        fields2 = [float(column) for column in second_line.split()[1:]]

        total_time2 = sum(fields2)
        idle_time2 = fields2[3]

        total_delta = total_time2 - total_time
        idle_delta = idle_time2 - idle_time

        cpu_usage = 100 * (1 - (idle_delta / total_delta))
        return cpu_usage

    except Exception as e:
        logging.error("Error retrieving CPU usage from /proc/stat: {}".format(e))
        return None


def restart_mysql():
    """
    Restart the MySQL service using systemctl.
    """
    try:
        subprocess.check_call(['systemctl', 'restart', 'mysql'])
        logging.info("MySQL restarted successfully due to high CPU usage.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to restart MySQL: {}".format(e))

def main():
    """
    Monitor CPU usage and restart MySQL if the threshold is exceeded.
    """
    while True:
        cpu_usage = get_cpu_usage()
        if cpu_usage is not None:
            logging.info("Current CPU usage: {:.2f}%".format(cpu_usage))
            logging.getLogger().handlers[0].flush()  # Force log update
            
            if cpu_usage > THRESHOLD:
                logging.warning("CPU usage ({:.2f}%) exceeded threshold ({:.2f}%). Restarting MySQL...".format(cpu_usage, THRESHOLD))
                logging.getLogger().handlers[0].flush()
                restart_mysql()
        else:
            logging.error("Could not retrieve CPU usage.")
            logging.getLogger().handlers[0].flush()

        time.sleep(300)  # Wait 5 minutes before checking again

if __name__ == "__main__":
    main()

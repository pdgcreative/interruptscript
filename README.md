Highland CPU Monitoring Script  - Command reference guide.

This document provides a reference for managing the do_cpu_monitor.py script, which monitors CPU usage and restarts MySQL if CPU usage exceeds 95% threshold.

Start the Script in the Background
nohup /usr/bin/python3 /usr/local/bin/do_cpu_monitor.py > /var/log/do_cpu_monitor.log 2>&1 &

Check if the Script is Running
ps aux | grep do_cpu_monitor.py

Stop the Script
pkill -f do_cpu_monitor.py

Monitor Logs
tail -f /var/log/do_cpu_monitor.log

View the Last 100 Log Entries
tail -n 100 /var/log/do_cpu_monitor.log

If changes are made to the current script save them in the the file then 
Stop the script (pkill -f do_cpu_monitor.py) make sure it isn’t running 
(ps aux | grep do_cpu_monitor.py) then with the script stopped, run the new script so it will run in the background (nohup /usr/bin/python3 /usr/local/bin/do_cpu_monitor.py > /var/log/do_cpu_monitor.log 2>&1 &)

Script Location
192.241.202.247>usr>local>bin>do_cpu_monitor.py

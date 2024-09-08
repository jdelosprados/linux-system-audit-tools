# Captures the state of the Linux system including system information, running processes, 
# network connections, socket statistics, loaded kernel modules, scheduled tasks, 
# login history, and users and groups.

#!/bin/bash

# Define the output file
OUTPUT_FILE="/root/system_capture_$(date +%Y%m%d_%H%M%S).txt"

# Start capturing data
echo "System Capture Started: $(date)" > "${OUTPUT_FILE}"
echo "========================================" >> "${OUTPUT_FILE}"

# System information
echo "System Information:" >> "${OUTPUT_FILE}"
uname -a >> "${OUTPUT_FILE}"
lsb_release -a >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Running processes
echo "Running Processes:" >> "${OUTPUT_FILE}"
ps auxf >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Network connections and socket statistics
echo "Network Connections:" >> "${OUTPUT_FILE}"
netstat -tulnp >> "${OUTPUT_FILE}"
echo "Socket Statistics:" >> "${OUTPUT_FILE}"
ss -tulnp >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Loaded kernel modules
echo "Loaded Kernel Modules:" >> "${OUTPUT_FILE}"
lsmod >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Scheduled tasks
echo "Scheduled Tasks (User's Crontab):" >> "${OUTPUT_FILE}"
crontab -l >> "${OUTPUT_FILE}"
echo "Scheduled Tasks (/etc/crontab):" >> "${OUTPUT_FILE}"
cat /etc/crontab >> "${OUTPUT_FILE}"
echo "Scheduled Jobs in cron directories:" >> "${OUTPUT_FILE}"
ls -al /etc/cron.* >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Login history
echo "Login History:" >> "${OUTPUT_FILE}"
last >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Users and groups
echo "Users (/etc/passwd):" >> "${OUTPUT_FILE}"
cat /etc/passwd >> "${OUTPUT_FILE}"
echo "Groups (/etc/group):" >> "${OUTPUT_FILE}"
cat /etc/group >> "${OUTPUT_FILE}"
echo "----------------------------------------" >> "${OUTPUT_FILE}"

# Conclude capture
echo "System Capture Completed: $(date)" >> "${OUTPUT_FILE}"

echo "All system capture data has been saved to ${OUTPUT_FILE}"
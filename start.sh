echo "Starting tracking process..."
screen -S tracking -d -m ./venv/bin/python tracking.py
screen -d tracking
echo "Tracking process started."
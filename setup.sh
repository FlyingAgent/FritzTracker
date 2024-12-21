# Starting message
echo "Starting setup process..."

# VENV for the requirements to work
python3 -m venv venv

# Requirements for the project
venv/bin/pip install -r requirements.txt

# Finish message
echo "Setup process completed!"
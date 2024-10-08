# Define variables
USER=$(shell whoami)
GROUP=$(shell groups | cut -d' ' -f1)
WORKING_DIR=$(shell pwd)
PYTHON_EXEC=$(WORKING_DIR)/.venv/bin/python
SCRIPT_PATH=$(WORKING_DIR)/run.py
TEMP_SERVICE_FILE=/tmp/jobee.service
SERVICE_FILE=/etc/systemd/system/jobee.service

.PHONY: all setup venv install-deps generate-service clean

# Run all steps: setup and generate-service
all: setup generate-service

# Setup virtual environment
setup: venv install-deps

# Create virtual environment
venv:
	python3 -m venv .venv

# Install dependencies
install-deps:
	.venv/bin/pip install -r requirements.txt

# Generate systemd service file and save it to /tmp
generate-service:
	@echo "Generating systemd service file..."
	@echo "USER=$(USER)"
	@echo "GROUP=$(GROUP)"
	@echo "WORKING_DIR=$(WORKING_DIR)"
	@echo "PYTHON_EXEC=$(PYTHON_EXEC)"
	@echo "SCRIPT_PATH=$(SCRIPT_PATH)"
	sed -e "s|{{USER}}|$(USER)|g" \
	    -e "s|{{GROUP}}|$(GROUP)|g" \
	    -e "s|{{WORKING_DIR}}|$(WORKING_DIR)|g" \
	    -e "s|{{PYTHON_EXEC}}|$(PYTHON_EXEC)|g" \
	    -e "s|{{SCRIPT_PATH}}|$(SCRIPT_PATH)|g" \
	    lib/systemd/jobee.service.template > $(TEMP_SERVICE_FILE)
	@echo "Service file generated at $(TEMP_SERVICE_FILE)"

install-service:
	@echo "Installing and starting systemd service..."
	@if [ "$$(id -u)" -ne 0 ]; then \
	    echo "You must run this command as root."; \
	    exit 1; \
	fi
	cp $(TEMP_SERVICE_FILE) $(SERVICE_FILE)
	systemctl daemon-reload
	systemctl enable jobee.service
	systemctl start jobee.service
	@echo "Service installed and started successfully."


# Clean virtual environment
clean:
	rm -rf .venv
	rm -f $(TEMP_SERVICE_FILE)

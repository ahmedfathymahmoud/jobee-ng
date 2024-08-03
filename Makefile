# Makefile

.PHONY: all install-service install-venv clean

# Default target
all: install-venv install-service

# Create and activate virtual environment, install dependencies
install-venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

# Install systemd service
install-service:
	@echo "Installing systemd service..."
	USER=$(shell whoami)
	GROUP=$(shell id -g -n $(USER))
	WORKING_DIR=$(shell pwd)
	PYTHON_EXEC=$(WORKING_DIR)/.venv/bin/python
	SCRIPT_PATH=$(WORKING_DIR)/run.py
	sed -e "s/\$(USER)/$(USER)/g" \
	    -e "s/\$(GROUP)/$(GROUP)/g" \
	    -e "s/\$(WORKING_DIR)/$(WORKING_DIR)/g" \
	    -e "s/\$(PYTHON_EXEC)/$(PYTHON_EXEC)/g" \
	    -e "s/\$(SCRIPT_PATH)/$(SCRIPT_PATH)/g" \
	    jobbot.service.template | sudo tee /etc/systemd/system/jobbot.service > /dev/null
	sudo systemctl daemon-reload
	sudo systemctl enable jobbot.service
	sudo systemctl start jobbot.service

# Clean up virtual environment and service files
clean:
	@echo "Cleaning up..."
	rm -rf venv
	sudo rm /etc/systemd/system/jobbot.service
	sudo systemctl daemon-reload
	sudo systemctl stop jobbot.service

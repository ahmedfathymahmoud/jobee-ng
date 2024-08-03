# Define variables
USER=$(shell whoami)
GROUP=$(shell groups | cut -d' ' -f1)
WORKING_DIR=$(shell pwd)
PYTHON_EXEC=$(WORKING_DIR)/.venv/bin/python
SCRIPT_PATH=$(WORKING_DIR)/run.py
SERVICE_FILE=/etc/systemd/system/jobee.service

.PHONY: setup venv install-deps install-service clean

all: setup install-service


# Setup virtual environment
setup: venv install-deps

# Create virtual environment
venv:
	python3 -m venv .venv

# Install dependencies
install-deps:
	.venv/bin/pip install -r requirements.txt

# Check if running as root
define SUDO_IF_NOT_ROOT
if [ "$$(id -u)" -ne 0 ]; then \
    echo "Not running as root. Using sudo for $$1"; \
    sudo $$1; \
else \
    $$1; \
fi
endef

# Install systemd service
install-service:
	@echo "Installing systemd service..."
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
	    lib/systemd/jobee.service.template > jobee.service
	$(call SUDO_IF_NOT_ROOT, cp jobee.service $(SERVICE_FILE))
	$(call SUDO_IF_NOT_ROOT, systemctl daemon-reload)
	$(call SUDO_IF_NOT_ROOT, systemctl enable jobee.service)
	$(call SUDO_IF_NOT_ROOT, systemctl start jobee.service)

# Clean virtual environment
clean:
	rm -rf .venv

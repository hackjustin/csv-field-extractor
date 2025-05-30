.PHONY: install test clean lint setup

# Setup virtual environment and install dependencies
setup:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

# Install package in development mode
install:
	.venv/bin/pip install -e .

# Run tests
test:
	.venv/bin/python -m unittest test_csv_field_extractor.py -v

# Clean up generated files
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Lint code (install flake8 if not present)
lint:
	@if [ ! -f .venv/bin/flake8 ]; then \
		echo "Installing flake8..."; \
		.venv/bin/pip install flake8; \
	fi
	.venv/bin/flake8 csv_field_extractor.py test_csv_field_extractor.py

# Build package for distribution
build:
	.venv/bin/python setup.py sdist bdist_wheel

# Show help
help:
	@echo "Available commands:"
	@echo "  setup    - Create virtual environment and install dependencies"
	@echo "  install  - Install package in development mode"
	@echo "  test     - Run unit tests"
	@echo "  clean    - Remove generated files"
	@echo "  lint     - Check code style"
	@echo "  build    - Build package for distribution"
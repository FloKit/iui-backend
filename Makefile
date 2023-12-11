dependencies: 
	@echo "Installing dependencies..."
	poetry install

env: dependencies
	@echo "Activating virtual environment..."
	poetry shell
# Applying different Python linters with custom settings.

path := .

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: isort black flake ## Apply all the linters

isort: ## Apply isort
	@echo "Applying isort..."
	@echo "================="
	@echo

	@isort --atomic \
	--profile black \
	--color \
	--trailing-comma \
	--gitignore \
	--force-alphabetical-sort-within-sections \
	--ensure-newline-before-comments \
	--order-by-type \
	--honor-noqa \
	--remove-redundant-aliases \
	$(path)


black: ## Apply black
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@black $(path)


flake: ## Apply flake8
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 --count \
	--extend-exclude '.venv, .pytest_cache, ./*/migrations' \
	--max-complexity=12 \
	--ignore='E501, E402, W391, ' \
	--show-source \
	--statistics \
	$(path)


trim_imports: ## Remove unused imports
	@autoflake --remove-all-unused-imports \
	--ignore-init-module-imports \
	--in-place \
	--recursive \
	$(path)

.DEFAULT_GOAL := help
PKG = sffix
FIX_SCRIPT = ${PKG}/apps/fix.py
TESTS_DIR = ${PKG}/tests
TEST_FILES_DIR = ${PKG}/test_files

# NOTE: -e installs in "Development Mode"
# See: https://packaging.python.org/tutorials/installing-packages/
install: ## Install the package in development mode
	pip install -e .

# NOTE: remove the .egg-info directory
uninstall: ## Uninstall the package
	pip uninstall ${PKG}
	rm -rf ${PKG}.egg-info

# GLORIOUS hack to autogenerate Makefile help
# This simply parses the double hashtags that follow each Makefile command
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help message
	@echo "Makefile help for ${PKG}"
	@echo "======================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all python cache and build files
	find . -type f -name "*.o" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf ${PKG}.egg-info/
	rm -f ${TEST_FILES_DIR}/*_fixed_*.sf

test_script: ## Run the fix.py script on test files as a sanity check
	python ${FIX_SCRIPT} test --indir ${TEST_FILES_DIR}
	rm -f ${TEST_FILES_DIR}/*_fixed_*.sf

.PHONY: install uninstall help clean test_script
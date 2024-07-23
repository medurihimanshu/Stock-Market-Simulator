#!/bin/bash
rm -rf output/*
source .venv_wsl/bin/activate
pip install -r requirements.txt

# Run the tests
pytest assessment_app/tests/pub_tests/ --html=output/pub-test-report.html --self-contained-html
#pytest assessment_app/tests/private_tests/ --html=output/private-test-report.html --self-contained-html

# Run the coverage analysis
coverage run --source=assessment_app -m pytest

# Display the report in the terminal
coverage report --show-missing --include="*/assessment_app/*" --omit="*/__init__.py"

# Generate HTML report in the specified directory
coverage html --include="*/assessment_app/*" --omit="*/__init__.py" -d output/coverage_report
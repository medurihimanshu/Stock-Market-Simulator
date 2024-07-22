#!/bin/bash
# Run the tests
pytest /app/assessment_app/tests/pub_tests/ --html=/app/output/pub-test-report.html --self-contained-html
#pytest /app/assessment_app/tests/private_tests/ --html=/app/output/private-test-report.html --self-contained-html

# Run the coverage analysis
coverage run --source=assessment_app -m pytest

# Display the report in the terminal
coverage report --show-missing --include="*/assessment_app/*" --omit="*/__init__.py"

# Generate HTML report in the specified directory
coverage html --include="*/assessment_app/*" --omit="*/__init__.py" -d output/coverage_report
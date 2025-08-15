
#!/bin/bash
echo "Running tests with coverage..."
coverage run --source=. -m unittest discover
coverage report -m

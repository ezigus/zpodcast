#!/bin/bash

# Check if markdownlint-cli is installed
if ! command -v markdownlint &> /dev/null; then
    echo "markdownlint-cli is not installed. Please install it with:"
    echo "npm install -g markdownlint-cli"
    exit 1
fi

echo "Running markdown linting checks..."
# Only check main project markdown files, exclude node_modules and other external dirs
markdownlint --config .markdownlint.json \
  --ignore "node_modules/**/*.md" \
  --ignore "**/vendor/**/*.md" \
  --ignore "**/dist/**/*.md" \
  --ignore "**/build/**/*.md" \
  "./*.md" "./docs/**/*.md" "./zpodcast/**/*.md"

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "✅ All markdown files passed linting checks!"
else
    echo "❌ Some markdown files have linting issues. Please fix them."
fi

exit $exit_code
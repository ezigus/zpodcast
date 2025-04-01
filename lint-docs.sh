#!/bin/bash

# Run flake8 for linting
flake8 zpodcast tests

# Run black for formatting check
black --check zpodcast tests
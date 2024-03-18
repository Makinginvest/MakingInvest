#!/bin/bash

# Create backup directory if it doesn't exist
mkdir -p _project/requirements

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Get current date and time in YYYY-MM-DD-hms format
    current_datetime=$(date "+%Y-%m-%d-%H-%M-%S")
    # Backup the existing requirements.txt with the current date and time
    cp requirements.txt _project/requirements/requirements-BAK-${current_datetime}.txt
fi

# Generate requirements.txt with pigar
pigar generate

# List of packages to ensure they are in requirements.txt
packages=("pigar==2.1.1" "autoflake==2.2.1" "black==24.2.0" "uvicorn=0.27.1" "tabulate==0.9.0")

# Check if requirements.txt was successfully generated
if [ -f "requirements.txt" ]; then
    # Remove all blank lines and lines starting with # from requirements.txt
    # and output to a temporary file
    sed '/^$/d; /^#/d' requirements.txt > temp_requirements.txt

    # Replace the original requirements.txt with the temporary file
    mv temp_requirements.txt requirements.txt

    # Loop through each package in the packages array
    for package in "${packages[@]}"; do
        # Check if the package is not already in requirements.txt and add it if missing
        if ! grep -q "$package" requirements.txt; then
            echo "$package" >> requirements.txt
        fi
    done

    echo "requirements.txt has been updated."
else
    echo "Failed to generate requirements.txt."
fi

#!/bin/bash

# Check if .gitignore exists in the current directory to confirm if it's a Git repository
if [ ! -f ".gitignore" ]; then
    echo "Error: This script must be run in the root directory of a Git repository."
    exit 1
fi

# Add .DS_Store to .gitignore if not already present
if ! grep -q ".DS_Store" ".gitignore"; then
    echo ".DS_Store" >> .gitignore
    echo ".DS_Store added to .gitignore."
fi

# Initialize a flag to check if any .DS_Store files are found and removed
found_and_removed_files=0

# Find and remove any .DS_Store files from the repository or filesystem
echo "Searching for .DS_Store files in the repository..."
find . -name ".DS_Store" | while read file; do
    if git ls-files --error-unmatch "$file" > /dev/null 2>&1; then
        # File is tracked by Git, remove it from the index
        git rm --cached "$file"
        found_and_removed_files=1
    else
        # File is not tracked by Git, remove it from the filesystem
        rm "$file"
    fi
done

# Check if any .DS_Store files were found and removed
if [ $found_and_removed_files -eq 0 ]; then
    echo "No .DS_Store files found or needed to be removed. Everything is in order."
else
    # Commit the changes if any .DS_Store files were removed
    git commit -m "Remove .DS_Store files and update .gitignore"
    echo "Removed .DS_Store files and updated the repository."
fi

echo "Script execution completed."

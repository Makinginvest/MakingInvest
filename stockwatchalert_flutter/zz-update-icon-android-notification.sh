#!/bin/bash

# This script copies 'notification_icon.png' from 'assets/icon/' to 'android/app/src/res/drawable/'
# It checks if the user is in the root directory by looking for 'pubspec.yaml'

# Check if 'pubspec.yaml' exists in the current directory
if [ ! -f "pubspec.yaml" ]; then
    echo "Error: 'pubspec.yaml' not found. Please run this script from the root directory."
    exit 1
fi

# Path to the source file
SRC="assets/icon/notification_icon.png"

# Path to the destination
DEST="android/app/src/main/res/drawable/notification_icon.png"

# Check if the source file exists
if [ ! -f "$SRC" ]; then
    echo "Error: Source file '$SRC' not found."
    exit 1
fi

# Copy the file to the destination
cp -f "$SRC" "$DEST"

echo "File copied successfully."

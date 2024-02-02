#!/bin/bash

# Check if in the root directory by looking for 'pubspec.yaml'
if [ ! -f "pubspec.yaml" ]; then
    echo "Error: This script must be run from the root directory of the Flutter project."
    exit 1
fi

# Navigate to the iOS directory
cd ios || exit

# Execute the specified commands
rm -rf Pods
rm -rf .symlinks
rm -rf Flutter/Flutter.framework
rm -rf Flutter/Flutter.podspec
rm -f Runner.xcworkspace/xcshareddata/WorkspaceSettings.xcsettings
rm -rf Podfile.lock Pods Runner.xcworkspace

# Navigate back to the root directory
cd ..

# Execute Flutter clean and get commands
flutter clean
flutter pub get

# Navigate to the iOS directory again
cd ios || exit

# Execute CocoaPods related commands
rm -rf Flutter/App.framework
rm -rf Pods
pod deintegrate
pod install --repo-update
flutter pub get
pod install

echo "Script execution completed."

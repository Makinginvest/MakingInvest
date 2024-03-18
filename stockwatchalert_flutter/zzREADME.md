# app

Apple app specify fastlane password bwmr-kncm-fnym-qpek

GENERATE MODELS

flutter pub run build_runner build --delete-conflicting-outputs

flutter build apk --release
flutter build apk --debug

flutter build appbundle --target-platform android-arm,android-arm64

fastlane init
fastlane deliver setup - to upload meta

flutter build ios
fastlane spaceauth -u codememory101@gmail.com &&
flutter build ios --release && bundle exec fastlane test_flight && bundle update fastlane

# app icon

flutter packages pub run flutter_launcher_icons:main &&
flutter pub run flutter_native_splash:create

# flutter fix

dart fix --dry-run

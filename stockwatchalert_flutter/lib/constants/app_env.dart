import 'package:flutter_dotenv/flutter_dotenv.dart';

class AppENV {
  static String REVENUECAT_ANDROID_KEY = dotenv.get('REVENUECAT_ANDROID_KEY', fallback: 't');
  static String REVENUECAT_IOS_KEY = dotenv.get('REVENUECAT_IOS_KEY', fallback: 't');
}

import 'package:url_launcher/url_launcher_string.dart';

class ZLaunchUrl {
  static Future<void> launchUrl(String url, {LaunchMode mode = LaunchMode.externalApplication}) async {
    try {
      await launchUrlString(url, mode: mode);
    } catch (e) {
      print(e);
    }
  }
}

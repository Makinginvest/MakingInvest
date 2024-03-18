import 'package:hive/hive.dart';

import 'firestore_service.dart';

class HiveHelper {
  static Future<void> setApiUrl(String apiUrl) async {
    final settings = await Hive.openBox('settings');
    settings.put('apiUrl', apiUrl);
  }

  static Future<String> getApiUrl() async {
    final settings = await Hive.openBox('settings');
    String apiUrl = settings.get('apiUrl') ?? '';

    if (apiUrl == '') {
      var x = await FirestoreService.getAppControlsPublic();
      apiUrl = x.apiUrlV1;
      settings.put('apiUrl', apiUrl);
    }

    print(apiUrl);
    return apiUrl;
  }
}

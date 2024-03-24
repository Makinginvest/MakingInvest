import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:stockwatchalert/models/screener_model.dart';

class ApiScreenerService {
  static Dio _dio = Dio();

  static Future<ScreenerModel?> getStockScreen(String apiUrl, num minClose, num maxClose, num minVolume) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    try {
      log(apiUrl + '/v1/screener-stocks?jsonWebToken=${jsonWebToken}&minClose=${minClose}&maxClose=${maxClose}&minVolume=${minVolume}');
      var response = await _dio.get(apiUrl + '/v1/screener-stocks?minClose=${minClose}&maxClose=${maxClose}&minVolume=${minVolume}&jsonWebToken=${jsonWebToken}',
          options: Options(receiveTimeout: Duration(seconds: 5)));

      return ScreenerModel.fromJson(response.data);
    } catch (e) {
      log('response.data update user ${e}');
      return null;
    }
  }
}

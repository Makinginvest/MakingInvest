import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../../models/market_analysis.dart';

class ApiMarketAnalysisService {
  static Dio _dio = Dio();

  static Future<MarketAnalysis?> getMarketAnalysis(String apiUrl) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    try {
      var response = await _dio.get(apiUrl + '/signals-analysis?jsonWebToken=${jsonWebToken}', options: Options(receiveTimeout: Duration(seconds: 5)));

      return MarketAnalysis.fromJson(response.data);
    } catch (e) {
      log('response.data update user ${e}');
      return null;
    }
  }
}

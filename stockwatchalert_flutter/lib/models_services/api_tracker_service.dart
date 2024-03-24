import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../models/symbols_tracker_aggr.dart';

class ApiSymbolTrackerService {
  static Dio _dio = Dio();

  static Future<SymbolTrackerAggr?> getSymbolsTreackerAggr(String apiUrl) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    try {
      print(apiUrl + '/v1/symbols-trackers?jsonWebToken=${jsonWebToken}');
      var response = await _dio.get(apiUrl + '/v1/symbols-trackers?jsonWebToken=${jsonWebToken}', options: Options(receiveTimeout: Duration(seconds: 5)));

      return SymbolTrackerAggr.fromJson(response.data);
    } catch (e) {
      log('response.data update user ${e}');
      return null;
    }
  }
}

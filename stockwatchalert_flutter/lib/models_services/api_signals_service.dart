import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';

class ApiSignalsService {
  static Dio _dio = Dio();

  static Future<SignalAggrV1?> getClosedSignalAggrV1({required SignalAggrV1 signalAggr, required String apiUrl}) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    try {
      var response = await _dio.get(
          // apiUrl + '/v1/signals-results?jsonWebToken=${jsonWebToken}&nameCollection=${signalAggr.nameCollection}&nameId=${signalAggr.nameId}&nameVersion=${signalAggr.nameVersion}',
          apiUrl + '/v1/signals-results?jsonWebToken=${jsonWebToken}&nameCollection=${signalAggr.nameCollection}&nameId=${signalAggr.nameId}&nameVersion=${signalAggr.nameVersion}',
          options: Options(receiveTimeout: Duration(seconds: 5)));

      return SignalAggrV1.fromJson(response.data);
    } on DioException catch (e) {
      log('response.data update user ${e}');
      log('response.data update user ${e.response?.data['message']}');
      return null;
    }
  }
}

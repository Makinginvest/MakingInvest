import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../../models/signal_aggr.dart';

class ApiSignalsService {
  static Dio _dio = Dio();

  static Future<SignalAggr?> getClosedSignalAggr({required SignalAggr signalAggr, required String apiUrl}) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    try {
      var response = await _dio.get(
          apiUrl +
              '/signals-results?jsonWebToken=${jsonWebToken}&signalsCollection=${signalAggr.nameSignalsCollection}&name=${signalAggr.name}&nameVersion=${signalAggr.nameVersion}',
          options: Options(receiveTimeout: Duration(seconds: 5)));

      return SignalAggr.fromJson(response.data);
    } on DioException catch (e) {
      log('response.data update user ${e}');
      log('response.data update user ${e.response?.data['message']}');
      return null;
    }
  }

  static Future<SignalAggr?> getClosedSignalAggrBySymbol({required SignalAggr signalAggrx, required Signal signal, required String apiUrl}) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    try {
      var response = await _dio.get(
          apiUrl +
              '/signals-results/${signal.symbol}?jsonWebToken=${jsonWebToken}&signalsCollection=${signalAggrx.nameSignalsCollection}&name=${signalAggrx.name}&nameVersion=${signalAggrx.nameVersion}',
          options: Options(receiveTimeout: Duration(seconds: 5)));

      return SignalAggr.fromJson(response.data);
    } on DioException catch (e) {
      log('response.data update user ${e}');
      log('response.data update user ${e.response?.data['message']}');
      return null;
    }
  }
}

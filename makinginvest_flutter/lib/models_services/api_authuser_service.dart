import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '_hive_helper.dart';

class ApiAuthUserService {
  static Dio _dio = Dio();

  static Future<bool?> updateUser({required Map<String, dynamic> data, required String apiUrl}) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return null;

    // check if key has instance of DateTime and convert to toIso8601String()
    data.forEach((key, value) {
      if (value is DateTime) {
        data[key] = value.toIso8601String();
      }
    });

    try {
      await _dio.patch(
        apiUrl + '/users?jsonWebToken=${jsonWebToken}',
        data: {...data},
        options: Options(receiveTimeout: Duration(seconds: 5), contentType: 'application/json'),
      );

      return true;
    } on DioException catch (e) {
      log('error response.data update user ${e}');
      log('error response.data update user ${e.response?.data['message']}');
      return false;
    }
  }

  static Future<bool?> deleteAccount() async {
    try {
      User? fbUser = FirebaseAuth.instance.currentUser;
      String? jsonWebToken = await fbUser?.getIdToken();
      if (jsonWebToken == null) return null;

      String apiUrl = await HiveHelper.getApiUrl();

      await _dio.patch(
        apiUrl + '/users/userId/${fbUser?.uid}/delete-account',
        data: {'jsonWebToken': jsonWebToken},
        options: Options(receiveTimeout: Duration(seconds: 5), contentType: 'application/json'),
      );

      FirebaseAuth.instance.signOut();

      return true;
    } on DioException catch (e) {
      log('response ${e}');
      log('response ${e.response?.data['message']}');
      return false;
    }
  }

  static Future<bool?> deleteAccountFbUserJsonWebToken(User fbUser, String jsonWebToken, String apiUrl) async {
    try {
      await _dio.delete(
        apiUrl + '/users/userId/${fbUser.uid}/delete-account?jsonWebToken=$jsonWebToken',
        data: {'jsonWebToken': jsonWebToken},
        options: Options(receiveTimeout: Duration(seconds: 5), contentType: 'application/json'),
      );

      return true;
    } on DioException catch (e) {
      log('response ${e}');
      log('response ${e.response?.data['message']}');
      return false;
    }
  }
}

import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../../models/news_wordpress.dart';

class ApiNewsWordpressService {
  static Dio _dio = Dio();

  static Future<List<NewsWordpress>> getNews(String apiUrl) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? jsonWebToken = await fbUser?.getIdToken();
    if (jsonWebToken == null) return [];

    try {
      var response = await _dio.get(apiUrl + '/news-wordpress?jsonWebToken=${jsonWebToken}', options: Options(receiveTimeout: Duration(seconds: 5)));
      var data = response.data['news'] as List;
      return data.map((e) => NewsWordpress.fromJson(e)).toList();
    } catch (e) {
      log('response.data news wordpress ${e}');
      return [];
    }
  }
}

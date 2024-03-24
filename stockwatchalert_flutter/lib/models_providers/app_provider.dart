import 'dart:async';

import 'package:flutter/material.dart';
import 'package:stockwatchalert/models/auth_user.dart';
import 'package:stockwatchalert/models/post_aggr.dart';
import 'package:stockwatchalert/models/screener_model.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/models/symbols_tracker_aggr.dart';
import 'package:stockwatchalert/models/video_lesson_aggr.dart';
import 'package:stockwatchalert/models_services/api_screener_service.dart';
import 'package:stockwatchalert/models_services/firestore_service.dart';

import '../models/announcement_aggr.dart';
import '../models_services/api_tracker_service.dart';
import '../models_services/_hive_helper.dart';
import 'auth_provider.dart';

class AppProvider with ChangeNotifier {
  /* -------------------------------- NOTE INIT ------------------------------- */
  String? authUserId;
  AuthUser? authUser;

  AuthProvider? _authProvider;
  AuthProvider? get authProvider => _authProvider;
  set authProvider(AuthProvider? authProvider) {
    _authProvider = authProvider;
    bool rerun = authUserId == null || authUserId == '' || authUserId != _authProvider?.authUser?.id;

    if (_authProvider?.authUser != null && rerun) {
      streamSignalsXAggrOpenV1();
      getSymbolTrackerAggr();
      streamAnnoucementAggr();
      getStockScreener();

      notifyListeners();
      authUserId = _authProvider?.authUser?.id ?? '';
      authUser = _authProvider?.authUser;
    }

    if (_authProvider?.authUser == null) {
      cancleStreamPost();
      cancleStreamVideoLessonsAggr();
      cancleStreamAnnoucementAggr();

      notifyListeners();
      authUserId = null;
      authUser = null;
    }

    authUser = _authProvider?.authUser;
    notifyListeners();
  }

  /* -------------------------------- NOTE Cancle Streams ------------------------------- */
  void cancleAllStreams() {
    cancleStreamPost();
    cancleStreamVideoLessonsAggr();
    cancleStreamAnnoucementAggr();

    notifyListeners();
    authUserId = null;
    authUser = null;
  }

  /* -------------------------------- NOTE Post ------------------------------- */
  PostAggr _postAggr = PostAggr();
  PostAggr get postAggr => _postAggr;
  StreamSubscription<PostAggr>? _streamSubscriptionPostAggr;

  List<Post> _posts = [];
  List<Post> get posts => _posts;

  void streamPosts() {
    var res = FirestoreService.streamPostsAggr();
    _streamSubscriptionPostAggr = res.listen((event) {
      _postAggr = event;
      _posts = _postAggr.data;
      notifyListeners();
    });
  }

  void cancleStreamPost() {
    _streamSubscriptionPostAggr?.cancel();
  }

  /* -------------------------------- NOTE Video ------------------------------- */
  VideoLessonAggr _videoLessonAggr = VideoLessonAggr();
  VideoLessonAggr get videoLessonAggr => _videoLessonAggr;
  StreamSubscription<VideoLessonAggr>? _streamSubscriptionVideoLessonAggr;

  List<VideoLesson> _videoLessons = [];
  List<VideoLesson> get videoLessons => _videoLessons;

  void streamVideoLessonsAggr() {
    var res = FirestoreService.streamVideoLessonsAggr();
    _streamSubscriptionVideoLessonAggr = res.listen((event) {
      _videoLessonAggr = event;
      _videoLessons = _videoLessonAggr.data;
      notifyListeners();
    });
  }

  void cancleStreamVideoLessonsAggr() {
    _streamSubscriptionVideoLessonAggr?.cancel();
  }

  /* -------------------------------- NOTE Announcment Aggr ------------------------------- */
  AnnouncementAggr _announcementAggr = AnnouncementAggr();
  AnnouncementAggr get announcementAggr => _announcementAggr;
  StreamSubscription<AnnouncementAggr>? _streamSubscriptionAnnouncementAggr;

  void streamAnnoucementAggr() {
    var res = FirestoreService.streamAnnoucementAggr();
    _streamSubscriptionAnnouncementAggr = res.listen((event) {
      _announcementAggr = event;
      notifyListeners();
    });
  }

  void cancleStreamAnnoucementAggr() {
    _streamSubscriptionAnnouncementAggr?.cancel();
  }

  /* -------------------------- NOTE OPEN SIGNALS V1 -------------------------- */
  List<SignalAggrV1> _signalAggrsOpenV1 = [];
  List<SignalAggrV1> get signalAggrsOpenV1 => _signalAggrsOpenV1;
  StreamSubscription<List<SignalAggrV1>>? _streamSubscriptionSignalAggrsOpenV1;

  void streamSignalsXAggrOpenV1() {
    var res = FirestoreService.streamSignalsXAggrOpenV1();
    _streamSubscriptionSignalAggrsOpenV1 = res.listen((event) {
      _signalAggrsOpenV1 = event;
      notifyListeners();
    });
  }

  void cancleStreamSignalsAggrOpenV1() {
    _streamSubscriptionSignalAggrsOpenV1?.cancel();
  }

  /* ---------------------------- NOTE SYMBOLS TRACKER --------------------------- */
  SymbolTrackerAggr _symbolTrackerAggr = SymbolTrackerAggr();
  SymbolTrackerAggr get symbolTrackerAggr => _symbolTrackerAggr;

  List<SymbolTracker> _symbolTrackers = [];
  List<SymbolTracker> get symbolTrackers => _symbolTrackers;

  DateTime? _dtSymbolTrackersUpdated;

  void getSymbolTrackerAggr() async {
    DateTime? nowUtc = DateTime.now().toUtc();
    if (_dtSymbolTrackersUpdated != null && nowUtc.difference(_dtSymbolTrackersUpdated!).inMinutes < 15) return;

    String apiUrl = await HiveHelper.getApiUrl();
    var res = await ApiSymbolTrackerService.getSymbolsTreackerAggr(apiUrl);
    if (res == null) return;

    _symbolTrackerAggr = res;
    _dtSymbolTrackersUpdated = res.lastUpdatedDateTime;

    _symbolTrackers = _symbolTrackerAggr.stocks + _symbolTrackerAggr.crypto + _symbolTrackerAggr.forex;

    notifyListeners();
  }

  /* ------------------------------ NOTE SCREENER ----------------------------- */
  bool isLoadingStockScreener = false;
  ScreenerModel _stockScreener = ScreenerModel();
  ScreenerModel get stockScreener => _stockScreener;
  List<ScreenerDataModel> _stockScreenerData = [];
  List<ScreenerDataModel> _stockScreenerDataFiltered = [];
  List<ScreenerDataModel> get stockScreenerDataFiltered => _stockScreenerDataFiltered;
  List<String> filterStockRatingRecommendation = [];
  String _selectedFilterStockRatingRecommendation = 'All';
  String get selectedFilterStockRatingRecommendation => _selectedFilterStockRatingRecommendation;

  set selectedFilterStockRatingRecommendation(String value) {
    _selectedFilterStockRatingRecommendation = value;
    if (value == 'All') {
      _stockScreenerDataFiltered = _stockScreenerData;
    } else {
      _stockScreenerDataFiltered = _stockScreenerData.where((element) => element.ratingRecommendation == value).toList();
    }
    notifyListeners();
  }

  num stockScreenerMinClose = 1;
  num stockScreenerMaxClose = 10;
  num stockScreenerMinVolume = 500000;

  void getStockScreener() async {
    try {
      isLoadingStockScreener = true;
      selectedFilterStockRatingRecommendation = 'All';
      _stockScreenerDataFiltered = [];

      notifyListeners();
      String apiUrl = await HiveHelper.getApiUrl();
      var res = await ApiScreenerService.getStockScreen(apiUrl, stockScreenerMinClose, stockScreenerMaxClose, stockScreenerMinVolume);
      if (res == null) return;

      _stockScreener = res;
      _stockScreenerData = _stockScreener.data;
      _stockScreenerDataFiltered = _stockScreenerData;
      filterStockRatingRecommendation = _stockScreenerData.map((e) => e.ratingRecommendation).toSet().toList();
      // sort and put the rating that contains 'buy' lowercase first
      filterStockRatingRecommendation.sort((a, b) {
        if (a.toLowerCase().contains('buy') && !b.toLowerCase().contains('buy')) return -1;
        if (!a.toLowerCase().contains('buy') && b.toLowerCase().contains('buy')) return 1;
        return a.compareTo(b);
      });
      // add 'All' to the filter at start
      filterStockRatingRecommendation.insert(0, 'All');
      // remove ""
      filterStockRatingRecommendation.removeWhere((element) => element == '');

      isLoadingStockScreener = false;
      notifyListeners();
    } catch (e) {
      print('Error in getStockScreener: $e');
      isLoadingStockScreener = false;
      notifyListeners();
    }
  }
}

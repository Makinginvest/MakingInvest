import 'dart:async';

import 'package:flutter/material.dart';
import 'package:stockwatchalert/models/auth_user.dart';
import 'package:stockwatchalert/models/post_aggr.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/models/symbols_tracker_aggr.dart';
import 'package:stockwatchalert/models/video_lesson_aggr.dart';
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

    _symbolTrackers = _symbolTrackerAggr.crypto + _symbolTrackerAggr.forex + _symbolTrackerAggr.stocks;

    notifyListeners();
  }
}

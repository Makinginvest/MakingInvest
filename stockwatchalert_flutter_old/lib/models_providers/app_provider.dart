import 'dart:async';

import 'package:flutter/material.dart';

import '../models/announcement_aggr.dart';
import '../models/auth_user.dart';
import '../models/news_wordpress.dart';
import '../models/offering_aggr.dart';
import '../models/post_aggr.dart';
import '../models/signal_aggr.dart';
import '../models/symbols_tracker_aggr.dart';
import '../models/video_lesson_aggr.dart';
import '../models_services/_hive_helper.dart';
import '../models_services/api_news_service.dart';
import '../models_services/api_tracker_service.dart';
import '../models_services/firebase_auth_service.dart';
import '../models_services/firestore_service.dart';
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
      streamSignalsXAggrOpen();
      getSymbolTrackerAggr();
      streamAnnoucementAggr();
      streamOfferingAggr();
      getNewsWordpressInit();
      streamPosts();
      streamVideoLessonsAggr();

      notifyListeners();
      authUserId = _authProvider?.authUser?.id ?? '';
      authUser = _authProvider?.authUser;
    }

    if (_authProvider?.authUser == null) {
      cancleStreamSignalsAggrOpen();
      cancleStreamPost();
      cancleStreamVideoLessonsAggr();
      cancleStreamAnnoucementAggr();
      cancleStreamOfferingAggr();
      cancleStreamPost();
      cancleStreamVideoLessonsAggr();

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
    cancleStreamSignalsAggrOpen();

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

  toggleSignalToFavorites(Signal s) async {
    String apiUrl = await HiveHelper.getApiUrl();
    if (authUser == null || apiUrl == '') return;
    FirebaseAuthService.updateFavorite(id: s.id, user: authUser!, apiUrl: apiUrl);
  }

  /* ------------------------------ OFFETING Aggr ----------------------------- */
  OfferingAggr _offeringAggr = OfferingAggr();
  OfferingAggr get offeringAggr => _offeringAggr;
  StreamSubscription<OfferingAggr>? _streamSubscriptionOfferingAggr;

  void streamOfferingAggr() {
    var res = FirestoreService.streamOfferingAggr();
    _streamSubscriptionOfferingAggr = res.listen((event) {
      _offeringAggr = event;
      notifyListeners();
    });
  }

  void cancleStreamOfferingAggr() {
    _streamSubscriptionOfferingAggr?.cancel();
  }

  /* --------------------------------  New Wordpress------------------------------- */
  List<NewsWordpress> _newsWordpress = [];
  List<NewsWordpress> get newsWordpress => _newsWordpress;
  DateTime? _dtNewsWordpressUpdated;

  void getNewsWordpressInit() async {
    _dtNewsWordpressUpdated = DateTime.now();

    String apiUrl = await HiveHelper.getApiUrl();
    _newsWordpress = await ApiNewsWordpressService.getNews(apiUrl);
    notifyListeners();
  }

  void getNewsWordpress() async {
    if (_dtNewsWordpressUpdated == null) return;
    DateTime dtNow = DateTime.now();
    Duration diff = dtNow.difference(_dtNewsWordpressUpdated!);
    if (diff.inMinutes < 15 && _newsWordpress.isNotEmpty) return;

    String apiUrl = await HiveHelper.getApiUrl();
    _newsWordpress = await ApiNewsWordpressService.getNews(apiUrl);
    _dtNewsWordpressUpdated = DateTime.now();
    notifyListeners();
  }

/* ---------------------------- NOTE OPEN SIGNALS --------------------------- */
  String _selectedSignalAggrName = '';
  String get selectedSignalAggrName => _selectedSignalAggrName;

  set selectedSignalAggrName(String selectedSignalAggrName) {
    _selectedSignalAggrName = selectedSignalAggrName;
    notifyListeners();
  }

  List<SignalAggr> _signalAggrsOpen = [];
  List<SignalAggr> get signalAggrsOpen => _signalAggrsOpen;
  StreamSubscription<List<SignalAggr>>? _streamSubscriptionSignalAggrsOpen;

  void streamSignalsXAggrOpen() {
    var res = FirestoreService.streamSignalsXAggrOpen_v2();
    _streamSubscriptionSignalAggrsOpen = res.listen((event) {
      _signalAggrsOpen = event;
      notifyListeners();
    });
  }

  void cancleStreamSignalsAggrOpen() {
    _streamSubscriptionSignalAggrsOpen?.cancel();
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

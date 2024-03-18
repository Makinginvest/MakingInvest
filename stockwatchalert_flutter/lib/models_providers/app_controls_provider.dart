import 'dart:async';
import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart' hide AuthProvider;
import 'package:flutter/material.dart';
import 'package:package_info/package_info.dart';
import 'package:stockwatchalert/models/auth_user.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/models/symbols_tracker_aggr.dart';
import 'package:stockwatchalert/models/ws_symbol.dart';

import '../models/app_controls_public.dart';
import '../models/market_analysis.dart';
import '../models/news_aggr.dart';
import '../models_services/firestore_service.dart';
import '../models_services/_hive_helper.dart';
import 'auth_provider.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class AppControlsProvider with ChangeNotifier {
  /* -------------------------------- NOTE INIT ------------------------------- */
  DateTime? _dtWebsocketUpdated;
  String? _authUserId;
  String? _apiWebSocketUrlV1;
  String? _jsonWebToken;
  int _websocketTimerIntervalSecs = 30;
  Timer? _websocketTimer;

  AuthProvider? _authProvider;
  AuthUser? _authUser;
  AuthProvider? get authProvider => _authProvider;
  set authProvider(AuthProvider? authProvider) {
    _authProvider = authProvider;
    bool rerun = _authUserId == null || _authUserId != _authProvider?.authUser?.id;

    if (_authProvider?.authUser != null && rerun) {
      _authUserId = _authProvider?.authUser?.id ?? '';
      _authUser = _authProvider?.authUser;

      streamAppControls();
      startWebsockerTime();
      notifyListeners();
    }

    if (_authProvider?.authUser == null) {
      _authUserId = null;
      _websocketTimer?.cancel();

      disconnectSocketIo();
      cancleStreamAppControls();
      notifyListeners();
    }
  }

  /* ---------------------------- NOTE APP CONTROLS --------------------------- */
  AppControlsPublic _appControls = AppControlsPublic();
  AppControlsPublic get appControls => _appControls;
  StreamSubscription<AppControlsPublic>? _streamSubscriptionAppControls;

  void streamAppControls() {
    var res = FirestoreService.streamAppControlsPublic();
    _streamSubscriptionAppControls = res.listen((event) async {
      _appControls = event;

      await HiveHelper.setApiUrl(_appControls.apiUrlV1);

      connectSocketIo();
      notifyListeners();
    });
  }

  void cancleStreamAppControls() {
    _streamSubscriptionAppControls?.cancel();
  }

  /* --------------------- NOTE REFRESH TOKEN ON RECONNECT -------------------- */
  void validateJsonWebToken() async {
    FirebaseAuth.instance.idTokenChanges().listen((event) async {
      await FirebaseAuth.instance.currentUser?.reload();
      var newJsonWebToken = await FirebaseAuth.instance.currentUser?.getIdToken();
      if (newJsonWebToken != _jsonWebToken) {
        _jsonWebToken = newJsonWebToken;
        disconnectSocketIo();
        connectSocketIo();
      }
    });
  }

  void websocketReconnectAppResume() {
    disconnectSocketIo();
    connectSocketIo();
  }

  void startWebsockerTime() {
    _websocketTimer = Timer.periodic(Duration(seconds: _websocketTimerIntervalSecs), (timer) {
      websocketReconnect();
    });
  }

  void websocketReconnect() {
    var dtNow = DateTime.now();
    var dtWebsocketUpdated = this._dtWebsocketUpdated ?? dtNow;

    bool dtCheck = (dtWebsocketUpdated == dtNow) || dtNow.difference(dtWebsocketUpdated).inSeconds > _websocketTimerIntervalSecs;
    bool socketCheck = socket?.disconnected == true || socket == null;

    if (dtCheck && socketCheck) {
      disconnectSocketIo();
      connectSocketIo();
    }
  }

/* -------------------------------- WEBSOCKET ------------------------------- */
  IO.Socket? socket;
  void connectSocketIo() async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    String? newJsonWebToken = await FirebaseAuth.instance.currentUser?.getIdToken();
    if (fbUser == null) return;

    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    String appVersion = packageInfo.version;
    num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;

    if (appControls.apiWebSocketUrlV1 == '') {
      socket?.close();
      socket?.disconnect();
      return;
    }

    if (appControls.apiWebSocketUrlV1 == _apiWebSocketUrlV1 && socket?.connected == true && newJsonWebToken == _jsonWebToken) return;

    _apiWebSocketUrlV1 = appControls.apiWebSocketUrlV1;
    _jsonWebToken = newJsonWebToken;

    socket = IO.io(_apiWebSocketUrlV1, <String, dynamic>{
      'transports': ['websocket'],
      'path': '/socketio_v1/socket.io',
      'autoConnect': false,
      'forceNew': true,
      'extraHeaders': {
        'jsonWebToken': _jsonWebToken,
        'userId': fbUser.uid,
        'appVersion': appVersion,
        'appBuildNumber': appBuildNumber,
      }
    });

    socket?.connect();
    socket?.on('connect', (data) => print('websocket connect ${data}'));
    socket?.on('disconnect', (_) => print('websocket disconnect'));
    socket?.on('connect_error', (data) => print('websocket error ${data}'));

    socket?.on('prices_crypto', (message) {
      handlePriceData(message: message, type: 'crypto');
    });

    socket?.on('prices_forex', (message) {
      handlePriceData(message: message, type: 'forex');
      _dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('prices_stocks', (message) {
      handlePriceData(message: message, type: 'stocks');
      _dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('market_analysis', (message) {
      handleMarketAnalysis(message['data']);
      _dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('news_aggr', (message) {
      handleNewsAggr(message['data']);
      _dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('signal_aggr_open_v1', (message) {
      handleSignalsXAggrOpenV1(message['data']);
      _dtWebsocketUpdated = DateTime.now();
    });
  }

  void cancleAllStreams() {
    disconnectSocketIo();
    notifyListeners();
    _authUserId = null;
  }

  void disconnectSocketIo() {
    socket?.close();
    socket?.disconnect();
    socket = null;
  }

  /* -------------------------- NOTE OPEN SIGNALS V1 -------------------------- */
  List<SignalAggrV1> _signalAggrsOpenV1 = [];
  List<SignalAggrV1> get signalAggrsOpenV1 => _signalAggrsOpenV1;
  StreamSubscription<List<SignalAggrV1>>? _streamSubscriptionSignalAggrsOpenV1;

  void handleSignalsXAggrOpenV1(data) {
    if (data is String) data = json.decode(data);
    List<SignalAggrV1> signalAggrs = data.map<SignalAggrV1>((e) => SignalAggrV1.fromJson(e)).toList();
    bool isAdmin = _authUser?.isAdmin ?? false;
    if (!isAdmin) signalAggrs.removeWhere((e) => e.nameIsAdminOnly == true);
    _signalAggrsOpenV1 = signalAggrs;

    print('handleSignalsXAggrOpenV1 ${_signalAggrsOpenV1.length}');
    notifyListeners();
  }

  void cancleStreamSignalsAggrOpenV1() {
    _streamSubscriptionSignalAggrsOpenV1?.cancel();
  }

  /* -------------------------- NOTE MARKET ANALYSIS -------------------------- */
  MarketAnalysis _marketAnalysis = MarketAnalysis();
  MarketAnalysis get marketAnalysis => _marketAnalysis;

  void handleMarketAnalysis(data) {
    if (data is String) data = json.decode(data);
    _marketAnalysis = MarketAnalysis.fromJson(data);
    notifyListeners();
  }

  /* -------------------------------- NOTE NEWS ------------------------------- */
  NewsAggr _newsAggr = NewsAggr();
  NewsAggr get newsAggr => _newsAggr;

  List<News> _newsCrypto = [];
  List<News> get newsCrypto => _newsCrypto;

  List<News> _newsStocks = [];
  List<News> get newsStocks => _newsStocks;

  List<News> _newsForex = [];
  List<News> get newsForex => _newsForex;

  void handleNewsAggr(data) {
    if (data is String) data = json.decode(data);
    _newsAggr = NewsAggr.fromJson(data);
    _newsCrypto = _newsAggr.dataCrypto;
    _newsStocks = _newsAggr.dataStocks;
    _newsForex = _newsAggr.dataForex;

    notifyListeners();
  }

  /* -------------------------------- NOTE Symbols ws ------------------------------- */
  List<WSSymbol> wsSymbolsCrypto = [];
  List<WSSymbol> wsSymbolsForex = [];
  List<WSSymbol> wsSymbolsStocks = [];

  void handlePriceData({var message, String type = 'crypto'}) {
    var data = message['data'];
    List<WSSymbol> _wsSymbols = [];

    for (var item in data) {
      _wsSymbols.add(WSSymbol.fromJson(item));
    }
    if (_wsSymbols.length > 0) {
      if (type == 'crypto') wsSymbolsCrypto = _wsSymbols;
      if (type == 'forex') wsSymbolsForex = _wsSymbols;
      if (type == 'stocks') wsSymbolsStocks = _wsSymbols;

      notifyListeners();
    }
  }

  num getLivelPriceSignalV1(SignalV1 signal) {
    List<WSSymbol> symbols = [];
    if (signal.market.toLowerCase() == 'crypto') symbols = wsSymbolsCrypto.map((e) => e).toList();
    if (signal.market.toLowerCase() == 'forex') symbols = wsSymbolsForex.map((e) => e).toList();
    if (signal.market.toLowerCase() == 'stocks') symbols = wsSymbolsStocks.map((e) => e).toList();

    if (symbols.map((e) => e.symbol).toList().contains(signal.symbol)) {
      return symbols[symbols.map((e) => e.symbol).toList().indexOf(signal.symbol)].price;
    }

    return signal.entryPrice;
  }

  num? getWSSymbolPriceSymbolTracker(SymbolTracker s) {
    List<WSSymbol> symbols = [];
    if (s.market.toLowerCase() == 'crypto') symbols = wsSymbolsCrypto.map((e) => e).toList();
    if (s.market.toLowerCase() == 'forex') symbols = wsSymbolsForex.map((e) => e).toList();
    if (s.market.toLowerCase() == 'stocks') symbols = wsSymbolsStocks.map((e) => e).toList();

    if (symbols.map((e) => e.symbol).toList().contains(s.symbol)) {
      return symbols[symbols.map((e) => e.symbol).toList().indexOf(s.symbol)].price;
    }

    return null;
  }
}

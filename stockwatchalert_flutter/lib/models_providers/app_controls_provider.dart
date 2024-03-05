import 'dart:async';
import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart' hide AuthProvider;
import 'package:flutter/material.dart';
import 'package:package_info/package_info.dart';
import 'package:signalbyt/models/market_activity_aggr.dart';
import 'package:signalbyt/models/signal_aggr.dart';
import 'package:signalbyt/models/symbols_tracker_aggr.dart';
import 'package:signalbyt/models/ws_symbol.dart';

import '../models/app_controls_public.dart';
import '../models/market_analysis.dart';
import '../models/news_aggr.dart';
import '../models_services/firestore_service.dart';
import '../models_services/_hive_helper.dart';
import 'auth_provider.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class AppControlsProvider with ChangeNotifier {
  /* -------------------------------- NOTE INIT ------------------------------- */
  DateTime? dtWebsocketUpdated;
  String? authUserId;
  String? apiWebSocketUrl;
  String? jsonWebToken;
  int websockerTimerIntervalSecs = 30;
  Timer? websockerTimer;

  AuthProvider? _authProvider;
  AuthProvider? get authProvider => _authProvider;
  set authProvider(AuthProvider? authProvider) {
    _authProvider = authProvider;
    bool rerun = authUserId == null || authUserId != _authProvider?.authUser?.id;

    if (_authProvider?.authUser != null && rerun) {
      authUserId = _authProvider?.authUser?.id ?? '';

      streamAppControls();
      startWebsockerTime();
      notifyListeners();
    }

    if (_authProvider?.authUser == null) {
      authUserId = null;
      websockerTimer?.cancel();

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

      await HiveHelper.setApiUrl(_appControls.apiUrl);

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
      if (newJsonWebToken != jsonWebToken) {
        jsonWebToken = newJsonWebToken;
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
    websockerTimer = Timer.periodic(Duration(seconds: websockerTimerIntervalSecs), (timer) {
      websocketReconnect();
    });
  }

  void websocketReconnect() {
    var dtNow = DateTime.now();
    var dtWebsocketUpdated = this.dtWebsocketUpdated ?? dtNow;

    bool dtCheck = (dtWebsocketUpdated == dtNow) || dtNow.difference(dtWebsocketUpdated).inSeconds > websockerTimerIntervalSecs;
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

    if (appControls.apiWebSocketUrl == '') {
      socket?.close();
      socket?.disconnect();
      return;
    }

    if (appControls.apiWebSocketUrl == apiWebSocketUrl && socket?.connected == true && newJsonWebToken == jsonWebToken) return;

    apiWebSocketUrl = appControls.apiWebSocketUrl;
    jsonWebToken = newJsonWebToken;

    socket = IO.io(apiWebSocketUrl, <String, dynamic>{
      'transports': ['websocket'],
      'path': '/socketio/socket.io',
      'autoConnect': false,
      'forceNew': true,
      'extraHeaders': {
        'jsonWebToken': jsonWebToken,
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
      dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('prices_stocks', (message) {
      handlePriceData(message: message, type: 'stocks');
      dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('market_analysis', (message) {
      handleMarketAnalysis(message['data']);
      dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('news_aggr', (message) {
      handleNewsAggr(message['data']);
      dtWebsocketUpdated = DateTime.now();
    });

    socket?.on('market_activities_aggr', (message) {
      handleMarketActivityAggr(message['data']);
      dtWebsocketUpdated = DateTime.now();
    });
  }

  void cancleAllStreams() {
    disconnectSocketIo();
    notifyListeners();
    authUserId = null;
  }

  void disconnectSocketIo() {
    socket?.close();
    socket?.disconnect();
    socket = null;
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
    if (data is String) {
      data = json.decode(data);
    }

    _newsAggr = NewsAggr.fromJson(data);
    _newsCrypto = _newsAggr.dataCrypto;
    _newsStocks = _newsAggr.dataStocks;
    _newsForex = _newsAggr.dataForex;

    notifyListeners();
  }

  /* -------------------------------- NOTE NEWS ------------------------------- */
  MarketActivityAggr _marketActivityAggr = MarketActivityAggr();
  MarketActivityAggr get marketActivityAggr => _marketActivityAggr;

  List<MarketActivity> _gainers = [];
  List<MarketActivity> get gainers => _gainers;

  List<MarketActivity> _losers = [];
  List<MarketActivity> get losers => _losers;

  List<MarketActivity> _actives = [];
  List<MarketActivity> get actives => _actives;

  void handleMarketActivityAggr(data) {
    if (data is String) {
      data = json.decode(data);
      print('handleMarketActivityAggr ${data}');
    }

    _marketActivityAggr = MarketActivityAggr.fromJson(data);
    _gainers = _marketActivityAggr.gainers;
    _losers = _marketActivityAggr.losers;
    _actives = _marketActivityAggr.actives;

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

  num getWSSymbolPriceSignal(Signal signal) {
    List<WSSymbol> symbols = [];
    if (signal.market.toLowerCase() == 'crypto') symbols = wsSymbolsCrypto.map((e) => e).toList();
    if (signal.market.toLowerCase() == 'forex') symbols = wsSymbolsForex.map((e) => e).toList();
    if (signal.market.toLowerCase() == 'stocks') symbols = wsSymbolsStocks.map((e) => e).toList();

    if (symbols.map((e) => e.symbol).toList().contains(signal.symbol)) {
      return symbols[symbols.map((e) => e.symbol).toList().indexOf(signal.symbol)].price;
    }

    return signal.entryPrice;
  }

  num getLivelPriceSignalV1(Signal signal) {
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

import 'package:json_annotation/json_annotation.dart';

import '../utils/z_format.dart';
import '_parsers.dart';

part 'signal_aggr.g.dart';

@JsonSerializable(explicitToJson: true)
class SignalAggr {
  @JsonKey(defaultValue: '', name: 'id')
  String id;
  @JsonKey(defaultValue: '', name: 'name')
  String name;
  @JsonKey(defaultValue: '', name: 'nameSignalsCollection')
  String nameSignalsCollection;
  @JsonKey(defaultValue: 1, name: 'sort')
  num sort;
  @JsonKey(defaultValue: '', name: 'nameType')
  String nameType;
  @JsonKey(defaultValue: '', name: 'nameTypeSubtitle')
  String nameTypeSubtitle;
  @JsonKey(defaultValue: '', name: 'nameVersion')
  String nameVersion;
  @JsonKey(defaultValue: '', name: 'nameMarket')
  String nameMarket;
  @JsonKey(defaultValue: [], name: 'data')
  List<Signal> signals;
  //
  @JsonKey(defaultValue: null)
  Results? results7Days;
  @JsonKey(defaultValue: null)
  Results? results14Days;
  @JsonKey(defaultValue: null)
  Results? results30Days;
  @JsonKey(defaultValue: null)
  Results? results90Days;
  @JsonKey(defaultValue: null)
  Results? results180Days;
  @JsonKey(defaultValue: null)
  Results? results365Days;

  SignalAggr()
      : id = '',
        name = '',
        nameSignalsCollection = '',
        nameType = '',
        nameTypeSubtitle = '',
        nameVersion = '',
        nameMarket = '',
        sort = 0,
        signals = [],
        results7Days = null,
        results14Days = null,
        results30Days = null,
        results90Days = null,
        results180Days = null,
        results365Days = null;

  factory SignalAggr.fromJson(Map<String, dynamic> json) => _$SignalAggrFromJson(json);
  Map<String, dynamic> toJson() => _$SignalAggrToJson(this)..remove('id');

  int numLongs() {
    int numLongs = 0;
    for (var signal in signals) {
      if (signal.entryType == 'long') numLongs++;
    }
    return numLongs;
  }

  int numShorts() {
    int numShorts = 0;
    for (var signal in signals) {
      if (signal.entryType == 'short') numShorts++;
    }
    return numShorts;
  }

  int numFutures() {
    int numFutures = 0;
    for (var signal in signals) {
      if (signal.hasFutures) numFutures++;
    }
    return numFutures;
  }

  int numPending() {
    int numPending = 0;
    for (var signal in signals) {
      if (signal.entryResult == 'in progress') numPending++;
    }
    return numPending;
  }
}

@JsonSerializable(explicitToJson: true)
class Results {
  @JsonKey(defaultValue: 0)
  num avePct;
  @JsonKey(defaultValue: 0)
  num avePips;
  @JsonKey(defaultValue: 0)
  num losers;
  @JsonKey(defaultValue: 0)
  num losersPct;
  @JsonKey(defaultValue: 0)
  num losersPips;
  @JsonKey(defaultValue: 0)
  num total;
  @JsonKey(defaultValue: 0)
  num winners;
  @JsonKey(defaultValue: 0)
  num winnersPct;
  @JsonKey(defaultValue: 0)
  num winnersPips;

  Results()
      : avePct = 0,
        avePips = 0,
        losers = 0,
        losersPct = 0,
        losersPips = 0,
        total = 0,
        winners = 0,
        winnersPct = 0,
        winnersPips = 0;

  factory Results.fromJson(Map<String, dynamic> json) => _$ResultsFromJson(json);
  Map<String, dynamic> toJson() => _$ResultsToJson(this);

  num getWinRate() {
    if (total == 0) return 0;
    return (winners / total * 100).round();
  }
}

@JsonSerializable(explicitToJson: true)
class Signal {
  @JsonKey(defaultValue: '', name: 'id')
  String id;
  @JsonKey(defaultValue: '', name: 'signalName')
  String signalName;
  @JsonKey(defaultValue: '', name: 'analysisImage')
  String analysisImage;
  @JsonKey(defaultValue: '', name: 'analysisText')
  String analysisText;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'closedDateTimeEst')
  DateTime? closedDateTimeEst;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'closedDateTimeUtc')
  DateTime? closedDateTimeUtc;
  @JsonKey(defaultValue: '', name: 'comment')
  String comment;
  //
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'entryDateTimeEst')
  DateTime? entryDateTimeEst;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'entryDateTimeUtc')
  DateTime? entryDateTimeUtc;
  @JsonKey(defaultValue: 0, name: 'entryPrice')
  num entryPrice;
  @JsonKey(defaultValue: '', name: 'entryResult')
  String entryResult;
  @JsonKey(defaultValue: '', name: 'entryType')
  String entryType;
  @JsonKey(defaultValue: 0, name: 'currentPrice')
  num currentPrice;
  @JsonKey(defaultValue: '', name: 'symbol')
  String symbol;
  //
  @JsonKey(defaultValue: false, name: 'hasFutures')
  bool hasFutures;
  @JsonKey(defaultValue: false, name: 'isAlgo')
  bool isAlgo;
  @JsonKey(defaultValue: false, name: 'isClosed')
  bool isClosed;
  @JsonKey(defaultValue: false, name: 'isFree')
  bool isFree;
  @JsonKey(defaultValue: '', name: 'market')
  String market;
  //
  @JsonKey(defaultValue: 0, name: 'stopLoss')
  num stopLoss;
  @JsonKey(defaultValue: 0, name: 'stopLossPct')
  num stopLossPct;
  @JsonKey(defaultValue: 0, name: 'stopLossPips')
  num stopLossPips;
  @JsonKey(defaultValue: false, name: 'stopLossHit')
  bool stopLossHit;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'stopLossDateTimeEst')
  DateTime? stopLossDateTimeEst;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'stopLossDateTimeUtc')
  DateTime? stopLossDateTimeUtc;
  //
  @JsonKey(defaultValue: 0)
  num stopLossRevised;
  @JsonKey(defaultValue: false, name: 'stopLossRevisedTp1')
  bool stopLossRevisedTp1;
  @JsonKey(defaultValue: false, name: 'stopLossRevisedTp2')
  bool stopLossRevisedTp2;
  @JsonKey(defaultValue: false, name: 'stopLossRevisedTp3')
  bool stopLossRevisedTp3;
  //
  @JsonKey(defaultValue: 0, name: 'takeProfit1')
  num takeProfit1;
  @JsonKey(defaultValue: 0, name: 'takeProfit1Pct')
  num takeProfit1Pct;
  @JsonKey(defaultValue: 0, name: 'takeProfit1Pips')
  num takeProfit1Pips;
  @JsonKey(defaultValue: false, name: 'takeProfit1Hit')
  bool takeProfit1Hit;
  @JsonKey(defaultValue: '', name: 'takeProfit1Result')
  String takeProfit1Result;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit1DateTimeUtc')
  DateTime? takeProfit1DateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit1DateTimeEst')
  DateTime? takeProfit1DateTimeEst;
  //
  @JsonKey(defaultValue: 0, name: 'takeProfit2')
  num takeProfit2;
  @JsonKey(defaultValue: 0, name: 'takeProfit2Pct')
  num takeProfit2Pct;
  @JsonKey(defaultValue: 0, name: 'takeProfit2Pips')
  num takeProfit2Pips;
  @JsonKey(defaultValue: false, name: 'takeProfit2Hit')
  bool takeProfit2Hit;
  @JsonKey(defaultValue: '', name: 'takeProfit2Result')
  String takeProfit2Result;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit2DateTimeUtc')
  DateTime? takeProfit2DateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit2DateTimeEst')
  DateTime? takeProfit2DateTimeEst;

  //
  @JsonKey(defaultValue: 0, name: 'takeProfit3')
  num takeProfit3;
  @JsonKey(defaultValue: 0, name: 'takeProfit3Pct')
  num takeProfit3Pct;
  @JsonKey(defaultValue: 0, name: 'takeProfit3Pips')
  num takeProfit3Pips;
  @JsonKey(defaultValue: false, name: 'takeProfit3Hit')
  bool takeProfit3Hit;
  @JsonKey(defaultValue: '', name: 'takeProfit3Result')
  String takeProfit3Result;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit3DateTimeUtc')
  DateTime? takeProfit3DateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit3DateTimeEst')
  DateTime? takeProfit3DateTimeEst;
  //
  @JsonKey(defaultValue: 0, name: 'takeProfit4')
  num takeProfit4;
  @JsonKey(defaultValue: 0, name: 'takeProfit4Pct')
  num takeProfit4Pct;
  @JsonKey(defaultValue: 0, name: 'takeProfit4Pips')
  num takeProfit4Pips;
  @JsonKey(defaultValue: false, name: 'takeProfit4Hit')
  bool takeProfit4Hit;
  @JsonKey(defaultValue: '', name: 'takeProfit4Result')
  String takeProfit4Result;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit4DateTimeUtc')
  DateTime? takeProfit4DateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'takeProfit4DateTimeEst')
  DateTime? takeProfit4DateTimeEst;
  @JsonKey(defaultValue: 1, name: 'leverage')
  num leverage;

  Signal()
      : id = '',
        signalName = '',
        analysisImage = '',
        analysisText = '',
        comment = '',
        entryDateTimeEst = null,
        entryDateTimeUtc = null,
        entryPrice = 0,
        entryResult = '',
        entryType = '',
        currentPrice = 0,
        hasFutures = false,
        symbol = '',
        isAlgo = false,
        isClosed = false,
        isFree = false,
        market = '',
        stopLoss = 0,
        stopLossPct = 0,
        stopLossPips = 0,
        stopLossHit = false,
        stopLossRevised = 0,
        stopLossRevisedTp1 = false,
        stopLossRevisedTp2 = false,
        stopLossRevisedTp3 = false,
        stopLossDateTimeEst = null,
        stopLossDateTimeUtc = null,
        takeProfit1 = 0,
        takeProfit1Pct = 0,
        takeProfit1Pips = 0,
        takeProfit1Hit = false,
        takeProfit1Result = '',
        takeProfit1DateTimeEst = null,
        takeProfit1DateTimeUtc = null,
        takeProfit2 = 0,
        takeProfit2Pct = 0,
        takeProfit2Pips = 0,
        takeProfit2Hit = false,
        takeProfit2Result = '',
        takeProfit2DateTimeEst = null,
        takeProfit2DateTimeUtc = null,
        takeProfit3 = 0,
        takeProfit3Pct = 0,
        takeProfit3Pips = 0,
        takeProfit3Hit = false,
        takeProfit3Result = '',
        takeProfit3DateTimeEst = null,
        takeProfit3DateTimeUtc = null,
        takeProfit4 = 0,
        takeProfit4Pct = 0,
        takeProfit4Pips = 0,
        takeProfit4Hit = false,
        takeProfit4Result = '',
        takeProfit4DateTimeEst = null,
        takeProfit4DateTimeUtc = null,
        leverage = 1;

  factory Signal.fromJson(Map<String, dynamic> json) => _$SignalFromJson(json);
  Map<String, dynamic> toJson() => _$SignalToJson(this)
    ..remove('id')
    ..remove('createdDateTime');

  String getBreakEvenText() {
    if (stopLossRevisedTp3) return 'Stop loss moved to break even @ ${ZFormat.toPrecision(stopLossRevised, 10)} on ${ZFormat.dateFormatSignal(takeProfit3DateTimeUtc)}';
    if (stopLossRevisedTp2) return 'Stop loss moved to break even @ ${ZFormat.toPrecision(stopLossRevised, 10)} on ${ZFormat.dateFormatSignal(takeProfit2DateTimeUtc)}';
    if (stopLossRevisedTp1) return 'Stop loss moved to break even @ ${ZFormat.toPrecision(stopLossRevised, 10)} on ${ZFormat.dateFormatSignal(takeProfit1DateTimeUtc)}';
    return '';
  }

  String getPipsOrPercentStr({bool isPips = false, num pips = 0, num percent = 0}) {
    if (isPips) {
      return '${pips} pips';
    } else {
      return ZFormat.numToPercent(percent);
    }
  }

  compareEntryPriceWithCurrentPrice({required num price, isPips = false}) {
    if (price == 0) return 0;

    if (isPips) {
      num val = 0;
      if (entryType == 'long') val = (price - entryPrice) * 10000;
      if (entryType == 'short') val = (entryPrice - price) * 10000;
      if (symbol.contains('JPY')) val = val / 100;
      return (val / 1).round() * 1;
    }

    if (entryType == 'long') return (price - entryPrice) / entryPrice;
    if (entryType == 'short') return (entryPrice - price) / price;
  }

  String getEngineName() {
    if (isAlgo) return 'Algo';
    return 'Admin';
  }

  DateTime getEntryDateTimeUtc() {
    return entryDateTimeUtc ?? DateTime.now();
  }

  String getSignalXFavoriteId() {
    String SignalAggrXName = this.signalName;
    String symbol = this.symbol;
    String dateTimeString = this.entryDateTimeUtc?.toIso8601String() ?? '';
    String id = '$SignalAggrXName-$symbol-$dateTimeString';
    return id;
  }
}

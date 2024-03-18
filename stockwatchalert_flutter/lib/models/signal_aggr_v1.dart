import 'package:flutter/material.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:stockwatchalert/constants/app_colors.dart';
import 'package:stockwatchalert/models/_parsers.dart';
import 'package:stockwatchalert/utils/z_format.dart';

part 'signal_aggr_v1.g.dart';

@JsonSerializable(explicitToJson: true)
class SignalAggrV1 {
  @JsonKey(defaultValue: '', name: 'id')
  String id;
  @JsonKey(defaultValue: '', name: 'nameId')
  String nameId;
  @JsonKey(defaultValue: 1, name: 'nameSort')
  num nameSort;
  @JsonKey(defaultValue: '', name: 'nameType')
  String nameType;
  @JsonKey(defaultValue: '', name: 'nameMarket')
  String nameMarket;
  @JsonKey(defaultValue: '', name: 'nameCollection')
  String nameCollection;
  @JsonKey(defaultValue: '', name: 'nameTypeSubtitle')
  String nameTypeSubtitle;
  @JsonKey(defaultValue: '', name: 'nameVersion')
  String nameVersion;
  @JsonKey(defaultValue: false, name: 'nameIsAdminOnly')
  bool nameIsAdminOnly;
  @JsonKey(defaultValue: [], name: 'signals')
  List<SignalV1> signals;
  @JsonKey(defaultValue: [], name: 'results')
  List<ResultsV1> results;

  SignalAggrV1()
      : id = '',
        nameId = '',
        nameType = '',
        nameTypeSubtitle = '',
        nameMarket = '',
        nameCollection = '',
        nameVersion = '',
        nameIsAdminOnly = false,
        nameSort = 0,
        signals = [],
        results = [];

  factory SignalAggrV1.fromJson(Map<String, dynamic> json) => _$SignalAggrV1FromJson(json);
  Map<String, dynamic> toJson() => _$SignalAggrV1ToJson(this)..remove('id');

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

  int numPending() {
    int numPending = 0;
    for (var signal in signals) {
      if (signal.statusTrade == 'open') numPending++;
    }
    return numPending;
  }
}

@JsonSerializable(explicitToJson: true)
class ResultsV1 {
  @JsonKey(defaultValue: 0)
  num days;
  @JsonKey(defaultValue: 0)
  num sort;
  @JsonKey(defaultValue: 0)
  num total;
  @JsonKey(defaultValue: 0)
  num win;
  @JsonKey(defaultValue: 0)
  num loss;
  @JsonKey(defaultValue: 0)
  num winRate;

  ResultsV1()
      : days = 0,
        sort = 0,
        total = 0,
        win = 0,
        loss = 0,
        winRate = 0;

  factory ResultsV1.fromJson(Map<String, dynamic> json) => _$ResultsV1FromJson(json);
  Map<String, dynamic> toJson() => _$ResultsV1ToJson(this);

  num getWinRate() {
    if (total == 0) return 0;
    return (win / total * 100).round();
  }
}

@JsonSerializable(explicitToJson: true)
class SignalV1 {
  @JsonKey(defaultValue: '', name: 'id')
  String id;
  @JsonKey(defaultValue: 'open', name: 'statusTrade')
  String statusTrade;
  @JsonKey(defaultValue: 'In Progress', name: 'statusTarget')
  String statusTarget;
  @JsonKey(defaultValue: '', name: 'symbol')
  String symbol;
  @JsonKey(defaultValue: 1, name: 'leverage')
  num leverage;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'entryDateTimeUtc')
  DateTime? entryDateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'exitDateTimeUtc')
  DateTime? exitDateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'lastCheckedDateTimeUtc')
  DateTime? lastCheckedDateTimeUtc;
  @JsonKey(defaultValue: 0, name: 'entryPrice')
  num entryPrice;
  @JsonKey(defaultValue: 0, name: 'exitPrice')
  num exitPrice;
  @JsonKey(defaultValue: '', name: 'entryType')
  String entryType;
  @JsonKey(defaultValue: 0, name: 'currentPrice')
  num currentPrice;
  @JsonKey(defaultValue: false, name: 'isClosed')
  bool isClosed;
  @JsonKey(defaultValue: 'crypto', name: 'market')
  String market;
  @JsonKey(defaultValue: '', name: 'analysisImage')
  String analysisImage;
  @JsonKey(defaultValue: '', name: 'analysisText')
  String analysisText;
  @JsonKey(defaultValue: '', name: 'comment')
  String comment;
  @JsonKey(defaultValue: 0, name: 'tp1Pct')
  num tp1Pct;
  @JsonKey(defaultValue: 0, name: 'tp1Pips')
  num tp1Pips;
  @JsonKey(defaultValue: 0, name: 'tp1Price')
  num tp1Price;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'tp1DateTimeUtc')
  DateTime? tp1DateTimeUtc;
  @JsonKey(defaultValue: 0, name: 'tp2Pct')
  num tp2Pct;
  @JsonKey(defaultValue: 0, name: 'tp2Pips')
  num tp2Pips;
  @JsonKey(defaultValue: 0, name: 'tp2Price')
  num tp2Price;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'tp2DateTimeUtc')
  DateTime? tp2DateTimeUtc;
  @JsonKey(defaultValue: 0, name: 'tp3Pct')
  num tp3Pct;
  @JsonKey(defaultValue: 0, name: 'tp3Pips')
  num tp3Pips;
  @JsonKey(defaultValue: 0, name: 'tp3Price')
  num tp3Price;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'tp3DateTimeUtc')
  DateTime? tp3DateTimeUtc;
  @JsonKey(defaultValue: 0, name: 'slPct')
  num slPct;
  @JsonKey(defaultValue: 0, name: 'slPips')
  num slPips;
  @JsonKey(defaultValue: 0, name: 'slPrice')
  num slPrice;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'slDateTimeUtc')
  DateTime? slDateTimeUtc;
  @JsonKey(defaultValue: 0, name: 'amtProfitMaxPct')
  num amtProfitMaxPct;
  @JsonKey(defaultValue: 0, name: 'amtProfitMinPct')
  num amtProfitMinPct;
  @JsonKey(defaultValue: 0, name: 'amtProfitMaxPips')
  num amtProfitMaxPips;
  @JsonKey(defaultValue: 0, name: 'amtProfitMinPips')
  num amtProfitMinPips;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'amtProfitMaxDateTimeUtc')
  DateTime? amtProfitMaxDateTimeUtc;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'amtProfitMinDateTimeUtc')
  DateTime? lamtProfitMinDateTimeUtc;

  SignalV1()
      : id = '',
        statusTrade = 'open',
        statusTarget = 'In Progress',
        symbol = '',
        leverage = 0,
        entryDateTimeUtc = null,
        exitDateTimeUtc = null,
        lastCheckedDateTimeUtc = null,
        entryPrice = 0,
        exitPrice = 0,
        entryType = '',
        currentPrice = 0,
        isClosed = false,
        market = '',
        analysisImage = '',
        analysisText = '',
        comment = '',
        tp1Pct = 0,
        tp1Pips = 0,
        tp1Price = 0,
        tp1DateTimeUtc = null,
        tp2Pct = 0,
        tp2Pips = 0,
        tp2Price = 0,
        tp2DateTimeUtc = null,
        tp3Pct = 0,
        tp3Pips = 0,
        tp3Price = 0,
        tp3DateTimeUtc = null,
        slPct = 0,
        slPips = 0,
        slPrice = 0,
        slDateTimeUtc = null,
        amtProfitMaxPct = 0,
        amtProfitMinPct = 0,
        amtProfitMaxPips = 0,
        amtProfitMinPips = 0,
        amtProfitMaxDateTimeUtc = null,
        lamtProfitMinDateTimeUtc = null;

  factory SignalV1.fromJson(Map<String, dynamic> json) => _$SignalV1FromJson(json);
  Map<String, dynamic> toJson() => _$SignalV1ToJson(this)..remove('id');

/* -------------------------------- FUNCTIONS ------------------------------- */
  String get getMaxPctPips {
    if (market == 'forex') return 'Max Profit ${ZFormat.toPrecision(amtProfitMaxPips, 0)}pips';
    return 'Max Profit ${ZFormat.numToPercent(amtProfitMaxPct)}';
  }

  String get getMinPctPips {
    if (market == 'forex') return 'Min Profit ${ZFormat.toPrecision(amtProfitMinPips, 0)}pips';
    return 'Min Profit ${ZFormat.numToPercent(amtProfitMinPct)}';
  }

  DateTime getEntryDateTimeUtc() {
    return entryDateTimeUtc ?? DateTime.now();
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

  Color get getProgressColor {
    if (statusTrade == 'open') return Colors.grey;
    if (statusTrade == 'win') return AppColors.blue;
    if (statusTrade == 'loss') return AppColors.red;
    return Colors.grey;
  }
}

// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'signal_aggr_v1.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SignalAggrV1 _$SignalAggrV1FromJson(Map<String, dynamic> json) => SignalAggrV1()
  ..id = json['id'] as String? ?? ''
  ..nameId = json['nameId'] as String? ?? ''
  ..nameSort = json['nameSort'] as num? ?? 1
  ..nameType = json['nameType'] as String? ?? ''
  ..nameMarket = json['nameMarket'] as String? ?? ''
  ..nameCollection = json['nameCollection'] as String? ?? ''
  ..nameTypeSubtitle = json['nameTypeSubtitle'] as String? ?? ''
  ..nameVersion = json['nameVersion'] as String? ?? ''
  ..nameIsAdminOnly = json['nameIsAdminOnly'] as bool? ?? false
  ..signals = (json['signals'] as List<dynamic>?)
          ?.map((e) => SignalV1.fromJson(e as Map<String, dynamic>))
          .toList() ??
      []
  ..results = (json['results'] as List<dynamic>?)
          ?.map((e) => ResultsV1.fromJson(e as Map<String, dynamic>))
          .toList() ??
      [];

Map<String, dynamic> _$SignalAggrV1ToJson(SignalAggrV1 instance) =>
    <String, dynamic>{
      'id': instance.id,
      'nameId': instance.nameId,
      'nameSort': instance.nameSort,
      'nameType': instance.nameType,
      'nameMarket': instance.nameMarket,
      'nameCollection': instance.nameCollection,
      'nameTypeSubtitle': instance.nameTypeSubtitle,
      'nameVersion': instance.nameVersion,
      'nameIsAdminOnly': instance.nameIsAdminOnly,
      'signals': instance.signals.map((e) => e.toJson()).toList(),
      'results': instance.results.map((e) => e.toJson()).toList(),
    };

ResultsV1 _$ResultsV1FromJson(Map<String, dynamic> json) => ResultsV1()
  ..days = json['days'] as num? ?? 0
  ..sort = json['sort'] as num? ?? 0
  ..total = json['total'] as num? ?? 0
  ..win = json['win'] as num? ?? 0
  ..loss = json['loss'] as num? ?? 0
  ..winRate = json['winRate'] as num? ?? 0;

Map<String, dynamic> _$ResultsV1ToJson(ResultsV1 instance) => <String, dynamic>{
      'days': instance.days,
      'sort': instance.sort,
      'total': instance.total,
      'win': instance.win,
      'loss': instance.loss,
      'winRate': instance.winRate,
    };

SignalV1 _$SignalV1FromJson(Map<String, dynamic> json) => SignalV1()
  ..id = json['id'] as String? ?? ''
  ..statusTrade = json['statusTrade'] as String? ?? 'open'
  ..statusTarget = json['statusTarget'] as String? ?? 'In Progress'
  ..symbol = json['symbol'] as String? ?? ''
  ..leverage = json['leverage'] as num? ?? 1
  ..entryDateTimeUtc = parseToDateTime(json['entryDateTimeUtc'])
  ..exitDateTimeUtc = parseToDateTime(json['exitDateTimeUtc'])
  ..lastCheckedDateTimeUtc = parseToDateTime(json['lastCheckedDateTimeUtc'])
  ..entryPrice = json['entryPrice'] as num? ?? 0
  ..exitPrice = json['exitPrice'] as num? ?? 0
  ..entryType = json['entryType'] as String? ?? ''
  ..currentPrice = json['currentPrice'] as num? ?? 0
  ..isClosed = json['isClosed'] as bool? ?? false
  ..market = json['market'] as String? ?? 'crypto'
  ..analysisImage = json['analysisImage'] as String? ?? ''
  ..analysisText = json['analysisText'] as String? ?? ''
  ..comment = json['comment'] as String? ?? ''
  ..tp1Pct = json['tp1Pct'] as num? ?? 0
  ..tp1Pips = json['tp1Pips'] as num? ?? 0
  ..tp1Price = json['tp1Price'] as num? ?? 0
  ..tp1DateTimeUtc = parseToDateTime(json['tp1DateTimeUtc'])
  ..tp2Pct = json['tp2Pct'] as num? ?? 0
  ..tp2Pips = json['tp2Pips'] as num? ?? 0
  ..tp2Price = json['tp2Price'] as num? ?? 0
  ..tp2DateTimeUtc = parseToDateTime(json['tp2DateTimeUtc'])
  ..tp3Pct = json['tp3Pct'] as num? ?? 0
  ..tp3Pips = json['tp3Pips'] as num? ?? 0
  ..tp3Price = json['tp3Price'] as num? ?? 0
  ..tp3DateTimeUtc = parseToDateTime(json['tp3DateTimeUtc'])
  ..slPct = json['slPct'] as num? ?? 0
  ..slPips = json['slPips'] as num? ?? 0
  ..slPrice = json['slPrice'] as num? ?? 0
  ..slDateTimeUtc = parseToDateTime(json['slDateTimeUtc'])
  ..amtProfitMaxPct = json['amtProfitMaxPct'] as num? ?? 0
  ..amtProfitMinPct = json['amtProfitMinPct'] as num? ?? 0
  ..amtProfitMaxPips = json['amtProfitMaxPips'] as num? ?? 0
  ..amtProfitMinPips = json['amtProfitMinPips'] as num? ?? 0
  ..amtProfitMaxDateTimeUtc = parseToDateTime(json['amtProfitMaxDateTimeUtc'])
  ..lamtProfitMinDateTimeUtc = parseToDateTime(json['amtProfitMinDateTimeUtc']);

Map<String, dynamic> _$SignalV1ToJson(SignalV1 instance) => <String, dynamic>{
      'id': instance.id,
      'statusTrade': instance.statusTrade,
      'statusTarget': instance.statusTarget,
      'symbol': instance.symbol,
      'leverage': instance.leverage,
      'entryDateTimeUtc': parseToDateTime(instance.entryDateTimeUtc),
      'exitDateTimeUtc': parseToDateTime(instance.exitDateTimeUtc),
      'lastCheckedDateTimeUtc':
          parseToDateTime(instance.lastCheckedDateTimeUtc),
      'entryPrice': instance.entryPrice,
      'exitPrice': instance.exitPrice,
      'entryType': instance.entryType,
      'currentPrice': instance.currentPrice,
      'isClosed': instance.isClosed,
      'market': instance.market,
      'analysisImage': instance.analysisImage,
      'analysisText': instance.analysisText,
      'comment': instance.comment,
      'tp1Pct': instance.tp1Pct,
      'tp1Pips': instance.tp1Pips,
      'tp1Price': instance.tp1Price,
      'tp1DateTimeUtc': parseToDateTime(instance.tp1DateTimeUtc),
      'tp2Pct': instance.tp2Pct,
      'tp2Pips': instance.tp2Pips,
      'tp2Price': instance.tp2Price,
      'tp2DateTimeUtc': parseToDateTime(instance.tp2DateTimeUtc),
      'tp3Pct': instance.tp3Pct,
      'tp3Pips': instance.tp3Pips,
      'tp3Price': instance.tp3Price,
      'tp3DateTimeUtc': parseToDateTime(instance.tp3DateTimeUtc),
      'slPct': instance.slPct,
      'slPips': instance.slPips,
      'slPrice': instance.slPrice,
      'slDateTimeUtc': parseToDateTime(instance.slDateTimeUtc),
      'amtProfitMaxPct': instance.amtProfitMaxPct,
      'amtProfitMinPct': instance.amtProfitMinPct,
      'amtProfitMaxPips': instance.amtProfitMaxPips,
      'amtProfitMinPips': instance.amtProfitMinPips,
      'amtProfitMaxDateTimeUtc':
          parseToDateTime(instance.amtProfitMaxDateTimeUtc),
      'amtProfitMinDateTimeUtc':
          parseToDateTime(instance.lamtProfitMinDateTimeUtc),
    };

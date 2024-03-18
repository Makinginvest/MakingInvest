// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'signal_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SignalAggr _$SignalAggrFromJson(Map<String, dynamic> json) => SignalAggr()
  ..id = json['id'] as String? ?? ''
  ..name = json['name'] as String? ?? ''
  ..nameSignalsCollection = json['nameSignalsCollection'] as String? ?? ''
  ..sort = json['sort'] as num? ?? 1
  ..nameType = json['nameType'] as String? ?? ''
  ..nameTypeSubtitle = json['nameTypeSubtitle'] as String? ?? ''
  ..nameVersion = json['nameVersion'] as String? ?? ''
  ..nameMarket = json['nameMarket'] as String? ?? ''
  ..signals = (json['data'] as List<dynamic>?)
          ?.map((e) => Signal.fromJson(e as Map<String, dynamic>))
          .toList() ??
      []
  ..results7Days = json['results7Days'] == null
      ? null
      : Results.fromJson(json['results7Days'] as Map<String, dynamic>)
  ..results14Days = json['results14Days'] == null
      ? null
      : Results.fromJson(json['results14Days'] as Map<String, dynamic>)
  ..results30Days = json['results30Days'] == null
      ? null
      : Results.fromJson(json['results30Days'] as Map<String, dynamic>)
  ..results90Days = json['results90Days'] == null
      ? null
      : Results.fromJson(json['results90Days'] as Map<String, dynamic>)
  ..results180Days = json['results180Days'] == null
      ? null
      : Results.fromJson(json['results180Days'] as Map<String, dynamic>)
  ..results365Days = json['results365Days'] == null
      ? null
      : Results.fromJson(json['results365Days'] as Map<String, dynamic>);

Map<String, dynamic> _$SignalAggrToJson(SignalAggr instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'nameSignalsCollection': instance.nameSignalsCollection,
      'sort': instance.sort,
      'nameType': instance.nameType,
      'nameTypeSubtitle': instance.nameTypeSubtitle,
      'nameVersion': instance.nameVersion,
      'nameMarket': instance.nameMarket,
      'data': instance.signals.map((e) => e.toJson()).toList(),
      'results7Days': instance.results7Days?.toJson(),
      'results14Days': instance.results14Days?.toJson(),
      'results30Days': instance.results30Days?.toJson(),
      'results90Days': instance.results90Days?.toJson(),
      'results180Days': instance.results180Days?.toJson(),
      'results365Days': instance.results365Days?.toJson(),
    };

Results _$ResultsFromJson(Map<String, dynamic> json) => Results()
  ..avePct = json['avePct'] as num? ?? 0
  ..avePips = json['avePips'] as num? ?? 0
  ..losers = json['losers'] as num? ?? 0
  ..losersPct = json['losersPct'] as num? ?? 0
  ..losersPips = json['losersPips'] as num? ?? 0
  ..total = json['total'] as num? ?? 0
  ..winners = json['winners'] as num? ?? 0
  ..winnersPct = json['winnersPct'] as num? ?? 0
  ..winnersPips = json['winnersPips'] as num? ?? 0;

Map<String, dynamic> _$ResultsToJson(Results instance) => <String, dynamic>{
      'avePct': instance.avePct,
      'avePips': instance.avePips,
      'losers': instance.losers,
      'losersPct': instance.losersPct,
      'losersPips': instance.losersPips,
      'total': instance.total,
      'winners': instance.winners,
      'winnersPct': instance.winnersPct,
      'winnersPips': instance.winnersPips,
    };

Signal _$SignalFromJson(Map<String, dynamic> json) => Signal()
  ..id = json['id'] as String? ?? ''
  ..signalName = json['signalName'] as String? ?? ''
  ..analysisImage = json['analysisImage'] as String? ?? ''
  ..analysisText = json['analysisText'] as String? ?? ''
  ..closedDateTimeEst = parseToDateTime(json['closedDateTimeEst'])
  ..closedDateTimeUtc = parseToDateTime(json['closedDateTimeUtc'])
  ..comment = json['comment'] as String? ?? ''
  ..entryDateTimeEst = parseToDateTime(json['entryDateTimeEst'])
  ..entryDateTimeUtc = parseToDateTime(json['entryDateTimeUtc'])
  ..entryPrice = json['entryPrice'] as num? ?? 0
  ..entryResult = json['entryResult'] as String? ?? ''
  ..entryType = json['entryType'] as String? ?? ''
  ..currentPrice = json['currentPrice'] as num? ?? 0
  ..symbol = json['symbol'] as String? ?? ''
  ..hasFutures = json['hasFutures'] as bool? ?? false
  ..isAlgo = json['isAlgo'] as bool? ?? false
  ..isClosed = json['isClosed'] as bool? ?? false
  ..isFree = json['isFree'] as bool? ?? false
  ..market = json['market'] as String? ?? ''
  ..stopLoss = json['stopLoss'] as num? ?? 0
  ..stopLossPct = json['stopLossPct'] as num? ?? 0
  ..stopLossPips = json['stopLossPips'] as num? ?? 0
  ..stopLossHit = json['stopLossHit'] as bool? ?? false
  ..stopLossDateTimeEst = parseToDateTime(json['stopLossDateTimeEst'])
  ..stopLossDateTimeUtc = parseToDateTime(json['stopLossDateTimeUtc'])
  ..stopLossRevised = json['stopLossRevised'] as num? ?? 0
  ..stopLossRevisedTp1 = json['stopLossRevisedTp1'] as bool? ?? false
  ..stopLossRevisedTp2 = json['stopLossRevisedTp2'] as bool? ?? false
  ..stopLossRevisedTp3 = json['stopLossRevisedTp3'] as bool? ?? false
  ..takeProfit1 = json['takeProfit1'] as num? ?? 0
  ..takeProfit1Pct = json['takeProfit1Pct'] as num? ?? 0
  ..takeProfit1Pips = json['takeProfit1Pips'] as num? ?? 0
  ..takeProfit1Hit = json['takeProfit1Hit'] as bool? ?? false
  ..takeProfit1Result = json['takeProfit1Result'] as String? ?? ''
  ..takeProfit1DateTimeUtc = parseToDateTime(json['takeProfit1DateTimeUtc'])
  ..takeProfit1DateTimeEst = parseToDateTime(json['takeProfit1DateTimeEst'])
  ..takeProfit2 = json['takeProfit2'] as num? ?? 0
  ..takeProfit2Pct = json['takeProfit2Pct'] as num? ?? 0
  ..takeProfit2Pips = json['takeProfit2Pips'] as num? ?? 0
  ..takeProfit2Hit = json['takeProfit2Hit'] as bool? ?? false
  ..takeProfit2Result = json['takeProfit2Result'] as String? ?? ''
  ..takeProfit2DateTimeUtc = parseToDateTime(json['takeProfit2DateTimeUtc'])
  ..takeProfit2DateTimeEst = parseToDateTime(json['takeProfit2DateTimeEst'])
  ..takeProfit3 = json['takeProfit3'] as num? ?? 0
  ..takeProfit3Pct = json['takeProfit3Pct'] as num? ?? 0
  ..takeProfit3Pips = json['takeProfit3Pips'] as num? ?? 0
  ..takeProfit3Hit = json['takeProfit3Hit'] as bool? ?? false
  ..takeProfit3Result = json['takeProfit3Result'] as String? ?? ''
  ..takeProfit3DateTimeUtc = parseToDateTime(json['takeProfit3DateTimeUtc'])
  ..takeProfit3DateTimeEst = parseToDateTime(json['takeProfit3DateTimeEst'])
  ..takeProfit4 = json['takeProfit4'] as num? ?? 0
  ..takeProfit4Pct = json['takeProfit4Pct'] as num? ?? 0
  ..takeProfit4Pips = json['takeProfit4Pips'] as num? ?? 0
  ..takeProfit4Hit = json['takeProfit4Hit'] as bool? ?? false
  ..takeProfit4Result = json['takeProfit4Result'] as String? ?? ''
  ..takeProfit4DateTimeUtc = parseToDateTime(json['takeProfit4DateTimeUtc'])
  ..takeProfit4DateTimeEst = parseToDateTime(json['takeProfit4DateTimeEst'])
  ..leverage = json['leverage'] as num? ?? 1;

Map<String, dynamic> _$SignalToJson(Signal instance) => <String, dynamic>{
      'id': instance.id,
      'signalName': instance.signalName,
      'analysisImage': instance.analysisImage,
      'analysisText': instance.analysisText,
      'closedDateTimeEst': parseToDateTime(instance.closedDateTimeEst),
      'closedDateTimeUtc': parseToDateTime(instance.closedDateTimeUtc),
      'comment': instance.comment,
      'entryDateTimeEst': parseToDateTime(instance.entryDateTimeEst),
      'entryDateTimeUtc': parseToDateTime(instance.entryDateTimeUtc),
      'entryPrice': instance.entryPrice,
      'entryResult': instance.entryResult,
      'entryType': instance.entryType,
      'currentPrice': instance.currentPrice,
      'symbol': instance.symbol,
      'hasFutures': instance.hasFutures,
      'isAlgo': instance.isAlgo,
      'isClosed': instance.isClosed,
      'isFree': instance.isFree,
      'market': instance.market,
      'stopLoss': instance.stopLoss,
      'stopLossPct': instance.stopLossPct,
      'stopLossPips': instance.stopLossPips,
      'stopLossHit': instance.stopLossHit,
      'stopLossDateTimeEst': parseToDateTime(instance.stopLossDateTimeEst),
      'stopLossDateTimeUtc': parseToDateTime(instance.stopLossDateTimeUtc),
      'stopLossRevised': instance.stopLossRevised,
      'stopLossRevisedTp1': instance.stopLossRevisedTp1,
      'stopLossRevisedTp2': instance.stopLossRevisedTp2,
      'stopLossRevisedTp3': instance.stopLossRevisedTp3,
      'takeProfit1': instance.takeProfit1,
      'takeProfit1Pct': instance.takeProfit1Pct,
      'takeProfit1Pips': instance.takeProfit1Pips,
      'takeProfit1Hit': instance.takeProfit1Hit,
      'takeProfit1Result': instance.takeProfit1Result,
      'takeProfit1DateTimeUtc':
          parseToDateTime(instance.takeProfit1DateTimeUtc),
      'takeProfit1DateTimeEst':
          parseToDateTime(instance.takeProfit1DateTimeEst),
      'takeProfit2': instance.takeProfit2,
      'takeProfit2Pct': instance.takeProfit2Pct,
      'takeProfit2Pips': instance.takeProfit2Pips,
      'takeProfit2Hit': instance.takeProfit2Hit,
      'takeProfit2Result': instance.takeProfit2Result,
      'takeProfit2DateTimeUtc':
          parseToDateTime(instance.takeProfit2DateTimeUtc),
      'takeProfit2DateTimeEst':
          parseToDateTime(instance.takeProfit2DateTimeEst),
      'takeProfit3': instance.takeProfit3,
      'takeProfit3Pct': instance.takeProfit3Pct,
      'takeProfit3Pips': instance.takeProfit3Pips,
      'takeProfit3Hit': instance.takeProfit3Hit,
      'takeProfit3Result': instance.takeProfit3Result,
      'takeProfit3DateTimeUtc':
          parseToDateTime(instance.takeProfit3DateTimeUtc),
      'takeProfit3DateTimeEst':
          parseToDateTime(instance.takeProfit3DateTimeEst),
      'takeProfit4': instance.takeProfit4,
      'takeProfit4Pct': instance.takeProfit4Pct,
      'takeProfit4Pips': instance.takeProfit4Pips,
      'takeProfit4Hit': instance.takeProfit4Hit,
      'takeProfit4Result': instance.takeProfit4Result,
      'takeProfit4DateTimeUtc':
          parseToDateTime(instance.takeProfit4DateTimeUtc),
      'takeProfit4DateTimeEst':
          parseToDateTime(instance.takeProfit4DateTimeEst),
      'leverage': instance.leverage,
    };

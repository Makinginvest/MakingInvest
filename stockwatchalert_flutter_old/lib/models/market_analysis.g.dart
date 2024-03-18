// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'market_analysis.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

MarketAnalysis _$MarketAnalysisFromJson(Map<String, dynamic> json) =>
    MarketAnalysis()
      ..id = json['_id'] as String? ?? ''
      ..cryptoSymbolsAnalysis = (json['cryptoSymbolsAnalysis']
                  as List<dynamic>?)
              ?.map(
                  (e) => MarketAnalysisItem.fromJson(e as Map<String, dynamic>))
              .toList() ??
          []
      ..dtUpdated = parseToDateTime(json['dtUpdated']);

Map<String, dynamic> _$MarketAnalysisToJson(MarketAnalysis instance) =>
    <String, dynamic>{
      '_id': instance.id,
      'cryptoSymbolsAnalysis':
          instance.cryptoSymbolsAnalysis.map((e) => e.toJson()).toList(),
      'dtUpdated': parseToDateTime(instance.dtUpdated),
    };

MarketAnalysisItem _$MarketAnalysisItemFromJson(Map<String, dynamic> json) =>
    MarketAnalysisItem()
      ..symbol = json['symbol'] as String? ?? ''
      ..data = (json['data'] as List<dynamic>?)
              ?.map((e) =>
                  MarketAnalysisItemData.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];

Map<String, dynamic> _$MarketAnalysisItemToJson(MarketAnalysisItem instance) =>
    <String, dynamic>{
      'symbol': instance.symbol,
      'data': instance.data.map((e) => e.toJson()).toList(),
    };

MarketAnalysisItemData _$MarketAnalysisItemDataFromJson(
        Map<String, dynamic> json) =>
    MarketAnalysisItemData()
      ..timeframe = json['timeframe'] as String? ?? ''
      ..status = json['status'] as String? ?? ''
      ..statusMessages = (json['statusMessages'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [];

Map<String, dynamic> _$MarketAnalysisItemDataToJson(
        MarketAnalysisItemData instance) =>
    <String, dynamic>{
      'timeframe': instance.timeframe,
      'status': instance.status,
      'statusMessages': instance.statusMessages,
    };

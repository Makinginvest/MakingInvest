// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'symbols_tracker_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SymbolTrackerAggr _$SymbolTrackerAggrFromJson(Map<String, dynamic> json) =>
    SymbolTrackerAggr()
      ..id = json['id'] as String? ?? ''
      ..crypto = (json['crypto'] as List<dynamic>?)
              ?.map((e) => SymbolTracker.fromJson(e as Map<String, dynamic>))
              .toList() ??
          []
      ..forex = (json['forex'] as List<dynamic>?)
              ?.map((e) => SymbolTracker.fromJson(e as Map<String, dynamic>))
              .toList() ??
          []
      ..stocks = (json['stocks'] as List<dynamic>?)
              ?.map((e) => SymbolTracker.fromJson(e as Map<String, dynamic>))
              .toList() ??
          []
      ..lastUpdatedDateTime = parseToDateTime(json['lastUpdatedDateTime']);

Map<String, dynamic> _$SymbolTrackerAggrToJson(SymbolTrackerAggr instance) =>
    <String, dynamic>{
      'id': instance.id,
      'crypto': instance.crypto.map((e) => e.toJson()).toList(),
      'forex': instance.forex.map((e) => e.toJson()).toList(),
      'stocks': instance.stocks.map((e) => e.toJson()).toList(),
      'lastUpdatedDateTime': parseToDateTime(instance.lastUpdatedDateTime),
    };

SymbolTracker _$SymbolTrackerFromJson(Map<String, dynamic> json) =>
    SymbolTracker()
      ..symbol = json['symbol'] as String? ?? ''
      ..val1hrAgo = json['val1hrAgo'] as num?
      ..val2hrAgo = json['val2hrAgo'] as num?
      ..val4hrAgo = json['val4hrAgo'] as num?
      ..val8hrAgo = json['val8hrAgo'] as num?
      ..val24hrAgo = json['val24hrAgo'] as num?
      ..val7dAgo = json['val7dAgo'] as num?
      ..market = json['market'] as String? ?? '';

Map<String, dynamic> _$SymbolTrackerToJson(SymbolTracker instance) =>
    <String, dynamic>{
      'symbol': instance.symbol,
      'val1hrAgo': instance.val1hrAgo,
      'val2hrAgo': instance.val2hrAgo,
      'val4hrAgo': instance.val4hrAgo,
      'val8hrAgo': instance.val8hrAgo,
      'val24hrAgo': instance.val24hrAgo,
      'val7dAgo': instance.val7dAgo,
      'market': instance.market,
    };

// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'market_activity_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

MarketActivityAggr _$MarketActivityAggrFromJson(Map<String, dynamic> json) => MarketActivityAggr()
  ..id = json['id'] as String? ?? ''
  ..gainers = (json['gainers'] as List<dynamic>?)?.map((e) => MarketActivity.fromJson(e as Map<String, dynamic>)).toList() ?? []
  ..losers = (json['losers'] as List<dynamic>?)?.map((e) => MarketActivity.fromJson(e as Map<String, dynamic>)).toList() ?? []
  ..actives = (json['actives'] as List<dynamic>?)?.map((e) => MarketActivity.fromJson(e as Map<String, dynamic>)).toList() ?? [];

Map<String, dynamic> _$MarketActivityAggrToJson(MarketActivityAggr instance) => <String, dynamic>{
      'id': instance.id,
      'gainers': instance.gainers.map((e) => e.toJson()).toList(),
      'losers': instance.losers.map((e) => e.toJson()).toList(),
      'actives': instance.actives.map((e) => e.toJson()).toList(),
    };

MarketActivity _$MarketActivityFromJson(Map<String, dynamic> json) => MarketActivity()
  ..symbol = json['symbol'] as String? ?? ''
  ..name = json['name'] as String? ?? ''
  ..change = json['change'] as num? ?? 0
  ..changesPercentage = json['changesPercentage'] as num? ?? 0
  ..price = json['price'] as num? ?? 0;

Map<String, dynamic> _$MarketActivityToJson(MarketActivity instance) => <String, dynamic>{
      'symbol': instance.symbol,
      'name': instance.name,
      'change': instance.change,
      'changesPercentage': instance.changesPercentage,
      'price': instance.price,
    };

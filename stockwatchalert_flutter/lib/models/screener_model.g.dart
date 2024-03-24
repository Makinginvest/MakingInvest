// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'screener_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ScreenerModel _$ScreenerModelFromJson(Map<String, dynamic> json) =>
    ScreenerModel()
      ..count = json['count'] as num? ?? 0
      ..data = (json['data'] as List<dynamic>?)
              ?.map(
                  (e) => ScreenerDataModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];

Map<String, dynamic> _$ScreenerModelToJson(ScreenerModel instance) =>
    <String, dynamic>{
      'count': instance.count,
      'data': instance.data.map((e) => e.toJson()).toList(),
    };

ScreenerDataModel _$ScreenerDataModelFromJson(Map<String, dynamic> json) =>
    ScreenerDataModel()
      ..close = json['close'] as num? ?? 0
      ..volume = json['volume'] as num? ?? 0
      ..symbol = json['symbol'] as String? ?? ''
      ..rating = json['rating'] as String? ?? ''
      ..ratingRecommendation = json['ratingRecommendation'] as String? ?? ''
      ..image = json['image'] as String? ?? ''
      ..exchangeShortName = json['exchangeShortName'] as String? ?? '';

Map<String, dynamic> _$ScreenerDataModelToJson(ScreenerDataModel instance) =>
    <String, dynamic>{
      'close': instance.close,
      'volume': instance.volume,
      'symbol': instance.symbol,
      'rating': instance.rating,
      'ratingRecommendation': instance.ratingRecommendation,
      'image': instance.image,
      'exchangeShortName': instance.exchangeShortName,
    };

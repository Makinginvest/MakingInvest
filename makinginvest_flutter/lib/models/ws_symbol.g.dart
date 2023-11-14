// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'ws_symbol.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

WSSymbol _$WSSymbolFromJson(Map<String, dynamic> json) => WSSymbol()
  ..symbol = json['s'] as String? ?? ''
  ..price = json['p'] as num? ?? 0;

Map<String, dynamic> _$WSSymbolToJson(WSSymbol instance) => <String, dynamic>{
      's': instance.symbol,
      'p': instance.price,
    };

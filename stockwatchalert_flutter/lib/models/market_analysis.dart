import 'package:flutter/material.dart';
import 'package:json_annotation/json_annotation.dart';

import '../constants/app_colors.dart';
import '_parsers.dart';

part 'market_analysis.g.dart';

@JsonSerializable(explicitToJson: true)
class MarketAnalysis {
  @JsonKey(defaultValue: '', name: '_id')
  String id;
  @JsonKey(defaultValue: [])
  List<MarketAnalysisItem> cryptoSymbolsAnalysis;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? dtUpdated;

  MarketAnalysis()
      : id = '',
        dtUpdated = null,
        cryptoSymbolsAnalysis = [];

  factory MarketAnalysis.fromJson(Map<String, dynamic> json) => _$MarketAnalysisFromJson(json);
  Map<String, dynamic> toJson() => _$MarketAnalysisToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

@JsonSerializable(explicitToJson: true)
class MarketAnalysisItem {
  @JsonKey(defaultValue: '')
  String symbol;
  @JsonKey(defaultValue: [])
  List<MarketAnalysisItemData> data;

  MarketAnalysisItem()
      : symbol = '',
        data = [];

  factory MarketAnalysisItem.fromJson(Map<String, dynamic> json) => _$MarketAnalysisItemFromJson(json);
  Map<String, dynamic> toJson() => _$MarketAnalysisItemToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

@JsonSerializable(explicitToJson: true)
class MarketAnalysisItemData {
  @JsonKey(defaultValue: '')
  String timeframe;
  @JsonKey(defaultValue: '')
  String status;
  @JsonKey(defaultValue: [])
  List<String> statusMessages;

  MarketAnalysisItemData()
      : timeframe = '',
        status = '',
        statusMessages = [];

  factory MarketAnalysisItemData.fromJson(Map<String, dynamic> json) => _$MarketAnalysisItemDataFromJson(json);
  Map<String, dynamic> toJson() => _$MarketAnalysisItemDataToJson(this)
    ..remove('id')
    ..remove('createdDateTime');

  Color get getStatusColor {
    switch (status) {
      case 'Bullish':
        return AppColors.green;
      case 'Bearish':
        return AppColors.red;
      default:
        return AppColors.gray;
    }
  }
}

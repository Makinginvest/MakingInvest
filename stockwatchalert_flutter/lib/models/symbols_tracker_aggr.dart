import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'symbols_tracker_aggr.g.dart';

@JsonSerializable(explicitToJson: true)
class SymbolTrackerAggr {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: [])
  List<SymbolTracker> crypto;
  @JsonKey(defaultValue: [])
  List<SymbolTracker> forex;
  @JsonKey(defaultValue: [])
  List<SymbolTracker> stocks;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? lastUpdatedDateTime;

  SymbolTrackerAggr()
      : id = '',
        crypto = [],
        forex = [],
        stocks = [],
        lastUpdatedDateTime = null;

  factory SymbolTrackerAggr.fromJson(Map<String, dynamic> json) => _$SymbolTrackerAggrFromJson(json);
  Map<String, dynamic> toJson() => _$SymbolTrackerAggrToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

@JsonSerializable(explicitToJson: true)
class SymbolTracker {
  @JsonKey(defaultValue: '')
  String symbol;
  @JsonKey(defaultValue: null)
  num? val1hrAgo;
  @JsonKey(defaultValue: null)
  num? val2hrAgo;
  @JsonKey(defaultValue: null)
  num? val4hrAgo;
  @JsonKey(defaultValue: null)
  num? val8hrAgo;
  @JsonKey(defaultValue: null)
  num? val24hrAgo;
  @JsonKey(defaultValue: null)
  num? val7dAgo;
  @JsonKey(defaultValue: '')
  String market;

  SymbolTracker()
      : symbol = '',
        val1hrAgo = null,
        val2hrAgo = null,
        val4hrAgo = null,
        val8hrAgo = null,
        val24hrAgo = null,
        val7dAgo = null,
        market = '';

  factory SymbolTracker.fromJson(Map<String, dynamic> json) => _$SymbolTrackerFromJson(json);
  Map<String, dynamic> toJson() => _$SymbolTrackerToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

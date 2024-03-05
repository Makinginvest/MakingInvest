import 'package:json_annotation/json_annotation.dart';

part 'market_activity_aggr.g.dart';

@JsonSerializable(explicitToJson: true)
class MarketActivityAggr {
  @JsonKey(defaultValue: '', name: 'id')
  String id;

  @JsonKey(defaultValue: [])
  List<MarketActivity> gainers;
  @JsonKey(defaultValue: [])
  List<MarketActivity> losers;
  @JsonKey(defaultValue: [])
  List<MarketActivity> actives;

  MarketActivityAggr()
      : id = '',
        gainers = [],
        losers = [],
        actives = [];

  factory MarketActivityAggr.fromJson(Map<String, dynamic> json) => _$MarketActivityAggrFromJson(json);
  Map<String, dynamic> toJson() => _$MarketActivityAggrToJson(this)..remove('id');
}

@JsonSerializable(explicitToJson: true)
class MarketActivity {
  @JsonKey(defaultValue: '')
  String symbol;
  @JsonKey(defaultValue: '')
  String name;
  @JsonKey(defaultValue: 0)
  num change;
  @JsonKey(defaultValue: 0)
  num changesPercentage;
  @JsonKey(defaultValue: 0)
  num price;

  MarketActivity()
      : symbol = '',
        name = '',
        change = 0,
        changesPercentage = 0,
        price = 0;

  factory MarketActivity.fromJson(Map<String, dynamic> json) => _$MarketActivityFromJson(json);
  Map<String, dynamic> toJson() => _$MarketActivityToJson(this)..remove('id');

  get isChangePositive => changesPercentage > 0;
}

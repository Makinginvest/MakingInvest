import 'package:json_annotation/json_annotation.dart';

part 'screener_model.g.dart';

@JsonSerializable(explicitToJson: true)
class ScreenerModel {
  @JsonKey(defaultValue: 0)
  num count;
  @JsonKey(defaultValue: [])
  List<ScreenerDataModel> data;

  ScreenerModel()
      : count = 0,
        data = [];

  factory ScreenerModel.fromJson(Map<String, dynamic> json) => _$ScreenerModelFromJson(json);
  Map<String, dynamic> toJson() => _$ScreenerModelToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

@JsonSerializable(explicitToJson: true)
class ScreenerDataModel {
  @JsonKey(defaultValue: 0)
  num close;
  @JsonKey(defaultValue: 0)
  num volume;
  @JsonKey(defaultValue: '')
  String symbol;
  @JsonKey(defaultValue: '')
  String rating;
  @JsonKey(defaultValue: '')
  String ratingRecommendation;
  @JsonKey(defaultValue: '')
  String image;
  @JsonKey(defaultValue: '')
  String exchangeShortName;

  ScreenerDataModel()
      : close = 0,
        volume = 0,
        symbol = '',
        rating = '',
        ratingRecommendation = '',
        image = '',
        exchangeShortName = '';

  factory ScreenerDataModel.fromJson(Map<String, dynamic> json) => _$ScreenerDataModelFromJson(json);
  Map<String, dynamic> toJson() => _$ScreenerDataModelToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

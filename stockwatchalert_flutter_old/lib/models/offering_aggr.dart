import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'offering_aggr.g.dart';

@JsonSerializable(explicitToJson: true)
class OfferingAggr {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: [])
  List<Offering> data;

  OfferingAggr()
      : id = '',
        data = [];

  factory OfferingAggr.fromJson(Map<String, dynamic> json) => _$OfferingAggrFromJson(json);
  Map<String, dynamic> toJson() => _$OfferingAggrToJson(this)
    ..remove('id')
    ..remove('createdDateTime');

  get getTop5Offerings {
    if (data.length > 4) return data.sublist(0, 4);
    return data;
  }
}

@JsonSerializable(explicitToJson: true)
class Offering {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: '')
  String image;
  @JsonKey(defaultValue: '')
  String title;
  @JsonKey(defaultValue: '')
  String link;
  @JsonKey(defaultValue: '')
  String body;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? timestampCreated;

  Offering()
      : id = '',
        image = '',
        title = '',
        link = '',
        body = '',
        timestampCreated = null;

  factory Offering.fromJson(Map<String, dynamic> json) => _$OfferingFromJson(json);
  Map<String, dynamic> toJson() => _$OfferingToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

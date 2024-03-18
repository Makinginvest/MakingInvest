import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'support.g.dart';

@JsonSerializable(explicitToJson: true)
class Support {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: '')
  String name;
  @JsonKey(defaultValue: '')
  String email;
  @JsonKey(defaultValue: '')
  String message;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? createdDateTime;

  Support()
      : id = '',
        name = '',
        email = '',
        message = '',
        createdDateTime = null;

  factory Support.fromJson(Map<String, dynamic> json) => _$SupportFromJson(json);
  Map<String, dynamic> toJson() => _$SupportToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

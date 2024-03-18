import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'notification.g.dart';

@JsonSerializable(explicitToJson: true)
class Notification {
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
  DateTime? createdDateTime;

  Notification()
      : id = '',
        image = '',
        title = '',
        link = '',
        body = '',
        createdDateTime = null;

  factory Notification.fromJson(Map<String, dynamic> json) => _$NotificationFromJson(json);
  Map<String, dynamic> toJson() => _$NotificationToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

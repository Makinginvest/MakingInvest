import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'video_lesson_aggr.g.dart';

@JsonSerializable(explicitToJson: true)
class VideoLessonAggr {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: [])
  List<VideoLesson> data;

  VideoLessonAggr()
      : id = '',
        data = [];

  factory VideoLessonAggr.fromJson(Map<String, dynamic> json) => _$VideoLessonAggrFromJson(json);
  Map<String, dynamic> toJson() => _$VideoLessonAggrToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

@JsonSerializable(explicitToJson: true)
class VideoLesson {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: '')
  String image;
  @JsonKey(defaultValue: '')
  String title;
  @JsonKey(defaultValue: '')
  String link;
  @JsonKey(defaultValue: false)
  bool isFeatured;
  @JsonKey(defaultValue: false)
  bool isPremium;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? timestampCreated;

  VideoLesson()
      : id = '',
        image = '',
        title = '',
        link = '',
        isFeatured = false,
        isPremium = false,
        timestampCreated = null;

  factory VideoLesson.fromJson(Map<String, dynamic> json) => _$VideoLessonFromJson(json);
  Map<String, dynamic> toJson() => _$VideoLessonToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

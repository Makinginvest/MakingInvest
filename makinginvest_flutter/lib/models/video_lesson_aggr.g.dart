// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'video_lesson_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

VideoLessonAggr _$VideoLessonAggrFromJson(Map<String, dynamic> json) =>
    VideoLessonAggr()
      ..id = json['id'] as String? ?? ''
      ..data = (json['data'] as List<dynamic>?)
              ?.map((e) => VideoLesson.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];

Map<String, dynamic> _$VideoLessonAggrToJson(VideoLessonAggr instance) =>
    <String, dynamic>{
      'id': instance.id,
      'data': instance.data.map((e) => e.toJson()).toList(),
    };

VideoLesson _$VideoLessonFromJson(Map<String, dynamic> json) => VideoLesson()
  ..id = json['id'] as String? ?? ''
  ..image = json['image'] as String? ?? ''
  ..title = json['title'] as String? ?? ''
  ..link = json['link'] as String? ?? ''
  ..isFeatured = json['isFeatured'] as bool? ?? false
  ..isPremium = json['isPremium'] as bool? ?? false
  ..timestampCreated = parseToDateTime(json['timestampCreated']);

Map<String, dynamic> _$VideoLessonToJson(VideoLesson instance) =>
    <String, dynamic>{
      'id': instance.id,
      'image': instance.image,
      'title': instance.title,
      'link': instance.link,
      'isFeatured': instance.isFeatured,
      'isPremium': instance.isPremium,
      'timestampCreated': parseToDateTime(instance.timestampCreated),
    };

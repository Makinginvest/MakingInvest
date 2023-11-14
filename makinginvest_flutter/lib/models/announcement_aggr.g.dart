// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'announcement_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

AnnouncementAggr _$AnnouncementAggrFromJson(Map<String, dynamic> json) =>
    AnnouncementAggr()
      ..id = json['id'] as String? ?? ''
      ..data = (json['data'] as List<dynamic>?)
              ?.map((e) => Announcement.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];

Map<String, dynamic> _$AnnouncementAggrToJson(AnnouncementAggr instance) =>
    <String, dynamic>{
      'id': instance.id,
      'data': instance.data.map((e) => e.toJson()).toList(),
    };

Announcement _$AnnouncementFromJson(Map<String, dynamic> json) => Announcement()
  ..id = json['id'] as String? ?? ''
  ..image = json['image'] as String? ?? ''
  ..title = json['title'] as String? ?? ''
  ..link = json['link'] as String? ?? ''
  ..body = json['body'] as String? ?? ''
  ..timestampCreated = parseToDateTime(json['timestampCreated']);

Map<String, dynamic> _$AnnouncementToJson(Announcement instance) =>
    <String, dynamic>{
      'id': instance.id,
      'image': instance.image,
      'title': instance.title,
      'link': instance.link,
      'body': instance.body,
      'timestampCreated': parseToDateTime(instance.timestampCreated),
    };

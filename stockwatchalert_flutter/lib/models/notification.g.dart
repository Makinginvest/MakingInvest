// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'notification.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Notification _$NotificationFromJson(Map<String, dynamic> json) => Notification()
  ..id = json['id'] as String? ?? ''
  ..image = json['image'] as String? ?? ''
  ..title = json['title'] as String? ?? ''
  ..link = json['link'] as String? ?? ''
  ..body = json['body'] as String? ?? ''
  ..createdDateTime = parseToDateTime(json['createdDateTime']);

Map<String, dynamic> _$NotificationToJson(Notification instance) =>
    <String, dynamic>{
      'id': instance.id,
      'image': instance.image,
      'title': instance.title,
      'link': instance.link,
      'body': instance.body,
      'createdDateTime': parseToDateTime(instance.createdDateTime),
    };

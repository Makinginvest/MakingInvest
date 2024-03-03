// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'post_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

PostAggr _$PostAggrFromJson(Map<String, dynamic> json) => PostAggr()
  ..id = json['id'] as String? ?? ''
  ..data = (json['data'] as List<dynamic>?)
          ?.map((e) => Post.fromJson(e as Map<String, dynamic>))
          .toList() ??
      [];

Map<String, dynamic> _$PostAggrToJson(PostAggr instance) => <String, dynamic>{
      'id': instance.id,
      'data': instance.data.map((e) => e.toJson()).toList(),
    };

Post _$PostFromJson(Map<String, dynamic> json) => Post()
  ..id = json['id'] as String? ?? ''
  ..image = json['image'] as String? ?? ''
  ..title = json['title'] as String? ?? ''
  ..body = json['body'] as String? ?? ''
  ..isFeatured = json['isFeatured'] as bool? ?? false
  ..isPremium = json['isPremium'] as bool? ?? false
  ..postDate = parseToDateTime(json['postDate'])
  ..createdDateTime = parseToDateTime(json['createdDateTime']);

Map<String, dynamic> _$PostToJson(Post instance) => <String, dynamic>{
      'id': instance.id,
      'image': instance.image,
      'title': instance.title,
      'body': instance.body,
      'isFeatured': instance.isFeatured,
      'isPremium': instance.isPremium,
      'postDate': parseToDateTime(instance.postDate),
      'createdDateTime': parseToDateTime(instance.createdDateTime),
    };

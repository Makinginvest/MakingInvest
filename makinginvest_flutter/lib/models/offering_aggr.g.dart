// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'offering_aggr.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

OfferingAggr _$OfferingAggrFromJson(Map<String, dynamic> json) => OfferingAggr()
  ..id = json['id'] as String? ?? ''
  ..data = (json['data'] as List<dynamic>?)
          ?.map((e) => Offering.fromJson(e as Map<String, dynamic>))
          .toList() ??
      [];

Map<String, dynamic> _$OfferingAggrToJson(OfferingAggr instance) =>
    <String, dynamic>{
      'id': instance.id,
      'data': instance.data.map((e) => e.toJson()).toList(),
    };

Offering _$OfferingFromJson(Map<String, dynamic> json) => Offering()
  ..id = json['id'] as String? ?? ''
  ..image = json['image'] as String? ?? ''
  ..title = json['title'] as String? ?? ''
  ..link = json['link'] as String? ?? ''
  ..body = json['body'] as String? ?? ''
  ..timestampCreated = parseToDateTime(json['timestampCreated']);

Map<String, dynamic> _$OfferingToJson(Offering instance) => <String, dynamic>{
      'id': instance.id,
      'image': instance.image,
      'title': instance.title,
      'link': instance.link,
      'body': instance.body,
      'timestampCreated': parseToDateTime(instance.timestampCreated),
    };

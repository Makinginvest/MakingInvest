// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'news_wordpress.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

NewsWordpress _$NewsWordpressFromJson(Map<String, dynamic> json) =>
    NewsWordpress()
      ..image = json['image'] as String? ?? ''
      ..site = json['site'] as String? ?? ''
      ..title = json['title'] as String? ?? ''
      ..symbol = json['symbol'] as String? ?? ''
      ..text = json['text'] as String? ?? ''
      ..dateString = json['dateString'] as String? ?? ''
      ..url = json['url'] as String? ?? ''
      ..publishedDate = parseToDateTime(json['publishedDate']);

Map<String, dynamic> _$NewsWordpressToJson(NewsWordpress instance) =>
    <String, dynamic>{
      'image': instance.image,
      'site': instance.site,
      'title': instance.title,
      'symbol': instance.symbol,
      'text': instance.text,
      'dateString': instance.dateString,
      'url': instance.url,
      'publishedDate': parseToDateTime(instance.publishedDate),
    };

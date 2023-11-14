import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'news_wordpress.g.dart';

@JsonSerializable(explicitToJson: true)
class NewsWordpress {
  @JsonKey(defaultValue: '')
  String image;
  @JsonKey(defaultValue: '')
  String site;
  @JsonKey(defaultValue: '')
  String title;
  @JsonKey(defaultValue: '')
  String symbol;
  @JsonKey(defaultValue: '')
  String text;
  @JsonKey(defaultValue: '')
  String dateString;
  @JsonKey(defaultValue: '', name: 'url')
  String url;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, name: 'publishedDate')
  DateTime? publishedDate;

  NewsWordpress()
      : image = '',
        site = '',
        symbol = '',
        text = '',
        title = '',
        url = '',
        dateString = '',
        publishedDate = null;

  factory NewsWordpress.fromJson(Map<String, dynamic> json) => _$NewsWordpressFromJson(json);
  Map<String, dynamic> toJson() => _$NewsWordpressToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

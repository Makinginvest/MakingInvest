import 'package:json_annotation/json_annotation.dart';

import '_parsers.dart';

part 'post_aggr.g.dart';

@JsonSerializable(explicitToJson: true)
class PostAggr {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: [])
  List<Post> data;

  PostAggr()
      : id = '',
        data = [];

  factory PostAggr.fromJson(Map<String, dynamic> json) => _$PostAggrFromJson(json);
  Map<String, dynamic> toJson() => _$PostAggrToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

@JsonSerializable(explicitToJson: true)
class Post {
  @JsonKey(defaultValue: '')
  String id;
  @JsonKey(defaultValue: '')
  String image;
  @JsonKey(defaultValue: '')
  String title;
  @JsonKey(defaultValue: '')
  String body;
  @JsonKey(defaultValue: false)
  bool isFeatured;
  @JsonKey(defaultValue: false)
  bool isPremium;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? postDate;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? createdDateTime;

  Post()
      : id = '',
        image = '',
        title = '',
        body = '',
        isFeatured = false,
        isPremium = false,
        postDate = null,
        createdDateTime = null;

  factory Post.fromJson(Map<String, dynamic> json) => _$PostFromJson(json);
  Map<String, dynamic> toJson() => _$PostToJson(this)
    ..remove('id')
    ..remove('createdDateTime');
}

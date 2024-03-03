import 'package:json_annotation/json_annotation.dart';

part 'ws_symbol.g.dart';

@JsonSerializable(explicitToJson: true)
class WSSymbol {
  @JsonKey(defaultValue: '', name: 's')
  String symbol;
  @JsonKey(defaultValue: 0, name: 'p')
  num price;

  WSSymbol()
      : symbol = '',
        price = 0;

  factory WSSymbol.fromJson(Map<String, dynamic> json) => _$WSSymbolFromJson(json);
  Map<String, dynamic> toJson() => _$WSSymbolToJson(this)..remove('id');
}

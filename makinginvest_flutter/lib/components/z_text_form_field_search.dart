import 'package:flutter/material.dart';

import '../constants/app_colors.dart';
import '../constants/app_sizes.dart';
import 'z_card.dart';

typedef Null ValueChangeCallback(String value);

class ZSearch extends StatefulWidget {
  final ValueChangeCallback? onValueChanged;
  final TextEditingController? controller;
  final String? initialValue;
  final EdgeInsets? margin;
  final EdgeInsets? padding;
  final String? labelText;
  final Widget? prefix;
  final bool filled;
  final double? height;
  ZSearch({Key? key, this.onValueChanged, this.controller, this.initialValue, this.margin, this.padding, this.labelText, this.prefix, this.filled = false, this.height})
      : super(key: key);

  @override
  State<ZSearch> createState() => _ZSearchState();
}

class _ZSearchState extends State<ZSearch> {
  TextEditingController? valueController;
  FocusNode _focus = new FocusNode();

  @override
  void initState() {
    super.initState();
    valueController = widget.controller ?? TextEditingController.fromValue(TextEditingValue(text: widget.initialValue ?? ""));
    valueController?.addListener(() {
      if (widget.onValueChanged != null) widget.onValueChanged!(valueController?.text ?? '');
      setState(() {});
    });
    _focus.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    BorderRadius borderRadius = BorderRadius.circular(AppSIZES.textFormFieldRadius);

    Color disabledBorderColor = isLightTheme ? Color(0xFFE6E7EA) : Color(0xFFE6E7EA);
    Color enabledBorderColor = isLightTheme ? Colors.black12 : Colors.white10;
    Color errorBorderColor = isLightTheme ? Color(0xFFE20000) : Color(0xFFE20000);
    Color focusedBorderColor = isLightTheme ? AppCOLORS.green : AppCOLORS.green;
    Color focusedErrorBorderColor = isLightTheme ? AppCOLORS.red : AppCOLORS.red;

    return Container(
      padding: widget.padding ?? EdgeInsets.symmetric(horizontal: 0, vertical: 0),
      margin: widget.margin ?? EdgeInsets.symmetric(horizontal: 0, vertical: 6),
      height: widget.height,
      child: TextField(
        onChanged: (v) {
          if (widget.onValueChanged != null) widget.onValueChanged!(v);
        },
        style: TextStyle(fontSize: 13, fontWeight: FontWeight.w500, height: 1.45),
        cursorColor: AppCOLORS.green,
        cursorHeight: 13,
        controller: valueController,
        decoration: InputDecoration(
            border: OutlineInputBorder(borderSide: BorderSide(color: enabledBorderColor, width: 1), borderRadius: borderRadius),
            labelText: widget.labelText,
            prefixIcon: SizedBox.shrink(child: widget.prefix ?? Icon(Icons.search)),
            suffixIcon: valueController?.text != '' ? _buildClose(context) : null,
            prefixStyle: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
            fillColor: AppCOLORS.green.withOpacity(.3),
            filled: widget.filled,
            suffixStyle: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
            labelStyle: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
            contentPadding: EdgeInsets.symmetric(horizontal: 14, vertical: 14),
            enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: enabledBorderColor, width: 1), borderRadius: borderRadius),
            focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: focusedBorderColor, width: 1), borderRadius: borderRadius),
            errorBorder: OutlineInputBorder(borderSide: BorderSide(color: errorBorderColor, width: 1), borderRadius: borderRadius),
            focusedErrorBorder: OutlineInputBorder(borderSide: BorderSide(color: focusedErrorBorderColor, width: 1), borderRadius: borderRadius),
            disabledBorder: OutlineInputBorder(borderSide: BorderSide(color: disabledBorderColor, width: 1), borderRadius: borderRadius),
            isDense: true),
      ),
    );
  }

  _buildClose(BuildContext context) {
    return ZCard(
      child: Icon(Icons.close, color: Colors.grey.shade400, size: 20),
      margin: EdgeInsets.zero,
      padding: EdgeInsets.all(0),
      borderRadiusColor: Colors.transparent,
      color: Colors.transparent,
      borderWidth: 0,
      onTap: () {
        valueController?.text = '';
        if (widget.onValueChanged != null) widget.onValueChanged!('');
        FocusScope.of(context).requestFocus(new FocusNode());
      },
    );
  }
}

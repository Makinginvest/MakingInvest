import 'package:flutter/material.dart';

import '../constants/app_colors.dart';
import '../constants/app_sizes.dart';

typedef Null ValueChangeCallback(String value);
typedef Null OnSavedChangeCallback(String value);
typedef Null OnEditingComplete();

class ZTextFormField extends StatefulWidget {
  final AutovalidateMode? autovalidateMode;
  final Color? containerColor;
  final GestureTapCallback? onTap;
  final String? initialValue;
  final String? labelText;
  final String? Function(String?)? validator;
  final TextCapitalization? textCapitalization;
  final TextEditingController? controller;
  final TextInputType? keyboardType;
  final ValueChangeCallback onSaved;
  final ValueChangeCallback? onValueChanged;
  final OnEditingComplete? onEditingComplete;
  final ValueChangeCallback? onFieldSubmitted;
  final Widget? suffix;
  final bool isDarkMode;
  final bool isEnabled;
  final bool? obscureText;
  final bool readyOnly;
  final int? maxLength;
  final int? maxLines;
  final Widget? prefix;
  final bool autocorrect;
  final bool filled;
  final double? height;
  final EdgeInsets? margin;
  final EdgeInsets? padding;

  ZTextFormField(
      {Key? key,
      this.labelText,
      this.controller,
      this.onValueChanged,
      this.isEnabled = true,
      required this.onSaved,
      this.onEditingComplete,
      this.keyboardType,
      this.textCapitalization,
      this.validator,
      this.containerColor,
      this.initialValue,
      this.obscureText,
      this.maxLength,
      this.maxLines,
      this.readyOnly = false,
      this.onTap,
      this.suffix,
      this.isDarkMode = false,
      this.autovalidateMode,
      this.prefix,
      this.margin,
      this.autocorrect = false,
      this.filled = false,
      this.onFieldSubmitted,
      this.height,
      this.padding})
      : super(key: key);

  @override
  _ZTextFormFieldState createState() => _ZTextFormFieldState();
}

class _ZTextFormFieldState extends State<ZTextFormField> {
  TextEditingController? valueController;
  FocusNode _focus = new FocusNode();

  @override
  void initState() {
    super.initState();
    valueController = widget.controller ?? TextEditingController.fromValue(TextEditingValue(text: widget.initialValue ?? ""));
    valueController?.addListener(() {
      if (widget.onValueChanged != null) widget.onValueChanged!(valueController?.text ?? '');
    });
    _focus.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    BorderRadius borderRadius = BorderRadius.circular(AppSizes.textFormFieldRadius);

    Color disabledBorderColor = isLightTheme ? Color(0xFFE6E7EA) : Color(0xFFE6E7EA);
    Color enabledBorderColor = isLightTheme ? Colors.black12 : Colors.white10;
    Color errorBorderColor = isLightTheme ? Color(0xFFE20000) : Color(0xFFE20000);
    Color focusedBorderColor = isLightTheme ? AppColors.green : AppColors.green;
    Color focusedErrorBorderColor = isLightTheme ? AppColors.red : AppColors.red;

    return Container(
      padding: widget.padding ?? EdgeInsets.symmetric(horizontal: 0, vertical: 0),
      margin: widget.margin ?? EdgeInsets.symmetric(horizontal: 0, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextFormField(
            autocorrect: widget.autocorrect,
            autovalidateMode: widget.autovalidateMode ?? AutovalidateMode.disabled,
            maxLength: widget.maxLength ?? null,
            maxLines: widget.maxLines ?? 1,
            enabled: widget.isEnabled,
            readOnly: widget.readyOnly,
            focusNode: _focus,
            onTap: () {
              if (widget.onTap != null) widget.onTap!();
            },
            onSaved: (String? value) {
              widget.onSaved(value ?? '');
            },
            onEditingComplete: () {
              if (widget.onEditingComplete != null) widget.onEditingComplete!();
            },
            onFieldSubmitted: (v) {
              if (widget.onFieldSubmitted != null) widget.onFieldSubmitted!(v);
            },
            onChanged: (v) {
              if (widget.onValueChanged != null) widget.onValueChanged!(v);
            },
            style: TextStyle(fontSize: 13, fontWeight: FontWeight.w500, height: 1.45),
            keyboardType: widget.keyboardType ?? TextInputType.text,
            textCapitalization: widget.textCapitalization ?? TextCapitalization.none,
            obscureText: widget.obscureText ?? false,
            controller: valueController,
            cursorColor: AppColors.green,
            cursorHeight: 13,
            validator: widget.validator ??
                (String? value) {
                  if (value != null && value.isEmpty) return 'This field is required';
                  return null;
                },
            decoration: InputDecoration(
              labelText: widget.labelText,
              prefixIcon: widget.prefix ?? null,
              prefixStyle: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
              fillColor: Colors.black12,
              filled: widget.filled,
              suffixStyle: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
              labelStyle: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
              contentPadding: EdgeInsets.symmetric(horizontal: 14, vertical: 15),
              enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: enabledBorderColor, width: 1), borderRadius: borderRadius),
              focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: focusedBorderColor, width: 1), borderRadius: borderRadius),
              errorBorder: OutlineInputBorder(borderSide: BorderSide(color: errorBorderColor, width: 1), borderRadius: borderRadius),
              focusedErrorBorder: OutlineInputBorder(borderSide: BorderSide(color: focusedErrorBorderColor, width: 1), borderRadius: borderRadius),
              disabledBorder: OutlineInputBorder(borderSide: BorderSide(color: disabledBorderColor, width: 1), borderRadius: borderRadius),
              isDense: true,
            ),
          ),
        ],
      ),
    );
  }
}

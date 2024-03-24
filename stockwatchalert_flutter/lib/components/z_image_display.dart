import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:shimmer/shimmer.dart';

class ZImageDisplay extends StatelessWidget {
  const ZImageDisplay({
    Key? key,
    required this.image,
    this.height,
    this.width,
    this.borderRadius,
    this.margin = EdgeInsets.zero,
  }) : super(key: key);
  final String image;
  final double? height;
  final double? width;
  final BorderRadius? borderRadius;
  final EdgeInsets margin;

  @override
  Widget build(BuildContext context) {
    // Determine the theme brightness
    final isLight = Theme.of(context).brightness == Brightness.light;

    // Define color schemes based on the theme
    final baseColor = isLight ? Colors.grey.shade200 : Colors.grey.shade800;
    final highlightColor = isLight ? Colors.grey.shade300 : Colors.grey.shade700;
    final containerColor = isLight ? Colors.grey.shade100 : Colors.grey.shade600;

    return Container(
      decoration: BoxDecoration(color: containerColor, borderRadius: borderRadius),
      margin: margin,
      child: ClipRRect(
        borderRadius: borderRadius ?? BorderRadius.zero,
        child: _buildImageContent(baseColor, highlightColor),
      ),
    );
  }

  Widget _buildImageContent(Color baseColor, Color highlightColor) {
    if (image.isEmpty) return _buildPlaceholder();

    return CachedNetworkImage(
      imageUrl: image,
      fit: BoxFit.cover,
      width: width ?? double.infinity,
      height: height ?? double.infinity,
      fadeInCurve: Curves.easeIn,
      fadeInDuration: const Duration(milliseconds: 600),
      errorListener: (value) {},
      placeholder: (_, __) => Shimmer.fromColors(
        baseColor: baseColor,
        highlightColor: highlightColor,
        child: Container(color: Colors.white),
      ),
      errorWidget: (_, __, ___) => _buildErrorWidget(),
    );
  }

  Widget _buildPlaceholder() {
    return Container(
      alignment: Alignment.center,
      color: Colors.grey[300],
      width: width ?? double.infinity,
      height: height ?? double.infinity,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Icon(AntDesign.picture, size: 20, color: Colors.black26),
          SizedBox(height: 2),
        ],
      ),
    );
  }

  Widget _buildErrorWidget() {
    return Container(
      width: width ?? double.infinity,
      height: height ?? double.infinity,
      alignment: Alignment.center,
      color: Colors.grey[300],
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Icon(AntDesign.picture, size: 20, color: Colors.black26),
          SizedBox(height: 2),
        ],
      ),
    );
  }
}

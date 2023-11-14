import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../../components/z_image_display.dart';
import '../../constants/app_colors.dart';
import '../models/post_aggr.dart';
import '../pages/learn/post_details_page.dart';
import '../utils/z_format.dart';
import 'z_card.dart';

class ZPostCard extends StatelessWidget {
  const ZPostCard({Key? key, required this.post}) : super(key: key);
  final Post post;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      borderRadiusColor: isLightTheme ? AppCOLORS.cardBorderLight : AppCOLORS.cardBorderDark,
      onTap: () => Get.to(() => PostDetailsPage(post: post), transition: Transition.cupertino, fullscreenDialog: true),
      margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      padding: EdgeInsets.symmetric(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(),
          Hero(
            tag: post.id,
            child: ZImageDisplay(
              image: post.image,
              height: 140,
              width: MediaQuery.of(context).size.width,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(8),
                topRight: Radius.circular(8),
              ),
            ),
          ),
          SizedBox(height: 8),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 8),
            child: Text(post.title),
          ),
          SizedBox(height: 4),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 8),
            child: Text(ZFormat.dateFormatSignal(post.postDate), style: TextStyle(fontSize: 12)),
          ),
          SizedBox(height: 8),
        ],
      ),
    );
  }
}

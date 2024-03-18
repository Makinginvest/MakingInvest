import 'package:flutter/material.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/models/video_lesson_aggr.dart';
import 'package:stockwatchalert/utils/z_format.dart';

import '../../components/z_image_display.dart';
import '../../constants/app_colors.dart';
import '../../utils/z_launch_url.dart';

class ZVideoCard extends StatelessWidget {
  const ZVideoCard({Key? key, required this.videoLesson}) : super(key: key);
  final VideoLesson videoLesson;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      onTap: () => ZLaunchUrl.launchUrl(videoLesson.link),
      margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      padding: EdgeInsets.symmetric(),
      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(),
          ZImageDisplay(
            image: videoLesson.image,
            height: MediaQuery.of(context).size.width * .4,
            width: MediaQuery.of(context).size.width,
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(8),
              topRight: Radius.circular(8),
            ),
          ),
          SizedBox(height: 8),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 8),
            child: Text(videoLesson.title),
          ),
          SizedBox(height: 4),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 8),
            child: Text(ZFormat.dateFormatSignal(videoLesson.timestampCreated), style: TextStyle(fontSize: 12)),
          ),
          SizedBox(height: 8),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/components/z_image_display.dart';
import 'package:stockwatchalert/models/announcement_aggr.dart';

import '../constants/app_colors.dart';
import '../utils/z_format.dart';

class ZAnnoucementCard extends StatelessWidget {
  const ZAnnoucementCard({Key? key, required this.announcement}) : super(key: key);
  final Announcement announcement;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
        padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
        borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '${ZFormat.dateFormatSignal(announcement.timestampCreated)}',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 11),
                  ),
                  SizedBox(height: 4),
                  Text(announcement.title),
                  SizedBox(height: 4),
                  Text(
                    announcement.body,
                    style: TextStyle(fontSize: 12, color: Theme.of(context).textTheme.bodySmall!.color),
                  ),
                ],
              ),
            ),
            if (announcement.image != '')
              Container(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ZImageDisplay(
                      image: announcement.image,
                      width: MediaQuery.of(context).size.width * .125,
                      height: MediaQuery.of(context).size.width * .125,
                      borderRadius: BorderRadius.circular(8),
                    )
                  ],
                ),
              ),
          ],
        ));
  }
}

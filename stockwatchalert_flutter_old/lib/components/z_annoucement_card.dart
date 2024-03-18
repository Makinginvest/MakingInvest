import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../utils/z_launch_url.dart';

import '../constants/app_colors.dart';
import '../models/announcement_aggr.dart';
import '../pages/announcement/annoucement_detail_page.dart';
import '../utils/z_format.dart';
import 'z_card.dart';
import 'z_image_display.dart';

class ZAnnoucementCard extends StatelessWidget {
  const ZAnnoucementCard({Key? key, required this.announcement}) : super(key: key);
  final Announcement announcement;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
        onTap: () => announcement.link != '' ? ZLaunchUrl.launchUrl(announcement.link) : null,
        padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
        borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
        child: Row(
          children: [
            if (announcement.image != '')
              Container(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ZImageDisplay(
                      image: announcement.image,
                      width: MediaQuery.of(context).size.width * .125,
                      height: MediaQuery.of(context).size.width * .125,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    SizedBox(width: 8),
                  ],
                ),
              ),
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
                    announcement.getBodyPreview(),
                    style: TextStyle(fontSize: 12, color: Theme.of(context).textTheme.bodySmall!.color),
                  ),
                  if (announcement.body.length > 400)
                    Row(
                      children: [
                        Spacer(),
                        ZCard(
                          margin: EdgeInsets.symmetric(vertical: 8),
                          padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                          child: Text('More...'),
                          onTap: () => Get.to(() => AnnouncememtDetailsPage(announcement: announcement)),
                        ),
                      ],
                    ),
                ],
              ),
            ),
          ],
        ));
  }
}

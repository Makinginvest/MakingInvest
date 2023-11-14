import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../constants/app_colors.dart';
import '../models/news_aggr.dart';
import '../pages/_app/render_html_url_page.dart';
import '../utils/z_format.dart';
import 'z_card.dart';
import 'z_image_display.dart';

class ZNewsCard extends StatelessWidget {
  const ZNewsCard({Key? key, required this.news}) : super(key: key);
  final News news;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return Container(
      child: ZCard(
          margin: EdgeInsets.symmetric(vertical: 6, horizontal: 16),
          padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
          borderRadiusColor: isLightTheme ? AppCOLORS.cardBorderLight : AppCOLORS.cardBorderDark,
          onTap: () {
            Get.to(() => RenderHTMLUrlPage(url: news.url), fullscreenDialog: true);
          },
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(news.site.toUpperCase()),
                  Text(
                    '${ZFormat.dateFormatSignal(news.publishedDate)}',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 11),
                  ),
                ],
              ),
              SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    width: MediaQuery.of(context).size.width * 0.625,
                    child: Text(
                      news.text,
                      maxLines: 4,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(fontSize: 13),
                    ),
                  ),
                  ZImageDisplay(
                    image: news.image,
                    width: MediaQuery.of(context).size.width * .125,
                    height: MediaQuery.of(context).size.width * .125,
                    borderRadius: BorderRadius.circular(8),
                  )
                ],
              ),
            ],
          )),
    );
  }
}

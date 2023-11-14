import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../models/news_wordpress.dart';
import '../pages/_app/render_html_url_page.dart';
import 'z_card.dart';
import 'z_image_display.dart';

class ZNewsWordpressCard extends StatelessWidget {
  const ZNewsWordpressCard({Key? key, required this.news}) : super(key: key);
  final NewsWordpress news;

  @override
  Widget build(BuildContext context) {
    return Container(
      child: ZCard(
          margin: EdgeInsets.symmetric(vertical: 6, horizontal: 16),
          padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
          // onTap: () => ZLaunchUrl.launchUrl(news.url),
          onTap: () => Get.to(() => RenderHTMLUrlPage(url: news.url)),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(news.dateString),
              Text(news.title),
              // Text(
              //   '${ZFormat.dateFormatSignal(news.publishedDate)}',
              //   style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 11),
              // ),

              SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    width: MediaQuery.of(context).size.width * 0.625,
                    child: Text(
                      news.text,
                      maxLines: 3,
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

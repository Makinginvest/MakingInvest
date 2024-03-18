import 'package:flutter/material.dart';

import '../../components/z_image_display.dart';
import '../../models/announcement_aggr.dart';

class AnnouncememtDetailsPage extends StatefulWidget {
  const AnnouncememtDetailsPage({super.key, required this.announcement});
  final Announcement announcement;

  @override
  State<AnnouncememtDetailsPage> createState() => _AnnouncememtDetailsPageState();
}

class _AnnouncememtDetailsPageState extends State<AnnouncememtDetailsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Announcement Details'),
        ),
        body: ListView(
          padding: EdgeInsets.all(16),
          children: [
            if (widget.announcement.image != '')
              Container(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ZImageDisplay(
                      image: widget.announcement.image,
                      width: MediaQuery.of(context).size.width,
                      height: MediaQuery.of(context).size.height * .25,
                      borderRadius: BorderRadius.circular(16),
                    )
                  ],
                ),
              ),
            SizedBox(height: 16),
            Text(widget.announcement.title),
            SizedBox(height: 16),
            Text(widget.announcement.body),
          ],
        ));
  }
}

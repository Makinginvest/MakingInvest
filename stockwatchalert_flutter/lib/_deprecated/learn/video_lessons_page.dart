import 'package:flutter/material.dart';

import '../../components/z_video_card.dart';
import '../../models/video_lesson_aggr.dart';

class VideoLessonsPage extends StatefulWidget {
  final List<VideoLesson> videos;
  VideoLessonsPage({Key? key, required this.videos}) : super(key: key);

  @override
  State<VideoLessonsPage> createState() => _VideoLessonsPageState();
}

class _VideoLessonsPageState extends State<VideoLessonsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Videos'),
      ),
      body: ListView.builder(
        shrinkWrap: true,
        physics: ClampingScrollPhysics(),
        itemCount: widget.videos.length,
        itemBuilder: ((context, index) => Column(
              children: [
                if (index == 0) SizedBox(height: 8),
                ZVideoCard(videoLesson: (widget.videos[index])),
                if (index == widget.videos.length - 1) SizedBox(height: 8),
              ],
            )),
      ),
    );
  }
}

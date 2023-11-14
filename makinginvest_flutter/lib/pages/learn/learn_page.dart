import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../components/z_card.dart';
import '../../components/z_post_card.dart';
import '../../components/z_video_card.dart';
import '../../models/post_aggr.dart';
import '../../models/video_lesson_aggr.dart';
import '../../models_providers/app_provider.dart';

class LearnPage extends StatefulWidget {
  const LearnPage({Key? key}) : super(key: key);

  @override
  State<LearnPage> createState() => _LearnPageState();
}

class _LearnPageState extends State<LearnPage> {
  String selectedPage = 'guide';

  @override
  Widget build(BuildContext context) {
    AppProvider appProvider = Provider.of<AppProvider>(context);

    // final posts = appProvider.posts.length > 4 ? appProvider.posts.sublist(0, 4) : appProvider.posts;
    // final videoLessons = appProvider.videoLessons.length > 4 ? appProvider.videoLessons.sublist(0, 4) : appProvider.videoLessons;
    final posts = appProvider.posts;
    final videoLessons = appProvider.videoLessons;

    return Scaffold(
      appBar: AppBar(title: Text('Learn')),
      body: Column(
        children: [
          SizedBox(height: 16),
          Row(
            children: [
              ZCard(
                margin: EdgeInsets.symmetric(horizontal: 16),
                borderRadius: BorderRadius.circular(12),
                child: Text('Guides', style: TextStyle(color: selectedPage == 'guide' ? Colors.black : Colors.white)),
                onTap: () => setState(() => selectedPage = 'guide'),
                color: selectedPage == 'guide' ? Colors.white : Colors.white30,
              ),
              ZCard(
                margin: EdgeInsets.symmetric(),
                borderRadius: BorderRadius.circular(12),
                child: Text('Videos', style: TextStyle(color: selectedPage == 'videos' ? Colors.black : Colors.white)),
                color: selectedPage == 'videos' ? Colors.white : Colors.white30,
                onTap: () => setState(() => selectedPage = 'videos'),
              ),
            ],
          ),
          Expanded(
            child: AnimatedSwitcher(
              transitionBuilder: (Widget child, Animation<double> animation) {
                return FadeTransition(child: child, opacity: animation);
              },
              duration: Duration(milliseconds: 300),
              child: selectedPage == 'guide' ? DisplayPosts(posts: posts) : DisplayVideos(videos: videoLessons),
            ),
          )
        ],
      ),
    );
  }
}

class DisplayPosts extends StatefulWidget {
  const DisplayPosts({Key? key, required this.posts}) : super(key: key);
  final List<Post> posts;

  @override
  State<DisplayPosts> createState() => _DisplayPostsState();
}

class _DisplayPostsState extends State<DisplayPosts> {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics: ClampingScrollPhysics(),
      itemCount: widget.posts.length,
      itemBuilder: ((context, index) => Column(
            children: [
              if (index == 0) SizedBox(height: 8),
              ZPostCard(post: (widget.posts[index])),
              if (index == widget.posts.length - 1) SizedBox(height: 8),
            ],
          )),
    );
  }
}

class DisplayVideos extends StatefulWidget {
  final List<VideoLesson> videos;
  DisplayVideos({Key? key, required this.videos}) : super(key: key);

  @override
  State<DisplayVideos> createState() => _DisplayVideosState();
}

class _DisplayVideosState extends State<DisplayVideos> {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
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
    );
  }
}

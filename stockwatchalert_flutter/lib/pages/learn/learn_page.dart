import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_button.dart';
import 'package:stockwatchalert/constants/app_colors.dart';
import 'package:stockwatchalert/models/post_aggr.dart';
import 'package:stockwatchalert/models/video_lesson_aggr.dart';
import 'package:stockwatchalert/models_providers/app_provider.dart';
import 'package:stockwatchalert/pages/learn/posts_page.dart';
import 'package:stockwatchalert/pages/learn/video_lessons_page.dart';

import '../../components/z_post_card.dart';
import '../../components/z_video_card.dart';

class LearnPage extends StatefulWidget {
  const LearnPage({Key? key}) : super(key: key);

  @override
  State<LearnPage> createState() => _LearnPageState();
}

class _LearnPageState extends State<LearnPage> {
  @override
  Widget build(BuildContext context) {
    AppProvider appProvider = Provider.of<AppProvider>(context);

    final posts = appProvider.posts.length > 4 ? appProvider.posts.sublist(0, 4) : appProvider.posts;
    final videoLessons = appProvider.videoLessons.length > 4 ? appProvider.videoLessons.sublist(0, 4) : appProvider.videoLessons;

    return Scaffold(
      appBar: AppBar(
        title: Text('Learn'),
      ),
      body: ListView(
        shrinkWrap: true,
        children: [
          _buildHeading(
            title: 'Blogs',
            onTap: () => Get.to(() => PostsPage(posts: posts), fullscreenDialog: true),
            showViewAll: posts.length > 4,
          ),
          DisplayPosts(posts: posts),
          _buildHeading(title: 'Videos', onTap: () => Get.to(() => VideoLessonsPage(videos: videoLessons), fullscreenDialog: true), showViewAll: videoLessons.length > 4),
          DisplayVideos(videos: videoLessons),
        ],
      ),
    );
  }

  Container _buildHeading({required String title, required Function() onTap, showViewAll = true}) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 1, horizontal: 16),
      child: Row(
        children: [
          Text(
            title,
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.yellow),
          ),
          Spacer(),
          if (showViewAll)
            ZButton(
              margin: EdgeInsets.zero,
              height: 30,
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              text: 'View all',
              textStyle: TextStyle(fontSize: 14),
              onTap: onTap,
            ),
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

import 'package:flutter/material.dart';

import '../../components/z_post_card.dart';
import '../../models/post_aggr.dart';

class PostsPage extends StatefulWidget {
  const PostsPage({Key? key, required this.posts}) : super(key: key);
  final List<Post> posts;

  @override
  State<PostsPage> createState() => _PostsPageState();
}

class _PostsPageState extends State<PostsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Blogs'),
      ),
      body: ListView.builder(
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
      ),
    );
  }
}

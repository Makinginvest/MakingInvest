import 'package:flutter/material.dart';

import '../components/z_news_wordpress_card.dart';
import '../models/news_wordpress.dart';

class NewsWordpressPage extends StatefulWidget {
  final List<NewsWordpress> news;
  NewsWordpressPage({Key? key, required this.news}) : super(key: key);

  @override
  State<NewsWordpressPage> createState() => _NewsWordpressPageState();
}

class _NewsWordpressPageState extends State<NewsWordpressPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('News'),
      ),
      body: ListView.builder(
        shrinkWrap: true,
        physics: ClampingScrollPhysics(),
        itemCount: widget.news.length,
        itemBuilder: ((context, index) => Column(
              children: [
                if (index == 0) SizedBox(height: 8),
                ZNewsWordpressCard(news: (widget.news[index])),
                if (index == widget.news.length - 1) SizedBox(height: 8),
              ],
            )),
      ),
    );
  }
}

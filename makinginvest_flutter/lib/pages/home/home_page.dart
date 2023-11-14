import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';

import '../../components/z_annoucement_card.dart';
import '../../components/z_card.dart';
import '../../components/z_news_card.dart';
import '../../components/z_news_wordpress_card.dart';
import '../../constants/app_colors.dart';
import '../../models/announcement_aggr.dart';
import '../../models/news_aggr.dart';
import '../../models/news_wordpress.dart';
import '../../models_providers/app_provider.dart';
import 'annoucement_page.dart';
import 'news_wordpress_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  void initState() {
    Provider.of<AppProvider>(context, listen: false).getNewsWordpress();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    AppProvider appProvider = Provider.of<AppProvider>(context);
    final annoucements = appProvider.announcementAggr.getTop5Announcements;
    final newsWordpress = appProvider.newsWordpress.length > 4 ? appProvider.newsWordpress.sublist(0, 4) : appProvider.newsWordpress;

    return Scaffold(
      appBar: AppBar(title: Text('Home')),
      body: ListView(
        shrinkWrap: true,
        children: [
          SizedBox(height: 16),
          _buildHeading(title: 'Announcements', onTap: () => Get.to(() => AnnoucementsPage(annoucements: annoucements), fullscreenDialog: true)),
          DisplayAnnoucement(annoucements: annoucements),
          _buildHeading(title: 'News', onTap: () => Get.to(() => NewsWordpressPage(news: appProvider.newsWordpress), fullscreenDialog: true)),
          DisplayNewsWordpress(news: newsWordpress),
        ],
      ),
    );
  }

  Container _buildHeading({required String title, required Function() onTap}) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 1, horizontal: 16),
      child: Row(
        children: [
          Text(title, style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppCOLORS.white)),
          Spacer(),
          ZCard(
            margin: EdgeInsets.symmetric(),
            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            borderRadiusColor: AppCOLORS.yellow,
            child: Text('View All', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w900, color: AppCOLORS.yellow)),
            onTap: onTap,
          ),
        ],
      ),
    );
  }
}

class DisplayAnnoucement extends StatefulWidget {
  const DisplayAnnoucement({Key? key, required this.annoucements}) : super(key: key);
  final List<Announcement> annoucements;

  @override
  State<DisplayAnnoucement> createState() => _DisplayAnnoucementState();
}

class _DisplayAnnoucementState extends State<DisplayAnnoucement> {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics: ClampingScrollPhysics(),
      itemCount: widget.annoucements.length,
      itemBuilder: ((context, index) => Column(
            children: [
              if (index == 0) SizedBox(height: 8),
              ZAnnoucementCard(announcement: (widget.annoucements[index])),
              if (index == widget.annoucements.length - 1) SizedBox(height: 8),
            ],
          )),
    );
  }
}

class DisplayNews extends StatefulWidget {
  final List<News> news;
  DisplayNews({Key? key, required this.news}) : super(key: key);

  @override
  State<DisplayNews> createState() => _DisplayNewsState();
}

class _DisplayNewsState extends State<DisplayNews> {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics: ClampingScrollPhysics(),
      itemCount: widget.news.length,
      itemBuilder: ((context, index) => Column(
            children: [
              if (index == 0) SizedBox(height: 8),
              ZNewsCard(news: (widget.news[index])),
              if (index == widget.news.length - 1) SizedBox(height: 8),
            ],
          )),
    );
  }
}

class DisplayNewsWordpress extends StatefulWidget {
  final List<NewsWordpress> news;
  DisplayNewsWordpress({Key? key, required this.news}) : super(key: key);

  @override
  State<DisplayNewsWordpress> createState() => _DisplayNewsWordpressState();
}

class _DisplayNewsWordpressState extends State<DisplayNewsWordpress> {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
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
    );
  }
}

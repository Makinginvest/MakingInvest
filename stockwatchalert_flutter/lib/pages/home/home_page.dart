import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_appbar_title.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/constants/app_colors.dart';
import 'package:stockwatchalert/models_providers/app_provider.dart';
import 'package:stockwatchalert/pages/home/annoucement_page.dart';

import '../../components/z_news_card.dart';
import '../../components/z_annoucement_card.dart';
import '../../models/announcement_aggr.dart';
import '../../models/news_aggr.dart';
import '../../models_providers/app_controls_provider.dart';
import 'news_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    AppProvider appProvider = Provider.of<AppProvider>(context);
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final annoucements = appProvider.announcementAggr.getTop5Announcements;
    final newsCrypto = appControlsProvider.newsCrypto.length > 4 ? appControlsProvider.newsCrypto.sublist(0, 4) : appControlsProvider.newsCrypto;
    final newsForex = appControlsProvider.newsForex.length > 4 ? appControlsProvider.newsForex.sublist(0, 4) : appControlsProvider.newsForex;
    final newsStocks = appControlsProvider.newsStocks.length > 4 ? appControlsProvider.newsStocks.sublist(0, 4) : appControlsProvider.newsStocks;

    return Scaffold(
      appBar: AppBar(title: AppBarTitle()),
      body: ListView(
        shrinkWrap: true,
        children: [
          _buildHeading(title: 'Announcements', onTap: () => Get.to(() => AnnoucementsPage(annoucements: annoucements), fullscreenDialog: true)),
          DisplayAnnoucement(annoucements: annoucements),
          _buildHeading(title: 'News Crypto', onTap: () => Get.to(() => NewsPage(news: appControlsProvider.newsCrypto), fullscreenDialog: true)),
          DisplayNews(news: newsCrypto),
          _buildHeading(title: 'News Forex', onTap: () => Get.to(() => NewsPage(news: appControlsProvider.newsForex), fullscreenDialog: true)),
          DisplayNews(news: newsForex),
          _buildHeading(title: 'News Stocks', onTap: () => Get.to(() => NewsPage(news: appControlsProvider.newsStocks), fullscreenDialog: true)),
          DisplayNews(news: newsStocks),
        ],
      ),
    );
  }

  Container _buildHeading({required String title, required Function() onTap}) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 1, horizontal: 16),
      child: Row(
        children: [
          Text(
            title,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: AppColors.green),
          ),
          Spacer(),
          ZCard(
            margin: EdgeInsets.zero,
            borderRadius: BorderRadius.circular(8),
            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            child: Text('View all', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w900, color: AppColors.green)),
            borderWidth: 0,
            color: AppColors.green.withOpacity(.05),
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

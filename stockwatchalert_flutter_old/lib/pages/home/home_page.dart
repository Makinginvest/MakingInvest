import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:signalbyt/components/z_app_bar_title.dart';
import 'package:signalbyt/components/z_text_form_field_search.dart';
import 'package:signalbyt/models_providers/app_controls_provider.dart';
import 'package:signalbyt/pages/news/news_page.dart';

import '../../components/z_annoucement_card.dart';
import '../../components/z_card.dart';
import '../../components/z_news_card.dart';
import '../../components/z_news_wordpress_card.dart';
import '../../constants/app_colors.dart';
import '../../models/announcement_aggr.dart';
import '../../models/news_aggr.dart';
import '../../models/news_wordpress.dart';
import '../../models_providers/app_provider.dart';
import '../announcement/annoucement_page.dart';

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

    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final newsStocks = appControlsProvider.newsStocks.length > 4 ? appControlsProvider.newsStocks.sublist(0, 4) : appControlsProvider.newsStocks;

    return Scaffold(
      appBar: AppBar(
        title: AppBarTitle(),
      ),
      body: ListView(
        // shrinkWrap: true,
        children: [
          SizedBox(height: 16),
          // _buildHeading(title: 'Announcements', onTap: () => Get.to(() => AnnoucementsPage(), fullscreenDialog: true)),
          // DisplayAnnoucement(annoucements: annoucements),
          // _buildHeading(title: 'News Stocks', onTap: () => Get.to(() => NewsPage(), fullscreenDialog: true)),
          // DisplayNews(news: newsStocks),
          ZSearch(
            hintText: 'Search symbol or company name',
            margin: EdgeInsets.symmetric(horizontal: 16),
          ),
          SizedBox(height: 16),
          Stack(
            children: [
              Container(
                height: 200,
                foregroundDecoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.5),
                  borderRadius: BorderRadius.circular(16),
                ),
                margin: EdgeInsets.symmetric(horizontal: 16),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  image: DecorationImage(
                    image: AssetImage('assets/images/bull_market.jpg'),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              CarouselSlider(
                  options: CarouselOptions(
                    height: 200.0,
                    autoPlay: true,
                    viewportFraction: 1.0,
                    autoPlayInterval: Duration(seconds: 3),
                  ),
                  items: [
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 32),
                      width: double.infinity,
                      height: double.infinity,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'Lorem Ipsum is simply dummy text of the printing and typesetting industry',
                            style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w900, color: AppColors.white),
                          ),
                          SizedBox(height: 4),
                          Text(
                            'March 15, 2024',
                            style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w500, color: AppColors.white),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 32),
                      width: double.infinity,
                      height: double.infinity,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            '222Lorem Ipsum is simply dummy text of the printing and typesetting industry',
                            style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w900, color: AppColors.white),
                          ),
                          SizedBox(height: 4),
                          Text(
                            'March 15, 2024',
                            style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w500, color: AppColors.white),
                          ),
                        ],
                      ),
                    ),
                  ])
            ],
          ),
          Container(
              margin: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
              child: Column(
                children: [
                  Container(
                    margin: EdgeInsets.only(bottom: 8),
                    decoration: BoxDecoration(
                      border: Border(
                        bottom: BorderSide(
                          color: Colors.green, // This is the color of the border
                          width: 2.0, // This is the width of the border
                        ),
                      ),
                    ),
                    child: Row(
                      children: [Text('Hot Box', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: AppColors.white))],
                    ),
                  ),
                  for (var i = 0; i < 12; i++)
                    Container(
                      margin: EdgeInsets.symmetric(vertical: 3, horizontal: 0),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text('Basic Materials'),
                          Spacer(),
                          Text('0.74058%'),
                          Icon(
                            Icons.arrow_upward,
                            color: AppColors.green,
                            size: 14,
                          ),
                        ],
                      ),
                    ),
                ],
              ))
        ],
      ),
    );
  }

  Container _buildHeading({required String title, required Function() onTap}) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 1, horizontal: 16),
      child: Row(
        children: [
          Text(title, style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.white)),
          Spacer(),
          ZCard(
            margin: EdgeInsets.symmetric(),
            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            borderRadiusColor: AppColors.green,
            child: Text('View All', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w900, color: AppColors.green)),
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

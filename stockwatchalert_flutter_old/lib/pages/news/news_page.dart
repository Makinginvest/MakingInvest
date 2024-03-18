import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:signalbyt/components/z_app_bar_title.dart';

import 'package:signalbyt/models_providers/app_controls_provider.dart';

import '../../components/z_news_card.dart';

class NewsPage extends StatefulWidget {
  NewsPage({
    Key? key,
  }) : super(key: key);

  @override
  State<NewsPage> createState() => _NewsPageState();
}

class _NewsPageState extends State<NewsPage> {
  @override
  Widget build(BuildContext context) {
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final news = appControlsProvider.newsStocks;
    return Scaffold(
      appBar: AppBar(
        title: AppBarTitle(),
      ),
      body: ListView.builder(
        shrinkWrap: true,
        physics: ClampingScrollPhysics(),
        itemCount: news.length,
        itemBuilder: ((context, index) => Column(
              children: [
                if (index == 0) SizedBox(height: 8),
                ZNewsCard(news: (news[index])),
                if (index == news.length - 1) SizedBox(height: 8),
              ],
            )),
      ),
    );
  }
}

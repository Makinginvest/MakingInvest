import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:signalbyt/constants/app_colors.dart';
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
        title: Column(
          children: [
            Text.rich(
              TextSpan(
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700, color: AppColors.white),
                children: [
                  TextSpan(text: 'Stock ', style: TextStyle(color: AppColors.green)),
                  TextSpan(text: 'Watch Alert', style: TextStyle(color: AppColors.white)),
                ],
              ),
            ),
            Text('Your Ultimate Stock Source', style: TextStyle(fontSize: 10, color: AppColors.white)),
          ],
        ),
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

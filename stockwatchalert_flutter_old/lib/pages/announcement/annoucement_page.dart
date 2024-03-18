import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:signalbyt/constants/app_colors.dart';
import 'package:signalbyt/models_providers/app_provider.dart';

import '../../components/z_annoucement_card.dart';

class AnnoucementsPage extends StatefulWidget {
  const AnnoucementsPage({Key? key}) : super(key: key);

  @override
  State<AnnoucementsPage> createState() => _AnnoucementsPageState();
}

class _AnnoucementsPageState extends State<AnnoucementsPage> {
  @override
  Widget build(BuildContext context) {
    AppProvider appProvider = Provider.of<AppProvider>(context);
    final annoucements = appProvider.announcementAggr.getTop5Announcements;
    return Scaffold(
      appBar: AppBar(
        title: Column(
          mainAxisSize: MainAxisSize.min,
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
        itemCount: annoucements.length,
        itemBuilder: ((context, index) => Column(
              children: [
                if (index == 0) SizedBox(height: 8),
                ZAnnoucementCard(announcement: (annoucements[index])),
                if (index == annoucements.length - 1) SizedBox(height: 8),
              ],
            )),
      ),
    );
  }
}

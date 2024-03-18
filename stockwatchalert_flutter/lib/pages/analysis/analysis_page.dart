import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_appbar_title.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/constants/app_colors.dart';

import '../../models_providers/app_controls_provider.dart';
import '../../utils/z_format.dart';

class AnalysisPage extends StatefulWidget {
  const AnalysisPage({super.key});

  @override
  State<AnalysisPage> createState() => _AnalysisPageState();
}

class _AnalysisPageState extends State<AnalysisPage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final AppControlsProvider appProvider = Provider.of<AppControlsProvider>(context);
    final marketAnalysis = appProvider.marketAnalysis;

    return Scaffold(
      appBar: AppBar(title: AppBarTitle()),
      body: ListView(
        children: [
          for (var marketAnalysisItem in marketAnalysis.cryptoSymbolsAnalysis)
            ZCard(
                child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(marketAnalysisItem.symbol, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: AppColors.white)),
                    Spacer(),
                    Text(
                      '${ZFormat.dateFormatSignal(marketAnalysis.dtUpdated)}',
                      style: TextStyle(color: AppColors.white, fontSize: 13, fontWeight: FontWeight.w900),
                    ),
                  ],
                ),
                SizedBox(height: 8),
                Wrap(
                  runSpacing: 6,
                  spacing: 6,
                  children: [
                    for (var marketAnalysisItemData in marketAnalysisItem.data)
                      ZCard(
                        color: marketAnalysisItemData.getStatusColor,
                        margin: EdgeInsets.symmetric(vertical: 0),
                        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 5),
                        borderWidth: 0,
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(marketAnalysisItemData.status),
                            SizedBox(width: 2),
                            Text(marketAnalysisItemData.timeframe.toUpperCase()),
                          ],
                        ),
                      ),
                  ],
                )
              ],
            ))
        ],
      ),
    );
  }
}

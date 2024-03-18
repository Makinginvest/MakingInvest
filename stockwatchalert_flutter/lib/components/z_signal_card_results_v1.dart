import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/utils/z_format.dart';

import '../constants/app_colors.dart';

class ZSignalCardResultsV1 extends StatelessWidget {
  const ZSignalCardResultsV1({Key? key, required this.signalAggr}) : super(key: key);

  final SignalAggrV1 signalAggr;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
      borderWidth: 0,
      color: AppColors.blue,
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SvgPicture.asset('assets/svg/star.svg', height: 30, width: 30),
          SizedBox(width: 8),
          Expanded(
            child: Column(
              children: [
                for (var result in signalAggr.results)
                  Container(
                    margin: EdgeInsets.symmetric(vertical: 1.25),
                    child: Row(
                      children: [
                        Text('${result.days} days trades: ${result.total}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
                        Spacer(),
                        Text('Win rate: ${ZFormat.numToPercent(result.winRate)}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

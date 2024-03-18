import 'package:flutter/material.dart';

import '../constants/app_colors.dart';
import '../models/signal_aggr.dart';
import '../utils/z_format.dart';
import 'z_card.dart';

class ZSignalCardResults extends StatelessWidget {
  const ZSignalCardResults({
    Key? key,
    required this.signalAggr,
  }) : super(key: key);

  final SignalAggr signalAggr;

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
      borderWidth: 0,
      // color: Colors.purple,
      color: Color(0xFF048044),
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      child: Text(
                        '14 days trades: ${signalAggr.results14Days?.total}',
                        style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                      ),
                      width: MediaQuery.of(context).size.width * .3,
                    ),
                    Spacer(),
                    Container(
                      child: Text(
                        'Win rate: ${signalAggr.results14Days?.getWinRate()}%',
                        style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                      ),
                    ),
                    if (!signalAggr.name.contains('forex'))
                      Container(
                        child: Text(
                          ' || Avg: ${ZFormat.numToPercent(signalAggr.results14Days?.avePct ?? 0)}',
                          style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                        ),
                      ),
                    if (signalAggr.name.contains('forex'))
                      Container(
                        child: Text(
                          ' || Avg: ${ZFormat.toPrecision((signalAggr.results14Days?.avePct ?? 0) * 10000, 0)} pips',
                          style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                        ),
                      ),
                  ],
                ),
                SizedBox(height: 4),
                Row(
                  children: [
                    Container(
                      child: Text(
                        '30 days trades: ${signalAggr.results30Days?.total}',
                        style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                      ),
                      width: MediaQuery.of(context).size.width * .3,
                    ),
                    Spacer(),
                    Container(
                      child: Text(
                        'Win rate: ${signalAggr.results30Days?.getWinRate()}%',
                        style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                      ),
                    ),
                    if (!signalAggr.name.contains('forex'))
                      Container(
                        child: Text(
                          ' || Avg: ${ZFormat.numToPercent(signalAggr.results30Days?.avePct ?? 0)}',
                          style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                        ),
                      ),
                    if (signalAggr.name.contains('forex'))
                      Container(
                        child: Text(
                          ' || Avg: ${ZFormat.toPrecision((signalAggr.results30Days?.avePct ?? 0) * 10000, 0)} pips',
                          style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900),
                        ),
                      ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

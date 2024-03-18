import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../constants/app_colors.dart';
import '../models/signal_aggr.dart';
import '../pages/subsciption/subscription_page.dart';
import '../utils/z_format.dart';
import 'z_card.dart';

class ZSignalSubscribeCard extends StatefulWidget {
  ZSignalSubscribeCard({Key? key, required this.signal}) : super(key: key);
  final Signal signal;

  @override
  State<ZSignalSubscribeCard> createState() => _ZSignalSubscribeCardState();
}

class _ZSignalSubscribeCardState extends State<ZSignalSubscribeCard> {
  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return Column(
      children: [
        ZCard(
          padding: EdgeInsets.all(10),
          borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
          margin: EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Text('Opened:'),
                  Spacer(),
                  Text(
                    '${ZFormat.dateFormatSignal(widget.signal.entryDateTimeUtc)}',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13),
                  ),
                ],
              ),
              SizedBox(height: 6),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  // Container(
                  //   decoration:
                  //       BoxDecoration(color: widget.signal.entryType == 'long' ? AppColors.appColorGreen : AppColors.appColorRed, borderRadius: BorderRadius.circular(5)),
                  //   padding: EdgeInsets.symmetric(horizontal: 8, vertical: 5),
                  //   margin: EdgeInsets.only(bottom: 3),
                  //   child: Text('${widget.signal.entryType.toUpperCase()}', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 12)),
                  // ),
                  Text(
                    widget.signal.symbol,
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, height: 0),
                  ),
                  Spacer(),
                  getStatus(widget.signal),
                ],
              ),
              SizedBox(height: 8),
              ZCard(
                color: Colors.white,
                onTap: () => Get.to(() => SubscriptionPage(), fullscreenDialog: true),
                margin: EdgeInsets.only(left: 0, right: 0, bottom: 0),
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                child: Column(
                  children: [
                    Text('Tap to unlock all premium signals', style: TextStyle(color: Colors.black)),
                  ],
                ),
              ),
            ],
          ),
        ),

        // SizedBox(height: 8),
        // Divider(color: Colors.white12, height: 10, thickness: 1)
      ],
    );
  }

  getStatus(Signal signal) {
    if (signal.takeProfit3Hit) return _buildStatusContainer(text: 'Target 3', isProfit: true);
    if (signal.takeProfit2Hit) return _buildStatusContainer(text: 'Target 2', isProfit: true);
    if (signal.takeProfit1Hit) return _buildStatusContainer(text: 'Target 1', isProfit: true);
    return _buildStatusContainer(text: 'In progress', isProfit: true, isInProgress: true);
  }

  _buildStatusContainer({required String text, required bool isProfit, bool isInProgress = false}) {
    if (isInProgress)
      return Container(
        width: 95,
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(6), color: AppColors.gray),
        padding: EdgeInsets.symmetric(horizontal: 6, vertical: 5),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(text, style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
            SizedBox(width: 2),
            Icon(isProfit ? Icons.incomplete_circle_outlined : Icons.close, color: Colors.white, size: 13),
          ],
        ),
      );
    return Container(
      width: 95,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(5),
        color: isProfit ? AppColors.blue : AppColors.red,
      ),
      padding: EdgeInsets.symmetric(horizontal: 6, vertical: 5),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(text, style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
          SizedBox(width: 2),
          Icon(isProfit ? Icons.check : Icons.close, color: Colors.white, size: 13),
        ],
      ),
    );
  }
}

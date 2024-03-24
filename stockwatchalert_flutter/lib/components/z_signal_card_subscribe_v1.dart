import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/pages/subsciption/subscription_page.dart';

import '../constants/app_colors.dart';
import '../utils/z_format.dart';

class ZSignalCardSubscribeV1 extends StatefulWidget {
  ZSignalCardSubscribeV1({Key? key, required this.signal}) : super(key: key);
  final SignalV1 signal;

  @override
  State<ZSignalCardSubscribeV1> createState() => _ZSignalCardSubscribeV1State();
}

class _ZSignalCardSubscribeV1State extends State<ZSignalCardSubscribeV1> {
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
                  // getStatus(widget.signal),
                ],
              ),
              SizedBox(height: 8),
              ZCard(
                color: Colors.white,
                onTap: () => Get.to(() => SubscriptionPage(), fullscreenDialog: true),
                margin: EdgeInsets.only(left: 0, right: 0, bottom: 0),
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                borderRadius: BorderRadius.circular(8),
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

  // ignore: unused_element
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

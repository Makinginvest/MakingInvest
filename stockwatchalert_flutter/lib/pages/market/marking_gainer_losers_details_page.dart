import 'package:flutter/material.dart';
import 'package:signalbyt/components/z_card.dart';
import 'package:signalbyt/constants/app_colors.dart';
import 'package:signalbyt/models/market_activity_aggr.dart';
import 'package:signalbyt/utils/z_format.dart';

class MarketGainerLosersDetailsPage extends StatefulWidget {
  const MarketGainerLosersDetailsPage({super.key, required this.activities});
  final List<MarketActivity> activities;

  @override
  State<MarketGainerLosersDetailsPage> createState() => _MarketGainerLosersDetailsPageState();
}

class _MarketGainerLosersDetailsPageState extends State<MarketGainerLosersDetailsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: ListView.builder(
      itemCount: widget.activities.length,
      itemBuilder: ((context, index) => Column(
            children: [
              // if (index == 0) SizedBox(height: 8),
              ZCard(
                  child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(widget.activities[index].symbol),
                        SizedBox(height: 2),
                        Text(widget.activities[index].name, style: TextStyle(fontSize: 12, color: Colors.grey)),
                      ],
                    ),
                  ),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        '${ZFormat.numToMoney(widget.activities[index].price)}',
                      ),
                      SizedBox(height: 2),
                      Row(
                        children: [
                          Text('${ZFormat.numToPercent(widget.activities[index].changesPercentage / 100)}',
                              style: TextStyle(color: widget.activities[index].isChangePositive ? AppColors.green : AppColors.red)),
                          SizedBox(width: 4),
                          Text('(${ZFormat.numToMoney(widget.activities[index].change)})'),
                        ],
                      ),
                    ],
                  ),
                ],
              ))
            ],
          )),
    ));
  }
}

import 'package:configurable_expansion_tile_null_safety/configurable_expansion_tile_null_safety.dart';
import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';

import '../constants/app_colors.dart';
import '../models/signal_aggr.dart';
import '../models_providers/app_controls_provider.dart';
import '../pages/signals/signals_closed_page.dart';
import '../pages/tradingview/trading_view_page.dart';
import '../utils/Z_get_pips_percent.dart';
import '../utils/z_format.dart';
import 'z_card.dart';

class ZSignalCard extends StatefulWidget {
  ZSignalCard({Key? key, required this.signal, this.signalAggrX, this.isClosed = false}) : super(key: key);
  final SignalAggr? signalAggrX;
  final Signal signal;
  final bool isClosed;

  @override
  State<ZSignalCard> createState() => _ZSignalCardState();
}

class _ZSignalCardState extends State<ZSignalCard> {
  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    final AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final isForex = widget.signal.market.toLowerCase() == 'forex';

    final entryVsCurrentPrice = widget.signal.compareEntryPriceWithCurrentPrice(price: appControlsProvider.getWSSymbolPriceSignal(widget.signal), isPips: isForex);

    return Column(
      children: [
        ZCard(
          padding: EdgeInsets.all(10),
          borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
          borderWidth: 1.5,
          margin: EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          child: Container(
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(10), color: Colors.transparent),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (widget.isClosed)
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      if (!widget.signal.isClosed) Text('Still active:', style: TextStyle(fontSize: 14)),
                      if (widget.signal.isClosed) Text('Closed:'),
                      Spacer(),
                      Text(
                        '${ZFormat.dateFormatSignal(widget.signal.closedDateTimeUtc)}',
                        style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13),
                      ),
                    ],
                  ),
                if (widget.isClosed) SizedBox(height: 2),
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
                SizedBox(height: 12),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      width: 65,
                      decoration: BoxDecoration(
                        color: widget.signal.entryType == 'long' ? AppColors.green : AppColors.red,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: widget.signal.entryType == 'long' ? AppColors.green : AppColors.red),
                      ),
                      padding: EdgeInsets.symmetric(horizontal: 4, vertical: 3),
                      margin: EdgeInsets.only(bottom: 3),
                      child: Text(
                        '${widget.signal.entryType.toUpperCase()}',
                        style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14, color: AppColors.white),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    SizedBox(width: 6),
                    Text(
                      widget.signal.symbol,
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, height: 0),
                    ),
                    Spacer(),
                    getStatus(widget.signal),
                  ],
                ),
                SizedBox(height: 8),
                Row(
                  children: [
                    if (widget.signal.market == 'crypto')
                      ZCard(
                        borderRadius: BorderRadius.circular(8),
                        color: AppColors.green,
                        borderRadiusColor: Colors.transparent,
                        padding: EdgeInsets.symmetric(vertical: 5, horizontal: 6),
                        margin: EdgeInsets.symmetric(),
                        child: Text('${widget.signal.leverage}x leverage', style: TextStyle(fontSize: 12.25, fontWeight: FontWeight.w700, color: Colors.black)),
                      ),
                    SizedBox(width: 8),
                    if (widget.signal.market == 'crypto')
                      ZCard(
                        borderRadius: BorderRadius.circular(8),
                        borderRadiusColor: Colors.transparent,
                        color: AppColors.green,
                        padding: EdgeInsets.symmetric(vertical: 5, horizontal: 6),
                        margin: EdgeInsets.symmetric(),
                        child: Text(widget.signal.hasFutures ? 'Futures available' : 'Spot only trade ',
                            style: TextStyle(fontSize: 12.25, fontWeight: FontWeight.w700, color: Colors.black)),
                      ),
                  ],
                ),
                SizedBox(height: 8),
                Row(children: [
                  Text(
                    'Entry price',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
                  ),
                  SizedBox(width: 4),
                  Spacer(),
                  SizedBox(width: 4),
                  Text(widget.signal.entryPrice.toString()),
                ]),
                SizedBox(height: 8),
                Row(children: [
                  Text(
                    'Stop Loss',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color),
                  ),
                  SizedBox(width: 4),
                  Text(getPipsOrPercentStr(
                    isPips: widget.signal.market.toLowerCase() == 'forex' ? true : false,
                    pips: widget.signal.stopLossPips,
                    percent: widget.signal.stopLossPct,
                    leverage: widget.signal.leverage,
                  )),
                  Spacer(),
                  SizedBox(width: 4),
                  Text('${ZFormat.toPrecision(widget.signal.stopLoss, 8)}'),
                ]),
                SizedBox(height: 8),
                ConfigurableExpansionTile(
                  headerExpanded: Flexible(
                    child: ZCard(
                      height: 40,
                      borderWidth: 0,
                      padding: EdgeInsets.symmetric(vertical: 0, horizontal: 12),
                      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
                      color: isLightTheme ? AppColors.cardButtonLight : AppColors.cardButtonDark,
                      margin: EdgeInsets.zero,
                      child: Row(
                        children: [
                          Container(
                            width: MediaQuery.of(context).size.width * .375,
                            child: Text(widget.isClosed ? 'Targets' : "Current Price", style: TextStyle()),
                          ),
                          if (!widget.isClosed)
                            Text(appControlsProvider.getWSSymbolPriceSignal(widget.signal).toString(), style: TextStyle(fontSize: 14, fontWeight: FontWeight.w900)),
                          Spacer(),
                          if (!widget.isClosed)
                            Text(
                              getPipsOrPercentStr(
                                isPips: isForex,
                                pips: entryVsCurrentPrice,
                                percent: entryVsCurrentPrice,
                                leverage: widget.signal.leverage,
                              ),
                              style: TextStyle(
                                  color: widget.signal.compareEntryPriceWithCurrentPrice(price: appControlsProvider.getWSSymbolPriceSignal(widget.signal)) < 0
                                      ? AppColors.red
                                      : AppColors.green,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold),
                            ),
                          SizedBox(width: 4),
                          Icon(Icons.arrow_drop_up, size: 25),
                        ],
                      ),
                    ),
                  ),
                  header: (isExpanded, _, heightFactor, controller) => Flexible(
                    child: ZCard(
                      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
                      color: isLightTheme ? AppColors.cardButtonLight : AppColors.cardButtonDark,
                      borderWidth: 0,
                      padding: EdgeInsets.symmetric(vertical: 7, horizontal: 12),
                      margin: EdgeInsets.zero,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Container(
                              width: MediaQuery.of(context).size.width * .375,
                              child: Text(widget.isClosed ? 'Targets' : 'Current price', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w900))),
                          if (!widget.isClosed) Text(appControlsProvider.getWSSymbolPriceSignal(widget.signal).toString(), style: TextStyle()),
                          Spacer(),
                          if (!widget.isClosed)
                            Text(
                              getPipsOrPercentStr(
                                isPips: isForex,
                                pips: entryVsCurrentPrice,
                                percent: entryVsCurrentPrice,
                                leverage: widget.signal.leverage,
                              ),
                              style: TextStyle(
                                  color: widget.signal.compareEntryPriceWithCurrentPrice(price: appControlsProvider.getWSSymbolPriceSignal(widget.signal)) < 0
                                      ? AppColors.red
                                      : AppColors.green,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold),
                            ),
                          SizedBox(width: 4),
                          Icon(Icons.arrow_drop_down, size: 25),
                        ],
                      ),
                    ),
                  ),
                  childrenBody: Column(
                    children: [
                      SizedBox(height: 8),
                      _buildTargetCard(
                          name: 'Target 1',
                          target: widget.signal.takeProfit1,
                          targetPct: widget.signal.takeProfit1Pct,
                          targetPips: widget.signal.takeProfit1Pips,
                          result: widget.signal.takeProfit1Result,
                          resultTimeUtc: widget.signal.takeProfit1DateTimeUtc,
                          signal: widget.signal),
                      _buildTargetCard(
                          name: 'Target 2',
                          target: widget.signal.takeProfit2,
                          targetPct: widget.signal.takeProfit2Pct,
                          targetPips: widget.signal.takeProfit2Pips,
                          result: widget.signal.takeProfit2Result,
                          resultTimeUtc: widget.signal.takeProfit2DateTimeUtc,
                          signal: widget.signal),
                      _buildTargetCard(
                          name: 'Target 3',
                          target: widget.signal.takeProfit3,
                          targetPct: widget.signal.takeProfit3Pct,
                          targetPips: widget.signal.takeProfit3Pips,
                          result: widget.signal.takeProfit3Result,
                          resultTimeUtc: widget.signal.takeProfit3DateTimeUtc,
                          signal: widget.signal),
                      _buildTargetCard(
                          name: 'Target 4',
                          target: widget.signal.takeProfit4,
                          targetPct: widget.signal.takeProfit4Pct,
                          targetPips: widget.signal.takeProfit4Pips,
                          result: widget.signal.takeProfit4Result,
                          resultTimeUtc: widget.signal.takeProfit3DateTimeUtc,
                          signal: widget.signal),
                      SizedBox(height: 12),
                      Row(children: [Text(getStatusText(widget.signal))]),
                      SizedBox(height: 8),
                    ],
                  ),
                ),
                SizedBox(height: 8),
                if (widget.signal.stopLossRevisedTp1 || widget.signal.stopLossRevisedTp2 || widget.signal.stopLossRevisedTp3)
                  Column(
                    children: [
                      Text(widget.signal.getBreakEvenText()),
                      SizedBox(height: 8),
                    ],
                  ),
                if (!widget.isClosed && widget.signalAggrX != null)
                  Row(
                    children: [
                      Expanded(
                        child: ZCard(
                          height: 40,
                          borderWidth: 0,
                          color: isLightTheme ? AppColors.cardButtonLight : AppColors.cardButtonDark,
                          onTap: () => Get.to(() => TradingViewPage(symbol: widget.signal.symbol), fullscreenDialog: true),
                          padding: EdgeInsets.symmetric(vertical: 0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text('View Chart', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, height: 1.5)),
                              SizedBox(width: 4),
                              Icon(AntDesign.piechart, size: 14),
                            ],
                          ),
                          margin: EdgeInsets.zero,
                        ),
                      ),
                      SizedBox(width: 6),
                      Expanded(
                        child: ZCard(
                          borderWidth: 0,
                          height: 40,
                          onTap: () {
                            Get.to(() => SignalsClosedPage(signalAggr: widget.signalAggrX!, signal: widget.signal, showSearch: false),
                                fullscreenDialog: true, duration: Duration(milliseconds: 500));
                          },
                          padding: EdgeInsets.symmetric(vertical: 8),
                          color: isLightTheme ? AppColors.cardButtonLight : AppColors.cardButtonDark,
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('View History', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w900, height: 1.5)),
                              SizedBox(width: 8),
                              Icon(AntDesign.link, size: 14),
                            ],
                          ),
                          margin: EdgeInsets.zero,
                        ),
                      ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  _buildTargetCard({
    required String name,
    required String result,
    required num target,
    required num targetPct,
    required num targetPips,
    required DateTime? resultTimeUtc,
    required Signal signal,
  }) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8),
        color: result == 'profit'
            ? AppColors.green
            : isLightTheme
                ? AppColors.cardButtonLight
                : AppColors.cardButtonDark,
      ),
      margin: EdgeInsets.symmetric(vertical: 6),
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      child: Row(children: [
        Container(
          width: MediaQuery.of(context).size.width * .375,
          child: Text('${name}', style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontWeight: FontWeight.bold)),
        ),
        SizedBox(width: 4),
        Text('${ZFormat.toPrecision(target, 8)}'),
        Spacer(),
        Text(
            getPipsOrPercentStr(
              isPips: widget.signal.market.toLowerCase() == 'forex' ? true : false,
              pips: targetPips,
              percent: targetPct,
              leverage: widget.signal.leverage,
            ),
            style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontWeight: FontWeight.bold)),
        if (result == 'profit') Icon(Icons.check, color: Theme.of(context).textTheme.bodySmall!.color, size: 16),
      ]),
    );
  }

  getStatus(Signal signal) {
    if (signal.takeProfit4Hit) return _buildStatusContainer(text: 'Target 4', isProfit: true);
    if (signal.takeProfit3Hit) return _buildStatusContainer(text: 'Target 3', isProfit: true);
    if (signal.takeProfit2Hit) return _buildStatusContainer(text: 'Target 2', isProfit: true);
    if (signal.takeProfit1Hit) return _buildStatusContainer(text: 'Target 1', isProfit: true);
    if (signal.stopLossHit) return _buildStatusContainer(text: 'Stop Loss hit', isProfit: false);
    return _buildStatusContainer(text: 'In progress', isProfit: true, isInProgress: true);
  }

  String getStatusText(Signal signal) {
    if (signal.takeProfit4Hit) return 'Bagged full profit @ ${ZFormat.dateFormatSignal(signal.takeProfit4DateTimeUtc)}';
    if (signal.takeProfit3Hit) return 'Bagged target 3 profit @ ${ZFormat.dateFormatSignal(signal.takeProfit3DateTimeUtc)}';
    if (signal.takeProfit2Hit) return 'Bagged target 2 profit @ ${ZFormat.dateFormatSignal(signal.takeProfit2DateTimeUtc)}';
    if (signal.takeProfit1Hit) return 'Bagged target 1 profit @ ${ZFormat.dateFormatSignal(signal.takeProfit1DateTimeUtc)}';
    if (signal.stopLossHit) return 'Stopped out @ ${ZFormat.dateFormatSignal(signal.takeProfit1DateTimeUtc)}';
    return 'In progress';
  }

  _buildStatusContainer({required String text, required bool isProfit, bool isInProgress = false}) {
    if (isInProgress)
      return Container(
        width: 95,
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(8), color: AppColors.gray),
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
        borderRadius: BorderRadius.circular(8),
        color: isProfit ? AppColors.blue : AppColors.red,
        border: Border.all(color: isProfit ? AppColors.blue : AppColors.red),
      ),
      padding: EdgeInsets.symmetric(horizontal: 4, vertical: 5),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            text,
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13, height: 1.35),
            textAlign: TextAlign.center,
          ),
          SizedBox(width: 1),
          Icon(isProfit ? Icons.check : Icons.close, color: Colors.white, size: 12),
        ],
      ),
    );
  }
}

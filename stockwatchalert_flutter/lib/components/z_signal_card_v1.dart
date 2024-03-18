import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';

import '../constants/app_colors.dart';
import '../models_providers/app_controls_provider.dart';
import '../utils/Z_get_pips_percent.dart';
import '../utils/z_format.dart';

class ZSignalCardV1 extends StatefulWidget {
  ZSignalCardV1({Key? key, required this.signal, this.signalAggrV1, this.isClosed = false}) : super(key: key);
  final SignalAggrV1? signalAggrV1;
  final SignalV1 signal;
  final bool isClosed;

  @override
  State<ZSignalCardV1> createState() => _ZSignalCardV1State();
}

class _ZSignalCardV1State extends State<ZSignalCardV1> {
  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    final AppControlsProvider appWsProvider = Provider.of<AppControlsProvider>(context);
    final isForex = widget.signal.market.toLowerCase() == 'forex';
    final entryVsCurrentPrice = widget.signal.compareEntryPriceWithCurrentPrice(price: appWsProvider.getLivelPriceSignalV1(widget.signal), isPips: isForex);

    return Column(
      children: [
        ZCard(
          padding: EdgeInsets.all(6),
          borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
          borderWidth: 1.5,
          borderRadius: BorderRadius.circular(8),
          margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
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
                        '${ZFormat.dateFormatSignal(widget.signal.exitDateTimeUtc)}',
                        style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13),
                      ),
                    ],
                  ),
                if (widget.isClosed) SizedBox(height: 2),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Text(
                              widget.signal.symbol,
                              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16, height: 0),
                            ),
                            SizedBox(width: 4),
                            Text(
                              '@${ZFormat.dateFormatSignal(widget.signal.entryDateTimeUtc)}',
                              style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 12, height: 0),
                            ),
                          ],
                        ),
                        SizedBox(height: 2),
                        Row(
                          children: [
                            Text(
                              widget.signal.getMaxPctPips,
                              style: TextStyle(
                                fontWeight: FontWeight.w700,
                                fontSize: 12,
                                height: 0,
                                fontStyle: FontStyle.italic,
                                color: AppColors.green,
                              ),
                            ),
                            SizedBox(width: 4),
                            Text(
                              widget.signal.getMinPctPips,
                              style: TextStyle(
                                fontWeight: FontWeight.w700,
                                fontSize: 12,
                                height: 0,
                                fontStyle: FontStyle.italic,
                                color: AppColors.red,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Spacer(),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Container(
                          decoration: BoxDecoration(
                            color: widget.signal.getProgressColor,
                            borderRadius: BorderRadius.circular(6),
                          ),
                          padding: EdgeInsets.symmetric(horizontal: 8, vertical: 7),
                          child: Text(
                            widget.signal.statusTarget,
                            style: TextStyle(fontWeight: FontWeight.w900, fontSize: 13.5, color: AppColors.white, height: 0),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(width: 4),
                  ],
                ),
                SizedBox(height: 12),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      width: 58,
                      decoration: BoxDecoration(
                        color: widget.signal.entryType == 'long' ? AppColors.green : AppColors.red,
                        borderRadius: BorderRadius.circular(6),
                        border: Border.all(color: widget.signal.entryType == 'long' ? AppColors.green : AppColors.red),
                      ),
                      padding: EdgeInsets.symmetric(horizontal: 2, vertical: 6),
                      margin: EdgeInsets.only(bottom: 3),
                      child: Text(
                        '${widget.signal.entryType.toUpperCase()}',
                        style: TextStyle(fontWeight: FontWeight.w900, fontSize: 13.5, color: AppColors.white),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    SizedBox(width: 6),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'Entry Price',
                          style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13.5, height: 0),
                        ),
                        Text(
                          '${ZFormat.toPrecision(widget.signal.entryPrice, 4)}',
                          style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13.5, height: 0),
                        ),
                      ],
                    ),
                    Spacer(),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text("Current Price", style: TextStyle(height: 0)),
                        if (!widget.isClosed)
                          Row(
                            children: [
                              if (!widget.isClosed)
                                Text(appWsProvider.getLivelPriceSignalV1(widget.signal).toString(),
                                    style: TextStyle(
                                      fontSize: 13.5,
                                      fontWeight: FontWeight.w500,
                                      height: 0,
                                    )),
                              SizedBox(width: 4),
                              Text(
                                getPipsOrPercentStr(isPips: isForex, pips: entryVsCurrentPrice, percent: entryVsCurrentPrice, leverage: widget.signal.leverage),
                                style: TextStyle(
                                    color: widget.signal.compareEntryPriceWithCurrentPrice(price: appWsProvider.getLivelPriceSignalV1(widget.signal)) < 0
                                        ? AppColors.red
                                        : AppColors.green,
                                    fontSize: 13.5,
                                    height: 0,
                                    fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                      ],
                    ),
                    // getStatus(widget.signal),
                  ],
                ),
                SizedBox(height: 6),
                Row(children: [
                  Text(
                    'Stop Loss',
                    style: TextStyle(
                      color: Theme.of(context).textTheme.bodySmall!.color,
                      fontSize: 13.5,
                    ),
                  ),
                  SizedBox(width: 4),
                  Text(
                      getPipsOrPercentStr(
                        isPips: widget.signal.market.toLowerCase() == 'forex' ? true : false,
                        pips: widget.signal.slPips,
                        percent: widget.signal.slPct,
                        leverage: widget.signal.leverage,
                      ),
                      style: TextStyle(fontWeight: FontWeight.w500)),
                  if (widget.signal.slDateTimeUtc != null)
                    Text(' @${ZFormat.dateFormatSignal(widget.signal.slDateTimeUtc)}', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
                  Spacer(),
                  Text('${ZFormat.toPrecision(widget.signal.slPrice, 4)}', style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w500)),
                ]),
                SizedBox(height: 6),
                Row(children: [
                  Text(
                    'Target 1',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13),
                  ),
                  SizedBox(width: 4),
                  Text(getPipsOrPercentStr(
                    isPips: widget.signal.market.toLowerCase() == 'forex' ? true : false,
                    pips: widget.signal.tp1Pips,
                    percent: widget.signal.tp1Pct,
                    leverage: widget.signal.leverage,
                  )),
                  if (widget.signal.tp1DateTimeUtc != null)
                    Text(' @${ZFormat.dateFormatSignal(widget.signal.tp1DateTimeUtc)}', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
                  Spacer(),
                  Text('${ZFormat.toPrecision(widget.signal.tp1Price, 4)}', style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w500)),
                ]),
                SizedBox(height: 6),
                Row(children: [
                  Text(
                    'Target 2',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13),
                  ),
                  SizedBox(width: 4),
                  Text(getPipsOrPercentStr(
                    isPips: widget.signal.market.toLowerCase() == 'forex' ? true : false,
                    pips: widget.signal.tp2Pips,
                    percent: widget.signal.tp2Pct,
                    leverage: widget.signal.leverage,
                  )),
                  if (widget.signal.tp2DateTimeUtc != null)
                    Text(' @${ZFormat.dateFormatSignal(widget.signal.tp2DateTimeUtc)}', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
                  Spacer(),
                  Text('${ZFormat.toPrecision(widget.signal.tp2Price, 4)}', style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w500)),
                ]),
                SizedBox(height: 6),
                Row(children: [
                  Text(
                    'Target 3',
                    style: TextStyle(color: Theme.of(context).textTheme.bodySmall!.color, fontSize: 13),
                  ),
                  SizedBox(width: 4),
                  Text(getPipsOrPercentStr(
                    isPips: widget.signal.market.toLowerCase() == 'forex' ? true : false,
                    pips: widget.signal.tp3Pips,
                    percent: widget.signal.tp3Pct,
                    leverage: widget.signal.leverage,
                  )),
                  if (widget.signal.tp3DateTimeUtc != null)
                    Text(' @${ZFormat.dateFormatSignal(widget.signal.tp3DateTimeUtc)}', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
                  Spacer(),
                  Text('${ZFormat.toPrecision(widget.signal.tp3Price, 4)}', style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w500)),
                ]),
                SizedBox(height: 6),
                if (widget.signal.comment != '')
                  Container(child: Text(widget.signal.comment, style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w500, fontStyle: FontStyle.italic))),
              ],
            ),
          ),
        ),
      ],
    );
  }

  void onDismiss() {
    print('Menu is dismiss');
  }

  void onShow() {
    print('Menu is show');
  }

  void _showStatusDialog({required SignalV1 signal}) {
    Get.bottomSheet(Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          decoration: BoxDecoration(color: Theme.of(context).scaffoldBackgroundColor, borderRadius: BorderRadius.circular(16)),
          width: MediaQuery.of(context).size.width,
          padding: EdgeInsets.all(16),
          child: Column(
            children: [
              Row(
                children: [
                  Spacer(),
                  ZCard(
                    margin: EdgeInsets.symmetric(),
                    padding: EdgeInsets.symmetric(horizontal: 2, vertical: 2),
                    child: Icon(Icons.close, size: 22),
                    onTap: () => Navigator.of(context).pop(),
                  ),
                ],
              ),
              SizedBox(height: 8),
              ZCard(
                  margin: EdgeInsets.symmetric(vertical: 8),
                  child: Row(
                    children: [
                      Text('View Chart'),
                      Spacer(),
                      Icon(Icons.arrow_forward_ios, size: 16),
                    ],
                  ),
                  onTap: () {}),
              ZCard(
                  margin: EdgeInsets.symmetric(vertical: 8),
                  child: Row(
                    children: [
                      Text('View Chart'),
                      Spacer(),
                      Icon(Icons.arrow_forward_ios, size: 16),
                    ],
                  ),
                  onTap: () {}),
              SizedBox(height: 32),
            ],
          ),
        )
      ],
    ));
  }
}

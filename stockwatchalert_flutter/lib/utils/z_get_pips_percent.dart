import 'package:stockwatchalert/utils/z_format.dart';

String getPipsOrPercentStr({bool isPips = false, num pips = 0, num percent = 0, leverage = 1}) {
  if (isPips) {
    pips = pips.round();
    return '${pips} pips';
  } else {
    return '(${ZFormat.numToPercent(percent * leverage)})';
  }
}

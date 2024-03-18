import 'package:flutter/widgets.dart';

import '../constants/app_colors.dart';

class AppBarTitle extends StatelessWidget {
  const AppBarTitle({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('StockWatchAlert', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700, color: AppColors.green, height: 0)),
        Text('Premium market insights', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w500, height: 0)),
      ],
    );
  }
}

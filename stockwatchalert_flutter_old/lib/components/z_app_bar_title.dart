import 'package:flutter/material.dart';

import '../constants/app_colors.dart';

class AppBarTitle extends StatelessWidget {
  const AppBarTitle({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text.rich(
          TextSpan(
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700, color: AppColors.white),
            children: [
              TextSpan(text: 'Stock', style: TextStyle(color: AppColors.green)),
              TextSpan(text: 'WatchAlert', style: TextStyle(color: AppColors.white)),
            ],
          ),
        ),
        Text('Your Ultimate Stock Source', style: TextStyle(fontSize: 10, color: AppColors.white)),
      ],
    );
  }
}

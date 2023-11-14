import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';

import '../models/auth_user.dart';
import '../models_providers/auth_provider.dart';
import '../pages/subsciption/subscription_page.dart';
import 'z_card.dart';

class ZUpgradeSubscriptionCard extends StatelessWidget {
  const ZUpgradeSubscriptionCard({super.key});

  @override
  Widget build(BuildContext context) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final authUser = authProvider.authUser;
    if (authUser == null) return Container();

    return ZCard(
        margin: EdgeInsets.symmetric(vertical: 0),
        onTap: () => Get.to(() => SubscriptionPage()),
        // color: Colors.purple,
        color: Color(0xFF048044),
        borderRadius: BorderRadius.circular(16),
        child: authUser.hasActiveSubscription ? _buildProSubscribe(authUser) : _buildSubscribe());
  }

  Row _buildSubscribe() {
    return Row(
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Upgrade to Pro', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            SizedBox(height: 2),
            Text('Enjoy all benefits without restrictions', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
          ],
        ),
        Spacer(),
        SvgPicture.asset('assets/svg/arrow-right.svg', colorFilter: ColorFilter.mode(Colors.white, BlendMode.srcIn), height: 16, width: 16),
      ],
    );
  }

  _buildProSubscribe(AuthUser authUser) {
    return Row(
      children: [
        // SvgPicture.asset('assets/svg/account-stars.svg', height: 60, width: 60),
        // SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('You have an active subscription', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            SizedBox(height: 2),
            if (authUser.subIsLifetimeExpirationDateTime == null) Text('Subscription valid forever', textAlign: TextAlign.center),
            if (authUser.subIsLifetimeExpirationDateTime != null) Text('Subscription valid until ${authUser.getSubscriptionEndDateTime()}'),
          ],
        ),
        Spacer(),
        SvgPicture.asset('assets/svg/arrow-right.svg', colorFilter: ColorFilter.mode(Colors.white, BlendMode.srcIn), height: 16, width: 16),
      ],
    );
  }
}

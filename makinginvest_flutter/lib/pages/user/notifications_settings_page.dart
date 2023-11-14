import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:provider/provider.dart';

import '../../components/z_card.dart';
import '../../constants/app_colors.dart';
import '../../models/auth_user.dart';
import '../../models_providers/auth_provider.dart';
import '../../models_services/firebase_auth_service.dart';

class NotificationSettingsPage extends StatefulWidget {
  const NotificationSettingsPage({Key? key}) : super(key: key);

  @override
  State<NotificationSettingsPage> createState() => _NotificationSettingsPageState();
}

class _NotificationSettingsPageState extends State<NotificationSettingsPage> {
  @override
  Widget build(BuildContext context) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final AuthUser? authUser = authProvider.authUser!;
    if (authUser == null) return Scaffold(appBar: AppBar(title: Text('Notifications Settings')));
    return Scaffold(
      appBar: AppBar(
        title: Text('Notifications Settings'),
      ),
      body: ListView(
        children: [
          Container(
            margin: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
            child: Text('Enable or disable notifications', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
          ),
          Divider(),
          _buildNotificationCard(
            value: !authUser.notificationsDisabled.contains('general'),
            title: 'General notifications',
            iconColor: AppCOLORS.green,
            id: 'general',
            authUser: authUser,
          ),

          Divider(),
          // _buildNotificationCard(
          //   value: authUser.isNotificationsEnabledCryptoRisky,
          //   title: 'Risky Stocks notifications',
          //   iconColor: AppColors.appColorPurple,
          //   fieldKey: 'isNotificationsEnabledCryptoRisky',
          //   authUser: authUser,
          // ),
          // _buildNotificationCard(
          //   value: authUser.isNotificationsEnabledForexRisky,
          //   title: 'Risky Stocks notifications',
          //   iconColor: AppColors.appColorPurple,
          //   fieldKey: 'isNotificationsEnabledForexRisky',
          //   authUser: authUser,
          // ),
          // _buildNotificationCard(
          //   value: authUser.isNotificationsEnabledStocksRisky,
          //   title: 'Risky Stocks notifications',
          //   iconColor: AppColors.appColorPurple,
          //   fieldKey: 'isNotificationsEnabledStocksRisky',
          //   authUser: authUser,
          // ),
        ],
      ),
    );
  }

  ZCard _buildNotificationCard({
    required bool value,
    required String title,
    required String id,
    required Color iconColor,
    required AuthUser authUser,
  }) {
    return ZCard(
        color: Colors.transparent,
        margin: EdgeInsets.only(left: 16, top: 2, bottom: 2),
        padding: EdgeInsets.zero,
        child: Row(
          children: [
            SvgPicture.asset('assets/svg/notification.svg', colorFilter: ColorFilter.mode(iconColor, BlendMode.srcIn), height: 20, width: 20),
            SizedBox(width: 16),
            Text(title, style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
            Spacer(),
            Switch(
                value: value,
                activeColor: AppCOLORS.primary,
                onChanged: (v) {
                  FirebaseAuthService.updateNofifications(user: authUser, id: id);
                })
          ],
        ));
  }
}

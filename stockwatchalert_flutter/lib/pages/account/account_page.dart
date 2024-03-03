import 'dart:io';

import 'package:firebase_auth/firebase_auth.dart' hide AuthProvider;
import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:signalbyt/pages/_app/onboarding_page.dart';

import '../../components/z_card.dart';
import '../../components/z_upgrade_subscription_card.dart';
import '../../constants/app_colors.dart';
import '../../models/auth_user.dart';
import '../../models_providers/app_controls_provider.dart';
import '../../models_providers/app_provider.dart';
import '../../models_providers/auth_provider.dart';
import '../../models_providers/theme_provider.dart';
import '../../models_services/api_authuser_service.dart';
import '../../models_services/firebase_auth_service.dart';
import '../../utils/z_launch_url.dart';
import 'account_delete_page.dart';

class MyAccountPage extends StatefulWidget {
  MyAccountPage({Key? key}) : super(key: key);

  @override
  State<MyAccountPage> createState() => _MyAccountPageState();
}

class _MyAccountPageState extends State<MyAccountPage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final AuthUser? authUser = authProvider.authUser;

    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final androidLink = appControlsProvider.appControls.linkGooglePlay;
    final iosLink = appControlsProvider.appControls.linkAppStore;
    final shareText = '''Hey check out Stock Watch Alert \n\n${iosLink} \n\n${androidLink}''';

    final storeName = Platform.isAndroid ? 'Google Play' : 'App Store';
    final storeLink = Platform.isAndroid ? androidLink : iosLink;

    return GestureDetector(
      onTap: () {
        FocusScope.of(context).requestFocus(FocusNode());
      },
      child: Scaffold(
        appBar: AppBar(title: Text('My Account')),
        body: ListView(
          padding: EdgeInsets.symmetric(horizontal: 16),
          children: [
            if (authUser?.isAnonymous == false)
              ZCard(
                onTap: () {
                  Get.to(() => AccountDeletePage());
                },
                margin: EdgeInsets.symmetric(vertical: 0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(authUser?.email ?? ''),
                    Spacer(),
                    Icon(Icons.arrow_forward_ios, size: 16),
                  ],
                ),
              ),
            SizedBox(height: 24),
            // ZCard(
            //   child: Text('Onbaording'),
            //   onTap: () => Get.to(() => OnboardingPage1()),
            // ),
            ZUpgradeSubscriptionCard(),
            SizedBox(height: 24),
            AccountNotificationItem(svgPath: 'assets/svg/notification.svg', title: 'Enable general notifications'),
            SizedBox(height: 24),
            AccountItem(svgPath: 'assets/svg/smile.svg', title: 'Rate on ${storeName}', onTap: () async => await ZLaunchUrl.launchUrl(storeLink)),
            SizedBox(height: 16),
            AccountItem(svgPath: 'assets/svg/share.svg', title: 'Share with friends', onTap: () async => await Share.share(shareText)),
            SizedBox(height: 24),
            AccountItemLogout(svgPath: 'assets/svg/logout.svg', title: 'Logout'),
            _buildSignIn(),
            FollowUs()
          ],
        ),
      ),
    );
  }

  _buildSignIn() {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    if (authProvider.authUser?.isAnonymous == false) return Container();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(),
        Container(margin: EdgeInsets.symmetric(horizontal: 0, vertical: 16), child: Text('Want to sync between devices?')),
        if (Platform.isIOS)
          ZCard(
              onTap: () async {
                try {
                  User? fbUser = FirebaseAuth.instance.currentUser;
                  String? jsonWebToken = await fbUser?.getIdToken();

                  await FirebaseAuthService.signInWithApple();

                  if (fbUser != null && jsonWebToken != null) {
                    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context, listen: false);
                    ApiAuthUserService.deleteAccountFbUserJsonWebToken(fbUser, jsonWebToken, appControlsProvider.appControls.apiUrl);
                  }

                  Provider.of<AppProvider>(context, listen: false).cancleAllStreams();
                  await Provider.of<AuthProvider>(context, listen: false).initReload();
                } catch (e) {
                  print(e);
                }
              },
              margin: EdgeInsets.symmetric(horizontal: 0),
              color: Colors.white,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset('assets/images/apple.png', width: 20, height: 20),
                  SizedBox(width: 4),
                  Text('Sign in with Apple', style: TextStyle(color: Colors.black, fontSize: 13))
                ],
              )),
        SizedBox(height: 16),
        ZCard(
            onTap: () async {
              try {
                User? fbUser = FirebaseAuth.instance.currentUser;
                String? jsonWebToken = await fbUser?.getIdToken();

                await FirebaseAuthService.signInWithGoogle();

                if (fbUser != null && jsonWebToken != null) {
                  AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context, listen: false);
                  ApiAuthUserService.deleteAccountFbUserJsonWebToken(fbUser, jsonWebToken, appControlsProvider.appControls.apiUrl);
                }

                Provider.of<AppProvider>(context, listen: false).cancleAllStreams();
                await Provider.of<AuthProvider>(context, listen: false).initReload();
              } catch (e) {
                print(e);
              }
            },
            margin: EdgeInsets.symmetric(horizontal: 0),
            color: Colors.white,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset('assets/images/google.png', width: 20, height: 20),
                SizedBox(width: 4),
                Text('Sign in with Google', style: TextStyle(color: Colors.black, fontSize: 13))
              ],
            )),
      ],
    );
  }

  Color getIconColor(int index) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    Color color = isLightTheme ? Colors.black54 : Colors.white60;
    return color;
  }
}

class FollowUs extends StatelessWidget {
  const FollowUs({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final appControls = appControlsProvider.appControls;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(height: 16),
        Container(margin: EdgeInsets.symmetric(horizontal: 0, vertical: 8), child: Text('Links:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900))),
        Column(
          children: [
            if (appControls.linkGooglePlay != '')
              if (Platform.isAndroid)
                ZSocialMedia(
                  text: 'Google Play',
                  bgColor: AppColors.blue,
                  icon: AntDesign.google,
                  onTap: () => ZLaunchUrl.launchUrl(appControls.linkGooglePlay),
                ),
            if (appControls.linkAppStore != '')
              ZSocialMedia(
                text: 'App Store',
                bgColor: Colors.grey,
                icon: AntDesign.apple_o,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkAppStore),
              ),
            if (appControls.linkInstagram != '')
              ZSocialMedia(
                text: 'Instagram',
                bgColor: AppColors.pink,
                icon: AntDesign.instagram,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkInstagram),
              ),
            if (appControls.linkTelegram != '')
              ZSocialMedia(
                text: 'Telegram',
                bgColor: AppColors.blue,
                icon: AntDesign.message1,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkTelegram),
              ),
            if (appControls.linkWhatsapp != '')
              ZSocialMedia(
                text: 'WhatsApp',
                bgColor: AppColors.green,
                icon: AntDesign.message1,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkWhatsapp),
              ),
            if (appControls.linkYoutube != '')
              ZSocialMedia(
                text: 'Youtube',
                bgColor: AppColors.red,
                icon: AntDesign.youtube,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkYoutube),
              ),
            if (appControls.linkTwitter != '')
              ZSocialMedia(
                text: 'Twitter',
                bgColor: AppColors.blue,
                icon: AntDesign.twitter,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkTwitter),
              ),
            if (appControls.linkSupport != '')
              ZSocialMedia(
                text: 'Support',
                bgColor: Color(0xffFFBD24),
                iconColor: Colors.black,
                textStyle: TextStyle(color: Colors.black),
                icon: AntDesign.user,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkSupport),
              ),
            if (appControls.linkTerms != '')
              ZSocialMedia(
                text: 'Terms',
                bgColor: Color(0xffFFBD24),
                iconColor: Colors.black,
                textStyle: TextStyle(color: Colors.black),
                icon: AntDesign.lock,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkTerms),
              ),
            if (appControls.linkPivacy != '')
              ZSocialMedia(
                text: 'Privacy',
                bgColor: Color(0xffFFBD24),
                iconColor: Colors.black,
                textStyle: TextStyle(color: Colors.black),
                icon: AntDesign.eyeo,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkPivacy),
              ),
          ],
        ),
      ],
    );
  }
}

class ZSocialMedia extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color bgColor;
  final Color? iconColor;
  final TextStyle? textStyle;
  final Function() onTap;

  ZSocialMedia({
    Key? key,
    required this.icon,
    required this.text,
    required this.bgColor,
    required this.onTap,
    this.textStyle,
    this.iconColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        margin: EdgeInsets.symmetric(horizontal: 0, vertical: 8),
        decoration: BoxDecoration(color: bgColor, borderRadius: BorderRadius.circular(8)),
        child: Row(
          children: [
            Icon(icon, color: iconColor),
            SizedBox(width: 8),
            if (textStyle != null) Text(text, style: textStyle),
            if (textStyle == null) Text(text),
          ],
        ),
      ),
    );
  }
}

class SectionHeader extends StatelessWidget {
  const SectionHeader({super.key, required this.title});
  final title;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 16),
      child: Row(
        children: [
          Text(title, style: TextStyle(color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(.7))),
          SizedBox(width: 16),
          Expanded(child: Divider(thickness: 1, height: 1))
        ],
      ),
    );
  }
}

class AccountThemeItem extends StatelessWidget {
  AccountThemeItem({super.key, required this.svgPath, required this.title, this.showRightArrow = true});
  final String svgPath;
  final String title;
  final bool showRightArrow;

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    final isDarkTheme = themeProvider.themeMode != ThemeMode.light;
    return GestureDetector(
      onTap: () => themeProvider.themeMode = isDarkTheme ? ThemeMode.light : ThemeMode.dark,
      child: Container(
        color: Colors.transparent,
        child: Row(
          children: [
            SvgPicture.asset(svgPath, colorFilter: ColorFilter.mode(context.isDarkMode ? Colors.white : Colors.black, BlendMode.srcIn), height: 18, width: 18),
            SizedBox(width: 16),
            Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            Spacer(),
            SizedBox(
              height: 24.0,
              width: 24.0,
              child: Switch(
                value: isDarkTheme,
                onChanged: (v) async {
                  themeProvider.themeMode = isDarkTheme ? ThemeMode.light : ThemeMode.dark;
                },
              ),
            ),
            SizedBox(width: 8),
          ],
        ),
      ),
    );
  }
}

class AccountNotificationItem extends StatelessWidget {
  AccountNotificationItem({super.key, required this.svgPath, required this.title, this.showRightArrow = true});
  final String svgPath;
  final String title;
  final bool showRightArrow;

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    final isDarkTheme = themeProvider.themeMode != ThemeMode.light;
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final AuthUser? authUser = authProvider.authUser;

    if (authUser == null) return Container();

    return GestureDetector(
      onTap: () => themeProvider.themeMode = isDarkTheme ? ThemeMode.light : ThemeMode.dark,
      child: Container(
        color: Colors.transparent,
        child: Row(
          children: [
            SvgPicture.asset(svgPath, colorFilter: ColorFilter.mode(context.isDarkMode ? Colors.white : Colors.black, BlendMode.srcIn), height: 18, width: 18),
            SizedBox(width: 16),
            Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            Spacer(),
            SizedBox(
              height: 24.0,
              width: 24.0,
              child: Switch(
                activeColor: AppColors.green,
                value: !authUser.notificationsDisabled.contains('general'),
                onChanged: (v) async {
                  FirebaseAuthService.updateNofifications(user: authUser, id: 'general');
                },
              ),
            ),
            SizedBox(width: 8),
          ],
        ),
      ),
    );
  }
}

class AccountItem extends StatelessWidget {
  AccountItem({super.key, required this.svgPath, required this.title, this.rightIcon, this.onTap});
  final String svgPath;
  final String title;
  final Widget? rightIcon;
  final Function? onTap;

  @override
  Widget build(BuildContext context) {
    return ZCard(
      margin: EdgeInsets.symmetric(),
      padding: EdgeInsets.symmetric(vertical: 8, horizontal: 0),
      color: Colors.transparent,
      borderRadiusColor: Colors.transparent,
      onTap: () {
        if (onTap != null) onTap!();
      },
      child: Container(
        color: Colors.transparent,
        child: Row(
          children: [
            SvgPicture.asset(svgPath, colorFilter: ColorFilter.mode(context.isDarkMode ? Colors.white : Colors.black, BlendMode.srcIn), height: 18, width: 18),
            SizedBox(width: 16),
            Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
            Spacer(),
            SizedBox(width: 8),
            if (rightIcon != null) rightIcon!,
          ],
        ),
      ),
    );
  }
}

class AccountItemLogout extends StatelessWidget {
  AccountItemLogout({super.key, required this.svgPath, required this.title, this.subtitle, this.showRightArrow = true});
  final String svgPath;
  final String title;
  final String? subtitle;
  final bool showRightArrow;

  @override
  Widget build(BuildContext context) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final AuthUser? authUser = authProvider.authUser;

    if (authUser?.isAnonymous == true) return Container();

    return ZCard(
      padding: EdgeInsets.symmetric(vertical: 0),
      margin: EdgeInsets.zero,
      color: Colors.transparent,
      borderRadiusColor: Colors.transparent,
      borderWidth: 0,
      onTap: () async {
        Provider.of<AppProvider>(context, listen: false).cancleAllStreams();
        await Provider.of<AuthProvider>(context, listen: false).signOut();
        await Provider.of<AuthProvider>(context, listen: false).initReload();
      },
      child: Row(
        children: [
          SvgPicture.asset(svgPath, colorFilter: ColorFilter.mode(AppColors.red, BlendMode.srcIn), height: 16, width: 16),
          SizedBox(width: 16),
          Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: AppColors.red)),
          Spacer(),
          if (subtitle != null) Text(subtitle!, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
          SizedBox(width: 24),
        ],
      ),
    );
  }
}
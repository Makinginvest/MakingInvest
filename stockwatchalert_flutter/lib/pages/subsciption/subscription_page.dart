import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import 'package:stockwatchalert/constants/app_colors.dart';

import '../../components/z_button.dart';
import '../../components/z_card.dart';
import '../../models_providers/app_controls_provider.dart';
import '../../models_providers/auth_provider.dart';
import '../../utils/z_launch_url.dart';

class SubscriptionPage extends StatefulWidget {
  SubscriptionPage({Key? key, this.isOnboarding = false}) : super(key: key);
  final bool isOnboarding;

  @override
  _SubscriptionPageState createState() => _SubscriptionPageState();
}

class _SubscriptionPageState extends State<SubscriptionPage> {
  bool isLoading = false;

  @override
  void initState() {
    Future.microtask(() => Provider.of<AuthProvider>(context, listen: false).checkPurchasesStatus(getPackages: true));
    super.initState();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // backgroundColor: Colors.black,
      extendBody: true,
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        // backgroundColor: Colors.transparent,
        actions: [
          if (widget.isOnboarding)
            ZCard(
              margin: EdgeInsets.zero,
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Text('Skip', style: TextStyle(fontWeight: FontWeight.bold)),
              onTap: () async {
                await Provider.of<AuthProvider>(context, listen: false).init();
              },
            ),
          SizedBox(width: 16),
        ],
      ),
      body: Stack(
        children: [
          _buildBody(),
          if (isLoading)
            GestureDetector(
              onDoubleTap: () => setState(() => isLoading = false),
              child: Container(
                color: Colors.black.withOpacity(0.1),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Row(),
                    SizedBox(height: 30, width: 30, child: CircularProgressIndicator(color: Colors.orange)),
                    SizedBox(height: Get.height * 0.225),
                  ],
                ),
              ),
            )
        ],
      ),
    );
  }

  _buildBody() {
    final authProvider = Provider.of<AuthProvider>(context);
    final entitlementInfos = authProvider.entitlementInfo;
    final isLoadingEntitlementInfo = authProvider.isLoadingEntitlementInfo;
    final packages = authProvider.packages;

    // if (null == null) return _buildNoSubscription(packages);
    if (isLoadingEntitlementInfo) return _buildLoading();
    if (authProvider.authUser!.hasLifetime) return _buildSubscriptionLifetime();
    if (entitlementInfos == null) return _buildNoSubscription(packages);
    return _buildSubscription();
  }

  Column _buildLoading() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Row(),
        SizedBox(child: CircularProgressIndicator(color: Colors.white), height: 20, width: 20),
        SizedBox(height: 8),
        Text('loading...'),
        SizedBox(height: 50),
      ],
    );
  }

  _buildNoSubscription(List<Package> packages) {
    final authProvider = Provider.of<AuthProvider>(context);
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final appControls = appControlsProvider.appControls;
    final selectedPackageId = authProvider.selectedPackageId;
    return Scaffold(
      body: ListView(
        children: [
          Container(
            margin: EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Unlock all premium signals',
                  style: TextStyle(fontSize: 20),
                ),
                Text(
                  'Unlock Crypto, Forex and Stock Signals',
                  style: TextStyle(fontSize: 14),
                ),
              ],
            ),
          ),
          SizedBox(height: 16),
          for (var package in packages)
            ZCard(
              onTap: () {
                authProvider.selectedPackageId = package.identifier;
                setState(() {});
              },
              borderRadiusColor: selectedPackageId == package.identifier ? AppColors.green : Color(0xFF2C2F38),
              borderWidth: 1.5,
              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              color: Colors.transparent,
              child: Container(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(getPackageType1(package), style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                        Spacer(),
                        if (selectedPackageId == package.identifier) Icon(Icons.check_circle_outline, color: AppColors.green),
                        if (selectedPackageId != package.identifier) Icon(Icons.circle_outlined, color: Colors.white30),
                      ],
                    ),
                    SizedBox(height: 4),
                    Row(
                      children: [
                        Text('${package.storeProduct.priceString}', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700)),
                        getPackageType2(package) == 'lifetime' ? Text('') : Text(' / ' + getPackageType2(package), style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                        Spacer(),
                        if (package.packageType != PackageType.annual)
                          Container(
                            decoration: BoxDecoration(color: AppColors.gray, borderRadius: BorderRadius.circular(0)),
                            padding: EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            child: Text('Standard', style: TextStyle(fontSize: 14, color: Colors.white, fontWeight: FontWeight.w700, height: 0)),
                          ),
                        if (package.packageType == PackageType.annual)
                          Transform(
                            transform: Matrix4.rotationZ(-0.05),
                            child: Container(
                              decoration: BoxDecoration(color: AppColors.green, borderRadius: BorderRadius.circular(0)),
                              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              child: Text('Best Price!', style: TextStyle(fontSize: 14, color: Colors.white, fontWeight: FontWeight.w700)),
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          SizedBox(height: 16),
          GestureDetector(
            onTap: () {
              if (authProvider.selectedPackage != null) {
                purchasePackage(authProvider.selectedPackage!);
              }
            },
            child: Stack(
              alignment: AlignmentDirectional.centerEnd,
              children: [
                ZButton(
                  borderRadius: BorderRadius.circular(20),
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  isLoading: authProvider.isloadingRestorePurchases,
                  text: 'Subscribe',
                  backgroundColor: AppColors.green,
                  onTap: () {
                    if (authProvider.selectedPackage != null) {
                      purchasePackage(authProvider.selectedPackage!);
                    }
                  },
                ),
                Container(child: Icon(Icons.arrow_forward_outlined), margin: EdgeInsets.only(right: 32)),
              ],
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ZCard(
                margin: EdgeInsets.symmetric(),
                borderRadiusColor: Colors.transparent,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkPivacy),
                shadowColor: Colors.transparent,
                color: Colors.transparent,
                child: Text('Privacy Policy', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12.5)),
              ),
              ZCard(
                margin: EdgeInsets.symmetric(),
                borderRadiusColor: Colors.transparent,
                onTap: () => ZLaunchUrl.launchUrl(appControls.linkTerms),
                color: Colors.transparent,
                shadowColor: Colors.transparent,
                child: Text('Term of Use', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12.5)),
              ),
              if (!authProvider.authUser!.hasActiveSubscription)
                ZCard(
                  margin: EdgeInsets.symmetric(),
                  borderRadiusColor: Colors.transparent,
                  onTap: () => authProvider.restorePurchases(),
                  color: Colors.transparent,
                  shadowColor: Colors.transparent,
                  child: Text('Restore purchases', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 12.5)),
                ),
            ],
          ),
          SizedBox(height: 8),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 20),
            child: Text(
              'The subcription is renewed automatically no longer than 24 hours before the end of the current period. You can cancel the renewal in your ${Platform.isAndroid ? 'Google Play' : 'App Store'}  account settings at anytime.',
              textAlign: TextAlign.center,
            ),
          ),
          SizedBox(height: 8),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 20),
            child: Text(
              'For futher information about price plan, you can contact me via Telegram by tapping the contact button below',
              textAlign: TextAlign.center,
            ),
          ),
          SizedBox(height: 0),
          Center(
              child: ZCard(
                  onTap: () => ZLaunchUrl.launchUrl(appControls.linkTelegram),
                  color: AppColors.green,
                  padding: EdgeInsets.symmetric(horizontal: 32, vertical: 8),
                  borderRadius: BorderRadius.circular(20),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(AntDesign.message1),
                      SizedBox(width: 8),
                      Text('Contact me', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900)),
                    ],
                  ))),
          SizedBox(height: 32),
        ],
      ),
    );
  }

  _buildSubscriptionLifetime() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(),
        Image.asset('assets/images/active_subscription.png', height: 300),
        SizedBox(height: 24),
        Text('Congrats you have a lifetime subscription', style: TextStyle(fontSize: 16)),
        SizedBox(height: 8),
        Text('Continue using premium features!', style: TextStyle(fontSize: 16)),
        SizedBox(height: Get.height * 0.1),
        SizedBox(height: Get.height * 0.15),
      ],
    );
  }

  _buildSubscription() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Row(),
        Image.asset('assets/images/active_subscription.png', height: 300),
        SizedBox(height: 24),
        Text(
          'You have an active \nsubscription',
          style: TextStyle(fontSize: 16),
          textAlign: TextAlign.center,
        ),
        SizedBox(height: Get.height * 0.1),
        SizedBox(height: Get.height * 0.15),
      ],
    );
  }

  removeAppNameFromString(String string) {
    // remove anything with ()
    string = string.replaceAll(RegExp(r"\(.*\)"), "");
    return string;
  }

  void purchasePackage(Package package) async {
    try {
      isLoading = true;
      setState(() => isLoading = true);
      await Purchases.purchasePackage(package);
      setState(() => isLoading = false);
    } catch (e) {
      setState(() => isLoading = false);
      print(e);
    }
  }

  getCardColor(Package package) {
    if (package.packageType == PackageType.monthly) return Colors.lightBlue.shade300;
    if (package.packageType == PackageType.annual) return Colors.purple.shade400;
    return Colors.green.shade400;
  }

  getPricePeriod(Package package) {
    if (package.packageType == PackageType.monthly) return '${package.storeProduct.priceString}/m';
    if (package.packageType == PackageType.annual) return '${package.storeProduct.priceString}/yr';
    return 'yearly';
  }

  getYearlyPackage(packages) {
    return packages.firstWhere((element) => element.packageType == PackageType.annual);
  }

  String getPackageType1(Package package) {
    if (package.packageType == PackageType.monthly) return 'Monthly';
    if (package.packageType == PackageType.annual) return 'Annual';
    if (package.packageType == PackageType.sixMonth) return '6 Months';
    if (package.packageType == PackageType.threeMonth) return '3 Months';
    if (package.packageType == PackageType.weekly) return 'Weekly';
    if (package.packageType == PackageType.lifetime) return 'Lifetime';
    if (package.packageType == PackageType.twoMonth) return '2 Months';
    if (package.packageType == PackageType.custom) return 'Custom';
    return 'Unknown';
  }

  String getPackageType2(Package package) {
    if (package.packageType == PackageType.monthly) return 'month';
    if (package.packageType == PackageType.annual) return 'year';
    if (package.packageType == PackageType.sixMonth) return '6 months';
    if (package.packageType == PackageType.threeMonth) return '3 months';
    if (package.packageType == PackageType.weekly) return 'weekly';
    if (package.packageType == PackageType.lifetime) return 'lifetime';
    if (package.packageType == PackageType.twoMonth) return '2 months';
    if (package.packageType == PackageType.custom) return 'custom';
    return 'unknown';
  }
}

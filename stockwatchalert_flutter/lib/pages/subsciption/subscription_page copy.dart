import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import 'package:stockwatchalert/components/z_appbar_title.dart';

import '../../components/z_card.dart';

import '../../constants/app_colors.dart';
import '../../models_providers/app_controls_provider.dart';
import '../../models_providers/auth_provider.dart';
import '../../utils/z_launch_url.dart';

class SubscriptionPage extends StatefulWidget {
  const SubscriptionPage({Key? key}) : super(key: key);

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
      extendBody: true,
      appBar: AppBar(title: AppBarTitle()),
      body: _buildBody(),
    );
  }

  _buildBody() {
    final authProvider = Provider.of<AuthProvider>(context);
    final entitlementInfos = authProvider.entitlementInfo;
    final isLoadingEntitlementInfo = authProvider.isLoadingEntitlementInfo;
    final packages = authProvider.packages;

    // if (null == null) return _buildNoSubscription(packages);
    if (isLoadingEntitlementInfo) return _buildLoadingSubscriptions();
    if (authProvider.authUser!.hasLifetime) return _buildSubscriptionLifetime();
    if (entitlementInfos == null) return _buildNoSubscription(packages);
    return _buildSubscription();
  }

  Column _buildLoadingSubscriptions() {
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

    return Stack(
      children: [
        Scaffold(
          body: ListView(
            children: [
              Container(
                margin: EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Let\'s gain profit',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'Unlock all premium signals',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 20),
                    ),
                    Text(
                      'Unlock Crypto, Forex and Stock signals',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 20),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 16),
              for (var package in sortPackages(packages))
                ZCard(
                  onTap: () {
                    if (!isLoading) purchasePackage(package);
                  },
                  borderRadiusColor: package.packageType == PackageType.monthly ? AppColors.blue : null,
                  color: package.packageType == PackageType.monthly ? AppColors.blue : null,
                  child: Row(children: [
                    Image.asset('assets/images/icon_subscription_thumbs_up.png', width: 40, height: 40),
                    SizedBox(width: 16),
                    Container(
                      width: MediaQuery.of(context).size.width * .675,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('${package.storeProduct.priceString}', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900)),
                          SizedBox(height: 2),
                          _buildPackageDescription2(package),
                        ],
                      ),
                    )
                  ]),
                ),

              SizedBox(height: 8),
              if (authProvider.authUser?.hasActiveSubscription == false)
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ZCard(
                      margin: EdgeInsets.zero,
                      color: Colors.transparent,
                      child: Text('Restore Purchases', style: TextStyle(color: AppColors.blue)),
                      onTap: () => authProvider.restorePurchases(),
                    ),
                  ],
                ),
              SizedBox(height: 8),
              Container(
                margin: EdgeInsets.symmetric(horizontal: 40),
                child: Text(
                  'By purchasing any subscription you will unlock all premium signals.',
                  textAlign: TextAlign.center,
                ),
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
                margin: EdgeInsets.symmetric(horizontal: 58),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ZCard(
                      margin: EdgeInsets.zero,
                      onTap: () {
                        ZLaunchUrl.launchUrl(appControls.linkPivacy);
                      },
                      color: Colors.transparent,
                      child: Text('Privacy Policy', style: TextStyle(color: Color(0xFFC1C1C1))),
                    ),
                    Spacer(),
                    ZCard(
                      margin: EdgeInsets.zero,
                      onTap: () {
                        ZLaunchUrl.launchUrl(appControls.linkTerms);
                      },
                      color: Colors.transparent,
                      child: Text('Terms of Use', style: TextStyle(color: Color(0xFFC1C1C1))),
                    ),
                  ],
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
              SizedBox(height: 16),
              Center(
                  child: ZCard(
                      onTap: () => ZLaunchUrl.launchUrl(appControls.linkTelegram),
                      color: AppColors.blue,
                      padding: EdgeInsets.symmetric(horizontal: 32, vertical: 8),
                      borderRadius: BorderRadius.circular(50),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(AntDesign.message1),
                          SizedBox(width: 8),
                          Text('Contact me', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900)),
                        ],
                      ))),
              // Row(
              //   mainAxisAlignment: MainAxisAlignment.center,
              //   children: [
              //     ZCard(
              //       onTap: () {
              //         ZLaunchUrl.launchUrl(appControls.linkPivacy);
              //       },
              //       color: Colors.transparent,
              //       child: Text('Privacy Policy', style: TextStyle(color: Color(0xFFC1C1C1))),
              //     ),
              //     ZCard(
              //       onTap: () {
              //         ZLaunchUrl.launchUrl(appControls.linkTerms);
              //       },
              //       color: Colors.transparent,
              //       child: Text('Term of Use', style: TextStyle(color: Color(0xFFC1C1C1))),
              //     ),
              //   ],
              // ),
              SizedBox(height: 32),
            ],
          ),
        ),
      ],
    );
  }

  _buildSubscriptionLifetime() {
    final authProvider = Provider.of<AuthProvider>(context);
    final authUser = authProvider.authUser;
    if (authUser == null) return Container();

    if (authUser.subIsLifetime)
      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Row(),
          SvgPicture.asset('assets/svg/subscription-stars.svg', height: 140, width: 140),
          SizedBox(height: 24),
          Text('You have an active \nsubscription', style: TextStyle(fontSize: 32, color: AppColors.green, fontWeight: FontWeight.w900), textAlign: TextAlign.center),
          SizedBox(height: 16),
          if (authUser.subIsLifetimeExpirationDateTime == null) Text('Subscription valid forever', textAlign: TextAlign.center),
          if (authUser.subIsLifetimeExpirationDateTime != null) Text('Subscription valid until ${authUser.getSubscriptionEndDateTime()}'),
          SizedBox(height: Get.height * 0.15),
        ],
      );

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
    final authProvider = Provider.of<AuthProvider>(context);
    final authUser = authProvider.authUser;
    if (authUser == null) return Container();

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Row(),
        Image.asset('assets/images/active_subscription.png', height: 300),
        SizedBox(height: 24),
        Text('You have an active subscription', style: TextStyle(fontSize: 16), textAlign: TextAlign.center),
        Text('Subscription until: ${authUser.getSubscriptionEndDateTime()}', textAlign: TextAlign.center),
        SizedBox(height: Get.height * 0.15),
      ],
    );
  }

  List<Package> sortPackages(List<Package> ps) {
    List<Package> sorted = [];
    ps.forEach((p) {
      if (p.packageType == PackageType.weekly) sorted.add(p);
    });
    ps.forEach((p) {
      if (p.packageType == PackageType.monthly) sorted.add(p);
    });
    ps.forEach((p) {
      if (p.packageType == PackageType.threeMonth) sorted.add(p);
    });
    ps.forEach((p) {
      if (p.packageType == PackageType.sixMonth) sorted.add(p);
    });
    ps.forEach((p) {
      if (p.packageType == PackageType.annual) sorted.add(p);
    });
    return sorted;
  }

  checkIfStringContainsString(String string, String substring) {
    return string.toLowerCase().contains(substring.toLowerCase());
  }

  _buildPackageDescription2(Package package) {
    String discription = package.storeProduct.title;
    // check for and remove () text can be in the middle of ()
    // regex to remove () text
    RegExp exp = new RegExp(r"\(.*?\)");
    discription = discription.replaceAll(exp, '');

    return Text(discription, style: TextStyle(fontSize: 14));
  }

  checkIfStringContainsStringAndRemove(String string, String substring) {
    if (string.toLowerCase().contains(substring.toLowerCase())) {
      return string.replaceAll(substring, '');
    }
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
    return Colors.blue.shade400;
  }

  getPricePeriod(Package package) {
    if (package.packageType == PackageType.monthly) return '${package.storeProduct.priceString}/m';
    if (package.packageType == PackageType.annual) return '${package.storeProduct.priceString}/yr';
    return 'yearly';
  }

  getYearlyPackage(packages) {
    return packages.firstWhere((element) => element.packageType == PackageType.annual);
  }
}

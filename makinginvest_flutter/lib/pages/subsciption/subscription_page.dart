import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:purchases_flutter/purchases_flutter.dart';

import '../../components/z_button.dart';
import '../../components/z_card.dart';
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
      appBar: AppBar(
        title: Text('Upgrade'),
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

    if (isLoadingEntitlementInfo) return _buildLoading();
    // if (null == null) return _buildNoSubscription(packages);
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
    // final AppControlLinks appControlLinks = appProvider.appControlLinks;
    return Stack(
      children: [
        Scaffold(
          body: ListView(
            children: [
              SizedBox(height: 16),
              Container(
                margin: EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SizedBox(height: 16),
                    Text('Maximize Your Opportunities with a Plan Tailored to Your Success! 🚀.', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
              SizedBox(height: 16),
              for (var package in packages)
                ZCard(
                  onTap: () => purchasePackage(package),
                  borderRadiusColor: Color(0xFF2C2F38),
                  color: Colors.transparent,
                  child: Row(children: [
                    Image.asset('assets/images/icon_subscription_thumbs_up.png', width: 40, height: 40),
                    SizedBox(width: 16),
                    Container(
                      width: MediaQuery.of(context).size.width * .675,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('${package.storeProduct.priceString}'),
                          SizedBox(height: 4),
                          Text(
                            removeAppNameFromString(package.storeProduct.description != '' ? package.storeProduct.description : package.storeProduct.title),
                          ),
                        ],
                      ),
                    )
                  ]),
                ),
              SizedBox(height: 16),
              Container(
                margin: EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                        "You'll receive a complimentary three-day free trial to explore all the features. This plan provides full access to our essential features, including real-time trading signals for Forex, cryptocurrencies, and stocks",
                        style: TextStyle(fontSize: 13)),
                    SizedBox(height: 6),
                    Text('Enjoy a comprehensive video learning section and a detailed trading guide to hone your trading skills.', style: TextStyle(fontSize: 13)),
                    SizedBox(height: 6),
                    Text('Stay informed with our Crypto ICO analysis, economic updates, and exclusive trading events.', style: TextStyle(fontSize: 13)),
                  ],
                ),
              ),
              SizedBox(height: 16),
              if (!authProvider.authUser!.hasActiveSubscription)
                ZButton(
                  margin: EdgeInsets.symmetric(horizontal: 32, vertical: 8),
                  isLoading: authProvider.isloadingRestorePurchases,
                  text: 'Restore Purchases',
                  onTap: () => authProvider.restorePurchases(),
                ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ZCard(
                    onTap: () {
                      ZLaunchUrl.launchUrl(appControls.linkPivacy);
                    },
                    color: Colors.transparent,
                    child: Text('Privacy Policy', style: TextStyle(color: Color(0xFFC1C1C1))),
                  ),
                  ZCard(
                    onTap: () {
                      ZLaunchUrl.launchUrl(appControls.linkTerms);
                    },
                    color: Colors.transparent,
                    child: Text('Term of Use', style: TextStyle(color: Color(0xFFC1C1C1))),
                  ),
                ],
              ),
              SizedBox(height: 32),
            ],
          ),
        ),
      ],
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

  // _buildPackageDescriptionHeader(Package package) {
  //   String packageType = '';
  //   if (package.packageType == PackageType.weekly) packageType = 'Weekly';
  //   if (package.packageType == PackageType.monthly) packageType = 'Monthly';
  //   if (package.packageType == PackageType.threeMonth) packageType = '3 Months';
  //   if (package.packageType == PackageType.sixMonth) packageType = '6 Months';
  //   if (package.packageType == PackageType.annual) packageType = 'Annual';

  //   String packageName = packageType + ' ' + 'Premium';

  //   return Text(packageName, style: TextStyle(fontSize: 14));
  // }

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

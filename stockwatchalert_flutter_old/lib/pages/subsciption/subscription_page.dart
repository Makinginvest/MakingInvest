import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import 'package:signalbyt/constants/app_colors.dart';

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
      backgroundColor: Colors.black,
      extendBody: true,
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        actions: [
          if (widget.isOnboarding)
            TextButton(
              onPressed: () async {
                await Provider.of<AuthProvider>(context, listen: false).init();
              },
              child: Text('Skip', style: TextStyle(color: Colors.white)),
            ),
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
    final selectedPackageId = authProvider.selectedPackageId;
    return Stack(
      children: [
        Scaffold(
          backgroundColor: Colors.black,
          body: ListView(
            children: [
              SvgPicture.asset('assets/svg/header-btc.svg', height: 140, width: double.infinity),
              SizedBox(height: 32),
              /* ------------------------------- Pro access ------------------------------- */
              Container(
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  children: [
                    Text('Get', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w800)),
                    SizedBox(width: 6),
                    Container(
                      child: Text('Pro', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w800)),
                      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.green,
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    SizedBox(width: 6),
                    Text('Access', style: TextStyle(fontSize: 28, fontWeight: FontWeight.w800)),
                  ],
                ),
              ),
              /* -------------------------- NEWS ANALYSIS SIGNALS ------------------------- */
              Container(
                margin: EdgeInsets.symmetric(vertical: 16),
                child: Row(
                  children: [
                    Expanded(
                      child: ZCard(
                          height: 60,
                          borderRadiusColor: Colors.transparent,
                          borderRadius: BorderRadius.circular(10),
                          margin: EdgeInsets.symmetric(),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SvgPicture.asset('assets/svg/news.svg', height: 20, width: 20),
                              SizedBox(width: 6),
                              Text('News', style: TextStyle(height: 1), textAlign: TextAlign.center),
                            ],
                          )),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: ZCard(
                          height: 60,
                          borderRadiusColor: Colors.transparent,
                          borderRadius: BorderRadius.circular(10),
                          margin: EdgeInsets.symmetric(),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SvgPicture.asset('assets/svg/rocket.svg', height: 20, width: 20),
                              SizedBox(width: 4),
                              Text('AI \nSignals', style: TextStyle(height: 1), textAlign: TextAlign.center),
                            ],
                          )),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: ZCard(
                          height: 60,
                          borderRadiusColor: Colors.transparent,
                          borderRadius: BorderRadius.circular(10),
                          margin: EdgeInsets.symmetric(),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SvgPicture.asset('assets/svg/analysis.svg', height: 20, width: 20),
                              SizedBox(width: 4),
                              Text('Analysis', style: TextStyle(height: 1), textAlign: TextAlign.center),
                            ],
                          )),
                    ),
                  ],
                ),
              ),
              for (var package in packages)
                ZCard(
                  onTap: () {
                    authProvider.selectedPackageId = package.identifier;
                    setState(() {});
                  },
                  borderRadiusColor: selectedPackageId == package.identifier ? AppColors.green : Color(0xFF2C2F38),
                  borderWidth: 2,
                  color: Colors.transparent,
                  child: Container(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Text(getPackageType1(package), style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700)),
                            Spacer(),
                            if (selectedPackageId == package.identifier) Icon(Icons.check_circle_outline, color: AppColors.green),
                            if (selectedPackageId != package.identifier) Icon(Icons.circle_outlined, color: Colors.white30),
                          ],
                        ),
                        SizedBox(height: 6),
                        Row(
                          children: [
                            Text('${package.storeProduct.priceString}', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                            getPackageType2(package) == 'lifetime' ? Text('') : Text(' / ' + getPackageType2(package), style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                            Spacer(),
                            if (package.packageType != PackageType.annual)
                              Container(
                                decoration: BoxDecoration(color: AppColors.gray, borderRadius: BorderRadius.circular(0)),
                                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                child: Text('Standard', style: TextStyle(fontSize: 14, color: Colors.white, fontWeight: FontWeight.w700)),
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
                      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      isLoading: authProvider.isloadingRestorePurchases,
                      text: 'Start 3-Day FREE trial',
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
    if (package.packageType == PackageType.weekly) return 'weekl';
    if (package.packageType == PackageType.lifetime) return 'lifetime';
    if (package.packageType == PackageType.twoMonth) return '2 months';
    if (package.packageType == PackageType.custom) return 'custom';
    return 'unknown';
  }
}

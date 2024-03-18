import 'dart:io';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import 'package:stockwatchalert/models/_parsers.dart';

import '../constants/app_env.dart';

class RevenueCatSevice {
  static String _androidKey = AppENV.REVENUECAT_ANDROID_KEY;
  static String _iosKey = AppENV.REVENUECAT_IOS_KEY;
  static String _apiKey = Platform.isIOS ? _iosKey : _androidKey;
  static final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  static Future init() async {
    try {
      await Purchases.setLogLevel(LogLevel.debug);
      PurchasesConfiguration configuration = PurchasesConfiguration(_apiKey);
      await Purchases.configure(configuration);
    } catch (e) {
      print('error in RevenueCatSevice init: $e');
    }
  }

  static Future<List<Offering>> getOfferings() async {
    try {
      final offering = await Purchases.getOfferings();
      final current = offering.current;
      return current == null ? [] : [current];
    } catch (e) {
      print('getOfferings error: $e');
      return [];
    }
  }

  static Future<List<Package>> getPackages() async {
    try {
      List<Offering> offerings = await RevenueCatSevice.getOfferings();
      final _packages = offerings.map((e) => e.availablePackages).expand((element) => element).toList();
      // sort packages by price
      _packages.sort((a, b) => a.storeProduct.price.compareTo(b.storeProduct.price));
      return _packages;
    } catch (e) {
      return [];
    }
  }

  static Future<bool> purchasePackage(Package package) async {
    try {
      await Purchases.purchasePackage(package);
      return true;
    } catch (e) {
      print('Error package ${e}');
      return false;
    }
  }

  static Future updateUserSub(EntitlementInfo entitlementInfo) async {
    try {
      User? fbUser = FirebaseAuth.instance.currentUser;
      if (fbUser == null) return;

      await _firestore.collection('users').doc(fbUser.uid).update({
        'subRevenuecatBillingIssueDetectedDateTime': parseToDateTime(entitlementInfo.billingIssueDetectedAt),
        'subRevenuecatExpirationDateTime': parseToDateTime(entitlementInfo.expirationDate),
        'subRevenuecatIsActive': entitlementInfo.isActive,
        'subRevenuecatIsSandbox': entitlementInfo.isSandbox,
        'subRevenuecatLatestPurchaseDateTime': parseToDateTime(entitlementInfo.latestPurchaseDate),
        'subRevenuecatOriginalPurchaseDateTime': parseToDateTime(entitlementInfo.originalPurchaseDate),
        'subRevenuecatPeriodType': entitlementInfo.periodType.toString(),
        'subRevenuecatProductIdentifier': entitlementInfo.productIdentifier,
        'subRevenuecatUnsubscribeDetectedDateTime': parseToDateTime(entitlementInfo.unsubscribeDetectedAt),
        'subRevenuecatWillRenew': entitlementInfo.willRenew,
      });

      return true;
    } catch (e) {
      print('Error package ${e}');
      return false;
    }
  }
}

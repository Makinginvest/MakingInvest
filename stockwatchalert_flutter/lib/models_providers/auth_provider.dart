import 'dart:async';

import 'package:firebase_auth/firebase_auth.dart' hide AuthProvider;
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:purchases_flutter/purchases_flutter.dart';
import 'package:signalbyt/pages/_app/onboarding_page.dart';

import '../models/auth_user.dart';
import '../models_services/_hive_helper.dart';
import '../models_services/api_authuser_service.dart';
import '../models_services/firebase_auth_service.dart';
import '../models_services/revenuecat_service.dart';
import '../pages/_app_navbar_page.dart';
import '../utils/z_utils.dart';

class AuthProvider with ChangeNotifier {
  AuthUser? _authUser;
  AuthUser? get authUser => _authUser;
  StreamSubscription<AuthUser>? _streamSubscriptionAuthUser;

  User? _fbUser;

  Future init({bool isFresh = true}) async {
    _fbUser = await FirebaseAuthService.getFirebaseUser();
    if (_fbUser == null) return;

    _authUser = await FirebaseAuthService.getAuthUser();
    if (_authUser == null) return;
    if (_authUser?.isOnboarded == false) {
      Get.offAll(() => OnboardingPage1());
      return;
    }
    ;

    Get.offAll(() => AppNavbarPage());
    FirebaseAuthService.updateAppVersionLastLogin();
    _setRevenueCatId();

    Stream<AuthUser>? streamAuthUser = FirebaseAuthService.streamAuthUser();
    _streamSubscriptionAuthUser = streamAuthUser?.listen((res) async {
      _authUser = res;

      String apiUrl = await HiveHelper.getApiUrl();
      if (_authUser != null || apiUrl == '') {
        ApiAuthUserService.updateUser(data: {..._authUser!.toJson()}, apiUrl: apiUrl);
      }
      ;
      notifyListeners();
    });

    notifyListeners();
    return _authUser;
  }

  Future initReload() async {
    _fbUser = await FirebaseAuthService.getFirebaseUser();
    if (_fbUser == null) return;

    _streamSubscriptionAuthUser?.cancel();

    Stream<AuthUser>? streamAuthUser = FirebaseAuthService.streamAuthUser();
    _streamSubscriptionAuthUser = streamAuthUser?.listen((res) async {
      _authUser = res;

      String apiUrl = await HiveHelper.getApiUrl();
      if (_authUser != null || apiUrl == '') {
        ApiAuthUserService.updateUser(data: {..._authUser!.toJson()}, apiUrl: apiUrl);
      }
      ;
      notifyListeners();
    });

    _setRevenueCatId();
    FirebaseAuthService.updateAppVersionLastLogin();

    return _authUser;
  }

  void cancleAllStreams() {
    _streamSubscriptionAuthUser?.cancel();
    _authUser = null;
    notifyListeners();
  }

  Future signOut() async {
    await FirebaseAuth.instance.signOut();
    _streamSubscriptionAuthUser?.cancel();
    _authUser = null;
    notifyListeners();
  }

/* ----------------------------- NOTE REVENUECAT ---------------------------- */
  EntitlementInfo? _entitlementInfo;
  EntitlementInfo? get entitlementInfo => _entitlementInfo;
  bool _isloadingRestorePurchases = false;
  bool get isloadingRestorePurchases => _isloadingRestorePurchases;
  String selectedPackageId = '';

  Package? get selectedPackage {
    if (selectedPackageId == '') return null;
    return _packages.firstWhere((element) => element.identifier == selectedPackageId);
  }

  List<Package> _packages = [];
  List<Package> get packages => _packages;

  bool _isLoadingEntitlementInfo = false;
  bool get isLoadingEntitlementInfo => _isLoadingEntitlementInfo;

  void _setRevenueCatId() async {
    try {
      await Purchases.logIn(_fbUser!.uid);
      checkPurchasesStatus();

      Purchases.addCustomerInfoUpdateListener((customerInfo) {
        checkPurchasesStatus();
      });
    } catch (e) {
      print(e);
    }
  }

  void restorePurchases() async {
    try {
      _isloadingRestorePurchases = true;
      notifyListeners();

      await Purchases.restorePurchases();
      checkPurchasesStatus();
      await Future.delayed(Duration(seconds: 2));
      ZUtils.showToastSuccess(message: 'Restore Purchases Success');

      _isloadingRestorePurchases = false;
      notifyListeners();
    } catch (e) {
      checkPurchasesStatus();
      await ZUtils.showToastError(message: 'Restore Purchases Failed');
      _isloadingRestorePurchases = false;
      notifyListeners();
    }
  }

  void checkPurchasesStatus({bool getPackages = false}) async {
    _isLoadingEntitlementInfo = true;
    notifyListeners();

    if (getPackages) {
      _packages = await RevenueCatSevice.getPackages();
      if (packages.isEmpty) {
        selectedPackageId = '';
      } else {
        selectedPackageId = packages[0].identifier;
      }
      print('CALLLED checkPurchasesStatus _packages ${_packages}');
    }

    CustomerInfo info = await Purchases.getCustomerInfo();

    List<EntitlementInfo> _entitlements = info.entitlements.active.values.toList();
    _entitlements.sort((a, b) => b.latestPurchaseDate.compareTo(a.latestPurchaseDate));
    if (_entitlements.isEmpty) _entitlementInfo = null;

    if (_entitlements.length >= 1) {
      _entitlementInfo = _entitlements[0];
      RevenueCatSevice.updateUserSub(_entitlementInfo!);
    }

    List<EntitlementInfo> _entitlementsAll = info.entitlements.all.values.toList();
    _entitlementsAll.sort((a, b) => b.latestPurchaseDate.compareTo(a.latestPurchaseDate));
    if (_entitlements.isEmpty && _entitlementsAll.isNotEmpty) {
      RevenueCatSevice.updateUserSub(_entitlementsAll[0]);
    }

    _isLoadingEntitlementInfo = false;
    notifyListeners();
  }

  checkIfStringContainsString(String string, String substring) {
    return string.toLowerCase().contains(substring.toLowerCase());
  }

  /* ---------------------------- NOTE SYMBOLS TRACKER --------------------------- */

  DateTime? _lastUpdateLastLogin;

  void updateLastLoginAfter6H() async {
    DateTime nowUtc = DateTime.now().toUtc();
    if (_lastUpdateLastLogin == null) {
      _lastUpdateLastLogin = nowUtc;
      return;
    }

    if (_lastUpdateLastLogin != null && nowUtc.difference(_lastUpdateLastLogin!).inHours < 6) return;

    FirebaseAuthService.updateAppVersionLastLogin();
    _lastUpdateLastLogin = nowUtc;
  }
}

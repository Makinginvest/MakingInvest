import 'dart:io';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart' hide AuthProvider;
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:package_info/package_info.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';

import '../../models/auth_user.dart';
import '../../utils/z_utils.dart';
import '../../utils/z_validators.dart';
import 'api_authuser_service.dart';

class FirebaseAuthService {
  static FirebaseAuth _auth = FirebaseAuth.instance;
  static final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  static final FirebaseMessaging _firestoreMessaging = FirebaseMessaging.instance;
  static final String device = Platform.isAndroid ? 'Android' : 'iOS';

/* ---------------------------- NOTE GET AUTHUSER --------------------------- */
  static Future<AuthUser?> getAuthUser() async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) return null;

    var doc = await _firestore.collection('users').doc(fbUser.uid).get();
    return AuthUser.fromJson({...?doc.data(), 'id': doc.id});
  }

  static Future<User?> getFirebaseUser() async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) await signInAnonymously();
    fbUser = FirebaseAuth.instance.currentUser;
    return fbUser;
  }

  /* ---------------------------- NOTE Stream User ---------------------------- */
  static Stream<AuthUser>? streamAuthUser() {
    User? user = FirebaseAuth.instance.currentUser;
    if (user == null) return null;
    var ref = FirebaseFirestore.instance.collection('users').doc(user.uid).snapshots();
    return ref.map((snap) => AuthUser.fromJson({...?snap.data(), 'id': snap.id}));
  }

/* --------------------------- NOTE GOOGLE SIGNIN --------------------------- */
  static Future<User?> signInWithGoogle() async {
    GoogleSignIn _googleSignIn = GoogleSignIn(scopes: ['email']);

    final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
    if (googleUser == null) return null;
    final GoogleSignInAuthentication googleAuth = await googleUser.authentication;

    final AuthCredential credential = GoogleAuthProvider.credential(accessToken: googleAuth.accessToken, idToken: googleAuth.idToken);

    var signInResult = await _auth.signInWithCredential(credential);

    final User? user = signInResult.user;
    if (user == null) return null;

    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    String appVersion = packageInfo.version;
    num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;
    String? token = await _firestoreMessaging.getToken();

    var query = await _firestore.collection('users').doc(user.uid).get();

    if (!query.exists) {
      AuthUser authUser = AuthUser();
      await _firestore.collection('users').doc(user.uid).set({
        ...authUser.toJson(),
        'appBuildNumber': appBuildNumber,
        'appVersion': appVersion,
        'devTokens': FieldValue.arrayUnion([token]),
        'isAnonymous': false,
        'email': user.email,
        'name': '',
        'lastLoginDateTime': DateTime.now(),
        'lastLoginDateTimeDevice': device,
        'createdDateTime': DateTime.now(),
        'lastUpdateDateTime': DateTime.now(),
        'isActive': true,
        'isNotificationsEnabledGeneral': true,
      });
    }

/* ---------------------------- NOTE query exits ---------------------------- */
    if (query.exists) {
      await _firestore.collection('users').doc(user.uid).update({
        'appBuildNumber': appBuildNumber,
        'appVersion': appVersion,
        'isAnonymous': false,
        'devTokens': FieldValue.arrayUnion([token]),
        'email': user.email,
        'lastLoginDateTime': DateTime.now(),
        'lastLoginDateTimeDevice': device,
      });
    }

    query = await _firestore.collection('users').doc(user.uid).get();
    if (query.exists) {
      AuthUser.fromJson({...?query.data(), 'id': query.id});
    }

    return user;
  }

  /* ------------------------ NOTE SIGIN IN WITH APPLE ------------------------ */
  static Future<User?> signInWithApple() async {
    try {
      final appleCredential = await SignInWithApple.getAppleIDCredential(
        scopes: [AppleIDAuthorizationScopes.email, AppleIDAuthorizationScopes.fullName],
      );

      final oauthCredential = OAuthProvider("apple.com").credential(idToken: appleCredential.identityToken);

      final signInResult = await _auth.signInWithCredential(oauthCredential);

      final User? user = signInResult.user;
      if (user == null) return null;

      PackageInfo packageInfo = await PackageInfo.fromPlatform();
      String appVersion = packageInfo.version;
      num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;
      String? token = await _firestoreMessaging.getToken();

      var query = await _firestore.collection('users').doc(user.uid).get();

      if (!query.exists) {
        AuthUser authUser = AuthUser();
        await _firestore.collection('users').doc(user.uid).set({
          ...authUser.toJson(),
          'appBuildNumber': appBuildNumber,
          'isAnonymous': false,
          'appVersion': appVersion,
          'devTokens': FieldValue.arrayUnion([token]),
          'email': user.email,
          'name': '',
          'lastLoginDateTime': DateTime.now(),
          'lastLoginDateTimeDevice': device,
          'createdDateTime': DateTime.now(),
          'lastUpdateDateTime': DateTime.now(),
          'isActive': true,
          'isNotificationsEnabledGeneral': true,
        });
      }
      /* ---------------------------- NOTE query.exists --------------------------- */
      if (query.exists) {
        await _firestore.collection('users').doc(user.uid).update({
          'appBuildNumber': appBuildNumber,
          'isAnonymous': false,
          'appVersion': appVersion,
          'devTokens': FieldValue.arrayUnion([token]),
          'email': user.email,
          'lastLoginDateTime': DateTime.now(),
          'lastLoginDateTimeDevice': device,
        });
      }

      query = await _firestore.collection('users').doc(user.uid).get();
      if (query.exists) {
        AuthUser.fromJson({...?query.data(), 'id': query.id});
      }

      return user;
    } catch (e) {
      return null;
    }
  }

  static Future<User?> signInWithEmailAndPassword({required String email, required String password}) async {
    try {
      UserCredential authResult = await _auth.signInWithEmailAndPassword(email: email, password: password);
      User? user = authResult.user;

      PackageInfo packageInfo = await PackageInfo.fromPlatform();
      String appVersion = packageInfo.version;
      num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;
      String? token = await _firestoreMessaging.getToken();

      AuthUser authUser = AuthUser();
      await _firestore.collection('users').doc(user!.uid).update({
        ...authUser.toJson(),
        'appBuildNumber': appBuildNumber,
        'isAnonymous': false,
        'appVersion': appVersion,
        'devTokens': FieldValue.arrayUnion([token]),
        'lastUpdateDateTime': DateTime.now(),
        'lastLoginDateTime': DateTime.now(),
        'lastLoginDateTimeDevice': device,
      });

      var query = await _firestore.collection('users').doc(user.uid).get();
      if (query.exists) {
        AuthUser.fromJson({...?query.data(), 'id': query.id});
      }

      return user;
    } catch (e) {
      print('signInWithEmailAndPassword error: $e');
      ZUtils.showToastError(message: ZValidators.getMessageFromErrorCode(e));
      return null;
    }
  }

  static Future<User?> signUpWithEmailAndPassword({required String email, required String password}) async {
    try {
      UserCredential authResult = await _auth.createUserWithEmailAndPassword(email: email, password: password);
      User? user = authResult.user;

      PackageInfo packageInfo = await PackageInfo.fromPlatform();
      String appVersion = packageInfo.version;
      num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;
      String? token = await _firestoreMessaging.getToken();

      AuthUser authUser = AuthUser();
      await _firestore.collection('users').doc(user!.uid).set({
        ...authUser.toJson(),
        'appBuildNumber': appBuildNumber,
        'isAnonymous': false,
        'appVersion': appVersion,
        'devTokens': FieldValue.arrayUnion([token]),
        'email': email,
        'name': '',
        'lastLoginDateTime': DateTime.now(),
        'createdDateTime': DateTime.now(),
        'lastUpdateDateTime': DateTime.now(),
        'isActive': true,
        'isAdmin': false,
        'isNotificationsEnabledGeneral': true,
      });

      var query = await _firestore.collection('users').doc(user.uid).get();
      if (query.exists) {
        AuthUser.fromJson({...?query.data(), 'id': query.id});
      }

      return user;
    } catch (e) {
      ZUtils.showToastError(message: ZValidators.getMessageFromErrorCode(e));
      return null;
    }
  }

  static Future<User?> signInAnonymously() async {
    UserCredential userCredential = await _auth.signInAnonymously();
    User? user = userCredential.user;

    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    String appVersion = packageInfo.version;
    num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;
    String? token = await _firestoreMessaging.getToken();

    AuthUser authUser = AuthUser();
    await _firestore.collection('users').doc(user!.uid).set({
      ...authUser.toJson(),
      'appBuildNumber': appBuildNumber,
      'isAnonymous': true,
      'appVersion': appVersion,
      'devTokens': FieldValue.arrayUnion([token]),
      'lastLoginDateTime': DateTime.now(),
      'createdDateTime': DateTime.now(),
      'lastUpdateDateTime': DateTime.now(),
      'isActive': true,
      'isAdmin': false,
      'isNotificationsEnabledGeneral': true,
    });

    return user;
  }

/* --------------------- NOTE Update Appversion Login & dev token --------------------- */
  static Future<void> updateAppVersionLastLogin() async {
    String? currentDevToken = await _firestoreMessaging.getToken();
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) return;

    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    String appVersion = packageInfo.version;
    num appBuildNumber = int.tryParse(packageInfo.buildNumber) ?? 0;

    await _firestore.collection('users').doc(fbUser.uid).set({
      'appBuildNumber': appBuildNumber,
      'appVersion': appVersion,
      'devTokens': FieldValue.arrayUnion([currentDevToken]),
      'lastLoginDateTime': DateTime.now(),
      'lastLoginDateTimeDevice': device,
      'isAnonymous': fbUser.isAnonymous,
    }, SetOptions(merge: true));
  }

  static Future<void> updateFavorite({required String id, required AuthUser user, required String apiUrl}) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) return;

    if (user.favoriteSignals.contains(id)) {
      _firestore.collection('users').doc(fbUser.uid).update({
        'favoriteSignals': FieldValue.arrayRemove([id])
      });
      ApiAuthUserService.updateUser(data: {'favoriteSignals': user.favoriteSignals}, apiUrl: apiUrl);
      return;
    }

    _firestore.collection('users').doc(fbUser.uid).update({
      'favoriteSignals': FieldValue.arrayUnion([id])
    });

    ApiAuthUserService.updateUser(data: {'favoriteSignals': user.favoriteSignals}, apiUrl: apiUrl);
  }

  static Future<void> updateNofifications({required String id, required AuthUser user}) async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) return;

    if (user.notificationsDisabled.contains(id)) {
      _firestore.collection('users').doc(fbUser.uid).update({
        'notificationsDisabled': FieldValue.arrayRemove([id])
      });
      return;
    }

    _firestore.collection('users').doc(fbUser.uid).update({
      'notificationsDisabled': FieldValue.arrayUnion([id])
    });
  }

  static Future<void> setOnboarded() async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) return;

    _firestore.collection('users').doc(fbUser.uid).update({'isOnboarded': true});
  }

/* ------------------------------ NOTE SIGNOUT ------------------------------ */
  static signOut() async {
    User? fbUser = FirebaseAuth.instance.currentUser;
    if (fbUser == null) return;
    _auth.signOut();
  }
}

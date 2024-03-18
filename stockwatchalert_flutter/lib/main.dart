import 'dart:io';

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:get/get.dart';
import 'package:hive/hive.dart';
import 'package:path_provider/path_provider.dart' as path_provider;
import 'package:provider/provider.dart';

import 'models_providers/app_provider.dart';
import 'models_providers/app_controls_provider.dart';
import 'models_providers/auth_provider.dart';
import 'models_providers/navbar_provider.dart';
import 'models_providers/theme_provider.dart';
import 'models_services/firebase_notification_service.dart';
import 'models_services/revenuecat_service.dart';
import 'pages/auth/splash_page.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';
import 'package:easy_localization/easy_localization.dart';

void main() async {
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();
  FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);
  SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(systemNavigationBarColor: Color(0xFF141518), systemNavigationBarIconBrightness: Brightness.light));
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.manual, overlays: [SystemUiOverlay.bottom, SystemUiOverlay.top]);
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp, DeviceOrientation.portraitDown]);

  await EasyLocalization.ensureInitialized();

  await dotenv.load(fileName: ".env");

  HttpOverrides.global = new MyHttpOverrides();

  final appDocumentDirectory = await path_provider.getApplicationDocumentsDirectory();
  Hive.init(appDocumentDirectory.path);

  ThemeMode themeMode = await Themes.getThemeModeHive();

  await Firebase.initializeApp();
  FirebaseNotificationService.init();
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterError;

  await RevenueCatSevice.init();

  runApp(
    EasyLocalization(
      supportedLocales: [Locale('en'), Locale('es'), Locale('ar')],
      path: 'assets/translations',
      fallbackLocale: Locale('en'),
      startLocale: Locale('en'),
      useOnlyLangCode: true,
      child: ChangeNotifierProvider(
        create: (_) => ThemeProvider(themeMode),
        child: MultiProvider(
          providers: [
            ChangeNotifierProvider(create: (context) => NavbarProvider()),
            ChangeNotifierProvider(create: (context) => AuthProvider()),
            ChangeNotifierProxyProvider<AuthProvider, AppProvider>(
              create: (context) => AppProvider(),
              update: (_, authProvider, prev) => prev!..authProvider = authProvider,
            ),
            ChangeNotifierProxyProvider<AuthProvider, AppControlsProvider>(
              create: (context) => AppControlsProvider(),
              update: (_, authProvider, prev) => prev!..authProvider = authProvider,
            ),
          ],
          child: MyApp(),
        ),
      ),
    ),
  );
}

class MyApp extends StatefulWidget {
  const MyApp({
    super.key,
  });

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    // WidgetsBinding.instance.renderView.automaticSystemUiAdjustment = false;
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void didChangeDependencies() {
    Themes.setStatusNavigationBarColor();
    super.didChangeDependencies();
  }

  @override
  didChangeAppLifecycleState(AppLifecycleState state) {
    Themes.setStatusNavigationBarColor();
    if (state == AppLifecycleState.resumed) Provider.of<AppControlsProvider>(context, listen: false).websocketReconnectAppResume();
    super.didChangeAppLifecycleState(state);
  }

  @override
  dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    return GetMaterialApp(
      localizationsDelegates: context.localizationDelegates,
      supportedLocales: context.supportedLocales,
      locale: context.locale,
      debugShowCheckedModeBanner: false,
      title: 'StockWatchAlert',
      theme: Themes.light(),
      darkTheme: Themes.dark(),
      themeMode: themeProvider.themeMode,
      home: SplashPage(),
    );
  }
}

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)..badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  }
}

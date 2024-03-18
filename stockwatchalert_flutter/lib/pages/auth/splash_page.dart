import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../models_providers/app_provider.dart';
import '../../models_providers/auth_provider.dart';
import 'package:flutter_native_splash/flutter_native_splash.dart';

class SplashPage extends StatefulWidget {
  @override
  _SplashPageState createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> with SingleTickerProviderStateMixin {
  @override
  void initState() {
    Future.delayed(Duration(milliseconds: 0)).then((value) async {
      await Provider.of<AuthProvider>(context, listen: false).init();
      Provider.of<AppProvider>(context, listen: false);
      await Future.delayed(Duration(milliseconds: 250));
      FlutterNativeSplash.remove();
    });
    super.initState();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold();
  }

  @override
  void dispose() {
    super.dispose();
  }
}

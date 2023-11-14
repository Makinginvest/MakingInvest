import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shimmer/shimmer.dart';

import '../../components/z_card.dart';
import '../../constants/app_colors.dart';
import '../../models_providers/app_provider.dart';
import 'signals_aggrs_page.dart';

class SignalsAggrsInitPage extends StatefulWidget {
  SignalsAggrsInitPage({Key? key, required this.type}) : super(key: key);
  final String type;

  @override
  State<SignalsAggrsInitPage> createState() => _SignalsAggrsInitPageState();
}

class _SignalsAggrsInitPageState extends State<SignalsAggrsInitPage> with TickerProviderStateMixin {
  String search = '';
  bool isLoadingInit = true;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    AppProvider appProvider = Provider.of<AppProvider>(context);
    final signalAggrsOpen = appProvider.signalAggrsOpen;

    if (signalAggrsOpen.length == 0) return SignalsInitLoadingPage();

    return SignalsAggrsPage(
      key: ObjectKey(signalAggrsOpen.length),
      signalsAggrOpen: signalAggrsOpen,
      controllerLength: signalAggrsOpen.length,
    );
  }
}

class SignalsInitLoadingPage extends StatelessWidget {
  const SignalsInitLoadingPage({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return Scaffold(
      appBar: AppBar(
        title: Shimmer.fromColors(
          baseColor: Colors.grey.shade700,
          highlightColor: Colors.grey.shade500,
          child: Row(
            children: [
              Container(
                width: 200.0,
                height: 20.0,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(4.0),
                  child: Container(color: Colors.white),
                ),
              ),
              SizedBox(width: 8),
              Spacer(),
              SizedBox(width: 32),
              Container(
                width: 60.0,
                height: 20.0,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(4.0),
                  child: Container(color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      ),
      body: ListView(
        children: [
          for (var i = 0; i < 10; i++)
            ZCard(
              padding: EdgeInsets.all(10),
              borderRadiusColor: isLightTheme ? AppCOLORS.cardBorderLight : AppCOLORS.cardBorderDark,
              margin: EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              child: Shimmer.fromColors(
                baseColor: Colors.grey.shade700,
                highlightColor: Colors.grey.shade500,
                child: Container(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Container(
                            width: 60.0,
                            height: 20.0,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(4.0),
                              child: Container(color: Colors.white),
                            ),
                          ),
                          SizedBox(width: 8),
                          Expanded(
                            child: Container(
                              width: 90.0,
                              height: 20.0,
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(4.0),
                                child: Container(color: Colors.white),
                              ),
                            ),
                          ),
                          SizedBox(width: 32),
                          Container(
                            width: 60.0,
                            height: 20.0,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(4.0),
                              child: Container(color: Colors.white),
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 8),
                      Row(
                        children: [
                          Container(
                            width: 80.0,
                            height: 20.0,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(4.0),
                              child: Container(color: Colors.white),
                            ),
                          ),
                          SizedBox(width: 8),
                          Spacer(),
                          SizedBox(width: 32),
                          Container(
                            width: 60.0,
                            height: 20.0,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(4.0),
                              child: Container(color: Colors.white),
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 8),
                      Row(
                        children: [
                          Container(
                            width: 100.0,
                            height: 20.0,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(4.0),
                              child: Container(color: Colors.white),
                            ),
                          ),
                          SizedBox(width: 8),
                          Spacer(),
                          SizedBox(width: 32),
                          Container(
                            width: 60.0,
                            height: 20.0,
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(4.0),
                              child: Container(color: Colors.white),
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 8),
                      Row(
                        children: [
                          Expanded(
                            child: Container(
                              width: 100.0,
                              height: 20.0,
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(4.0),
                                child: Container(color: Colors.white),
                              ),
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 8),
                      Row(
                        children: [
                          Expanded(
                            child: Container(
                              width: 100.0,
                              height: 20.0,
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(4.0),
                                child: Container(color: Colors.white),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

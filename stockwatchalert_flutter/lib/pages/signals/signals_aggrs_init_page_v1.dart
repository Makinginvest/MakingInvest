import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shimmer/shimmer.dart';
import 'package:stockwatchalert/constants/app_colors.dart';
import 'package:stockwatchalert/models_providers/app_controls_provider.dart';

import '../../components/z_card.dart';
import 'signals_aggrs_page_v1.dart';

class SignalsAggrsInitPageV1 extends StatefulWidget {
  SignalsAggrsInitPageV1({Key? key, required this.type}) : super(key: key);
  final String type;

  @override
  State<SignalsAggrsInitPageV1> createState() => _SignalsAggrsInitPageV1State();
}

class _SignalsAggrsInitPageV1State extends State<SignalsAggrsInitPageV1> with TickerProviderStateMixin {
  String search = '';
  bool isLoadingInit = true;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    AppControlsProvider appProvider = Provider.of<AppControlsProvider>(context);
    final signalAggrsOpenV1 = appProvider.signalAggrsOpenV1;

    if (signalAggrsOpenV1.length == 0) return SignalsInitLoadingPage();

    return SignalsAggrsPageV1(
      key: ObjectKey(signalAggrsOpenV1.length),
      signalsAggrOpenV1: signalAggrsOpenV1,
      controllerLength: signalAggrsOpenV1.length,
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
              borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
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

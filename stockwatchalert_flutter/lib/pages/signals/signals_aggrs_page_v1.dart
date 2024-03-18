import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_appbar_title.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/pages/signals/signals_aggr_page_v1.dart';

import '../../constants/app_colors.dart';
import '../../models_providers/auth_provider.dart';

class SignalsAggrsPageV1 extends StatefulWidget {
  SignalsAggrsPageV1({Key? key, required this.signalsAggrOpenV1, required this.controllerLength}) : super(key: key);

  final List<SignalAggrV1> signalsAggrOpenV1;
  final int controllerLength;

  @override
  State<SignalsAggrsPageV1> createState() => _SignalsAggrsPageV1State();
}

class _SignalsAggrsPageV1State extends State<SignalsAggrsPageV1> with TickerProviderStateMixin {
  String search = '';
  bool isLoadingInit = true;
  int signalsCount = 0;
  late TabController _controller;
  String? selectSignalAggrId;
  String? selectSignalAggrName;
  SignalAggrV1? selectedSignalAggrX;

  @override
  void initState() {
    _controller = TabController(length: (widget.controllerLength), vsync: this);
    if (widget.signalsAggrOpenV1.length > 0) {
      selectSignalAggrId = widget.signalsAggrOpenV1[0].id;
      selectSignalAggrName = widget.signalsAggrOpenV1[0].nameId;
      selectedSignalAggrX = widget.signalsAggrOpenV1[0];
    }
    _controller.addListener(() {
      int index = _controller.index;
      if (index == widget.controllerLength) return;

      selectSignalAggrId = widget.signalsAggrOpenV1[index].id;
      selectSignalAggrName = widget.signalsAggrOpenV1[index].nameId;
      selectedSignalAggrX = widget.signalsAggrOpenV1[index];

      setState(() {});
    });

    Future.microtask(() => Provider.of<AuthProvider>(context, listen: false).updateLastLoginAfter6H());

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return GestureDetector(
      onTap: () => FocusScope.of(context).requestFocus(FocusNode()),
      child: Scaffold(
          backgroundColor: Colors.transparent,
          body: NestedScrollView(
              floatHeaderSlivers: true,
              headerSliverBuilder: (context, innerBoxIsScrolled) => [
                    SliverOverlapAbsorber(
                      handle: NestedScrollView.sliverOverlapAbsorberHandleFor(context),
                      sliver: SliverAppBar(
                        pinned: true,
                        floating: true,
                        snap: true,
                        toolbarHeight: 52,
                        title: AppBarTitle(),
                        bottom: PreferredSize(
                          preferredSize: Size.fromHeight(44),
                          child: Container(
                            height: 44,
                            child: TabBar(
                              splashFactory: NoSplash.splashFactory,
                              overlayColor: MaterialStateProperty.all<Color>(Colors.transparent),
                              dividerColor: Colors.grey.withOpacity(.1115),
                              controller: _controller,
                              indicatorColor: AppColors.yellow,
                              labelColor: Colors.white,
                              labelStyle: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
                              indicatorSize: TabBarIndicatorSize.label,
                              padding: EdgeInsets.zero,
                              labelPadding: EdgeInsets.zero,
                              indicatorPadding: EdgeInsets.zero,
                              indicatorWeight: 3,
                              tabs: [
                                for (var s in widget.signalsAggrOpenV1)
                                  Tab(
                                      child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text('${s.nameType}', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                                      if (s.nameTypeSubtitle != '')
                                        Column(
                                          children: [
                                            SizedBox(height: 1.5),
                                            Text('${s.nameTypeSubtitle}', style: TextStyle(fontSize: 10, fontWeight: FontWeight.w500)),
                                          ],
                                        ),
                                    ],
                                  )),
                                // Tab(child: Icon(Icons.favorite_border, size: 20))
                              ],
                            ),
                          ),
                        ),
                      ),
                    )
                  ],
              body: Scaffold(
                backgroundColor: isLightTheme ? Colors.grey.shade300 : AppColors.bottomNavigationBarColorDark,
                appBar: AppBar(
                  toolbarHeight: 44,
                  backgroundColor: isLightTheme ? Colors.grey.shade300 : AppColors.bottomNavigationBarColorDark,
                ),
                body: ClipRRect(
                  // borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20)),
                  child: Container(
                    color: Theme.of(context).scaffoldBackgroundColor,
                    child: TabBarView(
                      // physics: const NeverScrollableScrollPhysics(),
                      controller: _controller,
                      children: [
                        for (var s in widget.signalsAggrOpenV1) SignalsAggrPageV1(signalAggr: s),
                      ],
                    ),
                  ),
                ),
              ))),
    );
  }

  List<SignalV1> getFilteredSignals(String s, List<SignalV1> signals) {
    if (s == '') return signals;
    return signals.where((signal) {
      return signal.symbol.toLowerCase().contains(s.toLowerCase());
    }).toList();
  }
}

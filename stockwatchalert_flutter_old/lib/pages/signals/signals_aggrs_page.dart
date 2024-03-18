import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';

import '../../components/z_card.dart';
import '../../constants/app_colors.dart';
import '../../models/auth_user.dart';
import '../../models/signal_aggr.dart';
import '../../models_providers/auth_provider.dart';
import '../../models_services/firebase_auth_service.dart';
import 'signals_aggr_page.dart';
import 'signals_closed_page.dart';

class SignalsAggrsPage extends StatefulWidget {
  SignalsAggrsPage({Key? key, required this.signalsAggrOpen, required this.controllerLength}) : super(key: key);

  final List<SignalAggr> signalsAggrOpen;
  final int controllerLength;

  @override
  State<SignalsAggrsPage> createState() => _SignalsAggrsPageState();
}

class _SignalsAggrsPageState extends State<SignalsAggrsPage> with TickerProviderStateMixin {
  String search = '';
  bool isLoadingInit = true;
  int signalsCount = 0;
  late TabController _controller;
  String? selectSignalAggrId;
  String? selectSignalAggrName;
  SignalAggr? selectedSignalAggrX;

  @override
  void initState() {
    _controller = TabController(length: (widget.controllerLength), vsync: this);
    if (widget.signalsAggrOpen.length > 0) {
      selectSignalAggrId = widget.signalsAggrOpen[0].id;
      selectSignalAggrName = widget.signalsAggrOpen[0].name;
      selectedSignalAggrX = widget.signalsAggrOpen[0];
    }
    _controller.addListener(() {
      int index = _controller.index;
      if (index == widget.controllerLength) return;

      selectSignalAggrId = widget.signalsAggrOpen[index].id;
      selectSignalAggrName = widget.signalsAggrOpen[index].name;
      selectedSignalAggrX = widget.signalsAggrOpen[index];

      setState(() {});
    });

    Future.microtask(() => Provider.of<AuthProvider>(context, listen: false).updateLastLoginAfter6H());

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final AuthUser authUser = authProvider.authUser!;
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
                        toolbarHeight: 46,
                        backgroundColor: isLightTheme ? Colors.grey.shade300 : AppColors.bottomNavigationBarColorDark,
                        title: Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text.rich(
                                    TextSpan(
                                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700, color: AppColors.white),
                                      children: [
                                        TextSpan(text: 'Stock', style: TextStyle(color: AppColors.green)),
                                        TextSpan(text: 'WatchAlert', style: TextStyle(color: AppColors.white)),
                                      ],
                                    ),
                                  ),
                                  Text('Your Ultimate Stock Source', style: TextStyle(fontSize: 10, color: AppColors.white)),
                                ],
                              ),
                            ),
                            Spacer(),
                            Center(
                              child: ZCard(
                                onTap: () {
                                  FirebaseAuthService.updateNofifications(user: authUser, id: selectSignalAggrName ?? '');
                                },
                                color: Colors.transparent,
                                shadowColor: Colors.transparent,
                                inkColor: Colors.transparent,
                                child:
                                    Icon(!authUser.notificationsDisabled.contains(selectSignalAggrName) ? Icons.notifications_active : Icons.notifications_off_outlined, size: 20),
                                margin: EdgeInsets.only(left: 10),
                                padding: EdgeInsets.all(10),
                                borderRadiusColor: Colors.transparent,
                              ),
                            ),
                            SizedBox(width: 8),
                            ZCard(
                              onTap: () {
                                if (selectedSignalAggrX == null) return;
                                Get.to(() => SignalsClosedPage(signalAggr: selectedSignalAggrX!), fullscreenDialog: true, duration: Duration(milliseconds: 500));
                              },
                              color: Colors.transparent,
                              shadowColor: Colors.transparent,
                              inkColor: Colors.transparent,
                              borderRadiusColor: AppColors.green,
                              child: Text('Results', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w900, color: AppColors.green)),
                              margin: EdgeInsets.symmetric(),
                              padding: EdgeInsets.fromLTRB(8, 4, 8, 4),
                            ),
                            SizedBox(width: 8),
                          ],
                        ),
                        bottom: PreferredSize(
                          preferredSize: Size.fromHeight(44),
                          child: Container(
                            height: 44,
                            child: TabBar(
                              dividerColor: Colors.transparent,
                              controller: _controller,
                              indicatorColor: AppColors.green,
                              labelColor: Colors.white,
                              labelStyle: TextStyle(fontSize: 14.5, fontWeight: FontWeight.w500),
                              indicatorSize: TabBarIndicatorSize.label,
                              padding: EdgeInsets.zero,
                              labelPadding: EdgeInsets.zero,
                              indicatorPadding: EdgeInsets.zero,
                              indicatorWeight: 3,
                              tabs: [
                                for (var s in widget.signalsAggrOpen)
                                  Tab(
                                      child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      // SizedBox(height: 5),
                                      Text('${s.nameType}'),
                                      if (s.nameTypeSubtitle != '') Text('${s.nameTypeSubtitle}', style: TextStyle(fontSize: 10, fontWeight: FontWeight.w500)),
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
                  toolbarHeight: 45,
                  backgroundColor: isLightTheme ? Colors.grey.shade300 : AppColors.bottomNavigationBarColorDark,
                ),
                body: ClipRRect(
                  borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20)),
                  child: Container(
                    color: Theme.of(context).scaffoldBackgroundColor,
                    child: TabBarView(
                      controller: _controller,
                      children: [
                        for (var s in widget.signalsAggrOpen) SignalsAggrPage(signalAggr: s),
                        // ListView(children: []),
                      ],
                    ),
                  ),
                ),
              ))),
    );
  }

  List<Signal> getFilteredSignals(String s, List<Signal> signals) {
    if (s == '') return signals;
    return signals.where((signal) {
      return signal.symbol.toLowerCase().contains(s.toLowerCase());
    }).toList();
  }
}

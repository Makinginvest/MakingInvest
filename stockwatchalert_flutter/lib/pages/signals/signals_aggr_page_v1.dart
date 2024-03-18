import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_signal_card_results_v1.dart';
import 'package:stockwatchalert/components/z_signal_card_subscribe_v1.dart';
import 'package:stockwatchalert/components/z_signal_card_v1.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/models_services/firebase_auth_service.dart';
import 'package:stockwatchalert/pages/signals/signals_closed_page_v1.dart';

import '../../components/z_card.dart';
import '../../constants/app_colors.dart';
import '../../models/auth_user.dart';
import '../../models_providers/app_provider.dart';
import '../../models_providers/auth_provider.dart';

class SignalsAggrPageV1 extends StatefulWidget {
  const SignalsAggrPageV1({Key? key, required this.signalAggr}) : super(key: key);
  final SignalAggrV1 signalAggr;

  @override
  State<SignalsAggrPageV1> createState() => _SignalsAggrPageV1State();
}

class _SignalsAggrPageV1State extends State<SignalsAggrPageV1> {
  String filterMode = 'All';
  SignalAggrV1 signalAggr = SignalAggrV1();
  List<SignalV1> signals = [];
  List<SignalV1> filteredSignals = [];

  @override
  void initState() {
    signalAggr = widget.signalAggr;
    signals = widget.signalAggr.signals;
    getFilteredSignalsByMode(filterMode);
    super.initState();
  }

  @override
  void didUpdateWidget(covariant SignalsAggrPageV1 oldWidget) {
    signalAggr = widget.signalAggr;
    signals = widget.signalAggr.signals;
    getFilteredSignalsByMode(filterMode);
    super.didUpdateWidget(oldWidget);
  }

  @override
  Widget build(BuildContext context) {
    final AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final authUser = authProvider.authUser;

    return Container(
      // color: Colors.red,
      child: CustomScrollView(
        slivers: [
          SliverList(
            delegate: SliverChildListDelegate(
              [
                SizedBox(height: 14),
                Container(
                  margin: EdgeInsets.only(left: 16),
                  height: 32,
                  child: ListView(shrinkWrap: true, scrollDirection: Axis.horizontal, children: [
                    _buildFilterHeading(text: 'All', total: signalAggr.signals.length),
                    _buildFilterHeading(text: 'Pending', total: signalAggr.numPending()),
                    if (authUser?.hasActiveSubscription == true) _buildFilterHeading(text: 'Long', total: signalAggr.numLongs()),
                    if (authUser?.hasActiveSubscription == true) _buildFilterHeading(text: 'Short', total: signalAggr.numShorts()),
                    _buildFilterHeading2(text: 'Results', total: signalAggr.numShorts()),
                    _buildFilterHeading3(text: 'Results', total: signalAggr.numShorts()),
                  ]),
                ),
                SizedBox(height: 4),
                ZSignalCardResultsV1(signalAggr: signalAggr),
              ],
            ),
          ),

          if (signalAggr.signals.isEmpty)
            SliverList(
              delegate: SliverChildListDelegate(
                [
                  SizedBox(height: MediaQuery.of(context).size.height * .125),
                  SvgPicture.asset('assets/svg/no_signal.svg', height: 160, width: 160),
                  Center(child: Text("We're sorry the ai ran out of signals")),
                  SizedBox(height: 3),
                  Center(child: Text("We're are cooking more high quality signals")),
                  SizedBox(height: 3),
                  Center(child: Text("Check out our results")),
                ],
              ),
            ),
          //
          SliverList(
              delegate: SliverChildBuilderDelegate((context, index) {
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                getSignalCard(filteredSignals[index]),
              ],
            );
          }, childCount: filteredSignals.length)),
        ],
      ),
    );
  }

  ZCard _buildFilterHeading({required String text, required int total}) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
      borderWidth: 1.25,
      padding: EdgeInsets.symmetric(horizontal: 8),
      margin: EdgeInsets.only(right: 7),
      child: Center(child: Text('${text} (${total})', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700))),
      color: filterMode == text
          ? isLightTheme
              ? Colors.grey.shade300
              : Color(0xFF35383F)
          : null,
      onTap: () => getFilteredSignalsByMode(text),
    );
  }

  ZCard _buildFilterHeading2({required String text, required int total}) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
      borderWidth: 1.25,
      padding: EdgeInsets.symmetric(horizontal: 8),
      margin: EdgeInsets.only(right: 7),
      child: Center(child: Text('${text}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700))),
      color: filterMode == text
          ? isLightTheme
              ? Colors.grey.shade300
              : Color(0xFF35383F)
          : null,
      onTap: () => Get.to(() => SignalsClosedPageV1(signalAggr: signalAggr), fullscreenDialog: true, duration: Duration(milliseconds: 500)),
    );
  }

  ZCard _buildFilterHeading3({required String text, required int total}) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    final AuthUser authUser = authProvider.authUser!;
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      borderRadiusColor: isLightTheme ? AppColors.cardBorderLight : AppColors.cardBorderDark,
      borderWidth: 1.25,
      padding: EdgeInsets.symmetric(horizontal: 8),
      margin: EdgeInsets.only(right: 7),
      child: Center(
        child: Icon(
          !authUser.notificationsDisabled.contains(signalAggr.nameId) ? Icons.notifications_active : Icons.notifications_off_outlined,
          size: 20,
        ),
      ),
      color: filterMode == text
          ? isLightTheme
              ? Colors.grey.shade300
              : Color(0xFF35383F)
          : null,
      onTap: () => FirebaseAuthService.updateNofifications(user: authUser, id: signalAggr.nameId),
    );
  }

  getFilteredSignalsByMode(String mode) {
    final AppProvider appProvider = Provider.of<AppProvider>(context, listen: false);
    List<String> favorites = appProvider.authUser?.favoriteSignals ?? [];
    if (mode == 'Favorites') filteredSignals = signals.where((signal) => favorites.contains(signal.id)).toList();
    if (mode == 'All') filteredSignals = signals;
    if (mode == 'Long') filteredSignals = signals.where((signal) => signal.entryType == 'long').toList();
    if (mode == 'Short') filteredSignals = signals.where((signal) => signal.entryType == 'short').toList();
    if (mode == 'Pending') filteredSignals = signals.where((signal) => signal.statusTrade == 'open').toList();

    filterMode = mode;

    if (mounted) setState(() {});
  }

  getSignalCard(SignalV1 signal) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    AuthUser? user = authProvider.authUser;

    if (user?.hasActiveSubscription == true) return ZSignalCardV1(signal: signal, signalAggrV1: signalAggr);
    if (signal.tp1DateTimeUtc != null) return ZSignalCardV1(signal: signal, signalAggrV1: signalAggr);
    return ZSignalCardSubscribeV1(signal: signal);
  }
}

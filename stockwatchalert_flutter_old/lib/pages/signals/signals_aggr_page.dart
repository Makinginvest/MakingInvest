import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:provider/provider.dart';

import '../../components/z_card.dart';
import '../../components/z_signal_card.dart';
import '../../components/z_signal_card_results.dart';
import '../../components/z_signal_subscribe_card.dart';
import '../../constants/app_colors.dart';
import '../../models/auth_user.dart';
import '../../models/signal_aggr.dart';
import '../../models_providers/app_provider.dart';
import '../../models_providers/auth_provider.dart';

class SignalsAggrPage extends StatefulWidget {
  const SignalsAggrPage({Key? key, required this.signalAggr}) : super(key: key);
  final SignalAggr signalAggr;

  @override
  State<SignalsAggrPage> createState() => _SignalsAggrPageState();
}

class _SignalsAggrPageState extends State<SignalsAggrPage> {
  String filterMode = 'All';
  SignalAggr signalAggr = SignalAggr();
  List<Signal> signals = [];
  List<Signal> filteredSignals = [];

  @override
  void initState() {
    signalAggr = widget.signalAggr;
    signals = widget.signalAggr.signals;
    getFilteredSignalsByMode(filterMode);
    super.initState();
  }

  @override
  void didUpdateWidget(covariant SignalsAggrPage oldWidget) {
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
      child: CustomScrollView(
        slivers: [
          if (authUser?.hasActiveSubscription == true)
            SliverList(
              delegate: SliverChildListDelegate(
                [
                  SizedBox(height: 16),
                  Container(
                    margin: EdgeInsets.only(left: 16),
                    height: 35,
                    child: ListView(shrinkWrap: true, scrollDirection: Axis.horizontal, children: [
                      _buildFilterHeading(text: 'All', total: signalAggr.signals.length),
                      _buildFilterHeading(text: 'Pending', total: signalAggr.numPending()),
                      _buildFilterHeading(text: 'Long', total: signalAggr.numLongs()),
                      _buildFilterHeading(text: 'Short', total: signalAggr.numShorts()),
                      if (signalAggr.nameSignalsCollection.contains('Crypto')) _buildFilterHeading(text: 'Futures', total: signalAggr.numFutures()),
                    ]),
                  ),
                  SizedBox(height: 4),
                  ZSignalCardResults(signalAggr: signalAggr),
                ],
              ),
            ),
          if (authUser?.hasActiveSubscription == false)
            SliverList(
              delegate: SliverChildListDelegate(
                [
                  SizedBox(height: 8),
                  ZSignalCardResults(signalAggr: signalAggr),
                ],
              ),
            ),
          //
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
      borderWidth: 1.5,
      padding: EdgeInsets.symmetric(horizontal: 8),
      margin: EdgeInsets.only(right: 7),
      child: Center(child: Text('${text} (${total})', style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700))),
      color: filterMode == text
          ? isLightTheme
              ? Colors.grey.shade300
              : Color(0xFF35383F)
          : null,
      onTap: () => getFilteredSignalsByMode(text),
    );
  }

  getFilteredSignalsByMode(String mode) {
    final AppProvider appProvider = Provider.of<AppProvider>(context, listen: false);
    List<String> favorites = appProvider.authUser?.favoriteSignals ?? [];
    if (mode == 'Favorites') filteredSignals = signals.where((signal) => favorites.contains(signal.id)).toList();
    if (mode == 'All') filteredSignals = signals;
    if (mode == 'Long') filteredSignals = signals.where((signal) => signal.entryType == 'long').toList();
    if (mode == 'Short') filteredSignals = signals.where((signal) => signal.entryType == 'short').toList();
    if (mode == 'Futures') filteredSignals = signals.where((signal) => signal.hasFutures == true).toList();
    if (mode == 'Pending') filteredSignals = signals.where((signal) => signal.entryResult == 'in progress').toList();

    filterMode = mode;

    if (mounted) setState(() {});
  }

  getSignalCard(Signal signal) {
    AuthProvider authProvider = Provider.of<AuthProvider>(context);
    AuthUser? user = authProvider.authUser;

    if (user?.hasActiveSubscription == true) return ZSignalCard(signal: signal, signalAggrX: signalAggr);
    if (signal.isFree) return ZSignalCard(signal: signal, signalAggrX: signalAggr);
    if (signal.takeProfit2Hit) return ZSignalCard(signal: signal, signalAggrX: signalAggr);

    return ZSignalSubscribeCard(signal: signal);
  }
}

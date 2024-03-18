import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/constants/app_colors.dart';
import 'package:stockwatchalert/models/symbols_tracker_aggr.dart';
import 'package:stockwatchalert/models_providers/app_provider.dart';

import '../../components/z_text_form_field_search.dart';
import '../../models_providers/app_controls_provider.dart';

class TrackerPage extends StatefulWidget {
  const TrackerPage({Key? key}) : super(key: key);

  @override
  State<TrackerPage> createState() => _TrackerPageState();
}

class _TrackerPageState extends State<TrackerPage> {
  String search = '';
  String filterMode = 'All';
  @override
  void initState() {
    Provider.of<AppProvider>(context, listen: false).getSymbolTrackerAggr();
    super.initState();
  }

  List<SymbolTracker> getFilteredSymbolTrackers(String search, List<SymbolTracker> symbolTrackers) {
    if (filterMode == 'All') symbolTrackers = symbolTrackers;
    if (filterMode == 'Crypto') symbolTrackers = symbolTrackers.where((element) => element.market.toLowerCase() == 'crypto').toList();
    if (filterMode == 'Forex') symbolTrackers = symbolTrackers.where((element) => element.market.toLowerCase() == 'forex').toList();
    if (filterMode == 'Stocks') symbolTrackers = symbolTrackers.where((element) => element.market.toLowerCase() == 'stocks').toList();

    if (search.isEmpty) return symbolTrackers;
    return symbolTrackers.where((element) => element.symbol.toLowerCase().contains(search.toLowerCase())).toList();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (() => FocusScope.of(context).unfocus()),
      child: Scaffold(appBar: AppBar(toolbarHeight: 0), body: _buildBody()),
    );
  }

  _buildBody() {
    final AppProvider appProvider = Provider.of<AppProvider>(context);
    final symbolTrackerAggr = appProvider.symbolTrackerAggr;
    final symbolTrackers = appProvider.symbolTrackers;
    final symbolTrackersFiltered = getFilteredSymbolTrackers(search, symbolTrackers);

    if (symbolTrackers.isEmpty) return Center(child: CircularProgressIndicator());

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(height: 8),
        Container(
          margin: EdgeInsets.symmetric(horizontal: 16),
          child: ZSearch(
            height: 38,
            margin: EdgeInsets.zero,
            onValueChanged: ((value) {
              search = value;
              setState(() {});
            }),
          ),
        ),
        SizedBox(height: 12),
        Container(
          margin: EdgeInsets.only(left: 16),
          height: 32,
          child: ListView(shrinkWrap: true, scrollDirection: Axis.horizontal, children: [
            _buildFilterHeading(text: 'All', total: symbolTrackers.length),
            _buildFilterHeading(text: 'Crypto', total: symbolTrackerAggr.crypto.length),
            _buildFilterHeading(text: 'Forex', total: symbolTrackerAggr.forex.length),
            _buildFilterHeading(text: 'Stocks', total: symbolTrackerAggr.stocks.length),
          ]),
        ),
        Expanded(
          child: ListView.builder(
            shrinkWrap: true,
            physics: ClampingScrollPhysics(),
            itemCount: symbolTrackersFiltered.length,
            itemBuilder: ((context, index) => Column(
                  children: [
                    if (index == 0) SizedBox(height: 4),
                    ZSymbolTrackerCard(symbolTracker: (symbolTrackersFiltered[index])),
                    if (index == symbolTrackersFiltered.length - 1) SizedBox(height: 8),
                  ],
                )),
          ),
        ),
      ],
    );
  }

  ZCard _buildFilterHeading({required String text, required int total}) {
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    return ZCard(
      padding: EdgeInsets.symmetric(horizontal: 8),
      margin: EdgeInsets.only(right: 7),
      child: Center(child: Text('${text} (${total})', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700))),
      borderRadiusColor: isLightTheme ? Colors.grey.shade300 : Color(0xFF35383F).withOpacity(.8),
      color: filterMode == text
          ? isLightTheme
              ? Colors.grey.shade300
              : Color(0xFF35383F)
          : null,
      onTap: () => setState(() => filterMode = text),
    );
  }
}

class ZSymbolTrackerCard extends StatelessWidget {
  final SymbolTracker symbolTracker;

  const ZSymbolTrackerCard({
    Key? key,
    required this.symbolTracker,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final AppControlsProvider appWsProvider = Provider.of<AppControlsProvider>(context);
    String market = symbolTracker.market.toUpperCase();
    return ZCard(
        borderRadius: BorderRadius.circular(16),
        borderRadiusColor: AppColors.dark4,
        borderWidth: 1.5,
        padding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
        child: Column(
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '(${market}) ${symbolTracker.symbol}',
                  style: TextStyle(color: AppColors.yellow, fontSize: 14, fontWeight: FontWeight.w900),
                ),
                SizedBox(height: 2),
                Spacer(),
                Text('${appWsProvider.getWSSymbolPriceSymbolTracker(symbolTracker)}', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w900, color: AppColors.green)),
                // Text(symbolTracker.market)
              ],
            ),
            SizedBox(height: 8),
            GridView(
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4,
                childAspectRatio: 1.35,
              ),
              shrinkWrap: true,
              physics: ClampingScrollPhysics(),
              children: [
                buildExpandedCard(
                    symbolTracker: symbolTracker, title: '1h ago', val: symbolTracker.val1hrAgo, currentPrice: appWsProvider.getWSSymbolPriceSymbolTracker(symbolTracker)),
                buildExpandedCard(
                    symbolTracker: symbolTracker, title: '4h ago', val: symbolTracker.val4hrAgo, currentPrice: appWsProvider.getWSSymbolPriceSymbolTracker(symbolTracker)),
                buildExpandedCard(
                    symbolTracker: symbolTracker, title: '24h ago', val: symbolTracker.val24hrAgo, currentPrice: appWsProvider.getWSSymbolPriceSymbolTracker(symbolTracker)),
                buildExpandedCard(
                    symbolTracker: symbolTracker, title: '7d ago', val: symbolTracker.val7dAgo, currentPrice: appWsProvider.getWSSymbolPriceSymbolTracker(symbolTracker)),
              ],
            ),
          ],
        ));
  }

  buildExpandedCard({required SymbolTracker symbolTracker, required String title, num? val = 0, num? currentPrice = 0}) {
    bool isForex = symbolTracker.market.toLowerCase() == 'forex';
    bool isPositive = (getPercentPipsChange(val: val, currentPrice: currentPrice) ?? 0) > 0;
    String percentPipsChangeString = getPercentPipsChangeString(val: val, currentPrice: currentPrice, isForex: isForex);
    return Container(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title),
          Text('${val}'),
          Text(
            percentPipsChangeString,
            style: TextStyle(fontSize: 13, fontWeight: FontWeight.w900, color: isPositive ? AppColors.green : AppColors.red),
          ),
        ],
      ),
    );
  }

  num? getPercentPipsChange({num? val, num? currentPrice, bool isForex = false}) {
    if (val == null || currentPrice == null || val == 0 || currentPrice == 0) return null;

    if (isForex) {
      val = (currentPrice - val) * 10000;
      if (symbolTracker.symbol.contains('JPY')) val = val / 100;
      return (val / 1).round() * 1;
    }

    return ((currentPrice - val) / val) * 100;
  }

  String getPercentPipsChangeString({num? val, num? currentPrice, bool isForex = false}) {
    if (val == null || currentPrice == null || val == 0 || currentPrice == 0) return '---';

    if (isForex) {
      val = (currentPrice - val) * 10000;
      if (symbolTracker.symbol.contains('JPY')) val = val / 100;
      val = (val / 1).round() * 1;
      return '${val} pips';
    }

    //  round to 2 decimal places
    num valPercent = ((currentPrice - val) / val) * 100;
    valPercent = (valPercent * 100).round() / 100;

    return '${valPercent} %';
  }
}

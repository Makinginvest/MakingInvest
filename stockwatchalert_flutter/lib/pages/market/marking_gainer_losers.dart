import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:provider/provider.dart';
import 'package:signalbyt/components/z_app_bar_title.dart';
import 'package:signalbyt/constants/app_colors.dart';
import 'package:signalbyt/models_providers/app_controls_provider.dart';
import 'package:signalbyt/pages/market/marking_gainer_losers_details_page.dart';

class MarketGainerLosers extends StatefulWidget {
  const MarketGainerLosers({super.key});

  @override
  State<MarketGainerLosers> createState() => _MarketGainerLosersState();
}

class _MarketGainerLosersState extends State<MarketGainerLosers> with TickerProviderStateMixin {
  late TabController _controller;
  @override
  void initState() {
    _controller = TabController(length: 3, vsync: this);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context);
    final gainers = appControlsProvider.gainers;
    final losers = appControlsProvider.losers;
    final mostActive = appControlsProvider.actives;
    return Scaffold(
        body: Scaffold(
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
                          title: AppBarTitle(),
                          bottom: PreferredSize(
                            preferredSize: Size.fromHeight(44),
                            child: Container(
                              height: 44,
                              child: TabBar(
                                dividerColor: Colors.grey.withOpacity(0.125),
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
                                  Tab(text: 'Gainers'),
                                  Tab(text: 'Losers'),
                                  Tab(text: 'Most Active'),
                                ],
                              ),
                            ),
                          ),
                        ),
                      )
                    ],
                body: Scaffold(
                  appBar: AppBar(toolbarHeight: 45),
                  body: TabBarView(
                    controller: _controller,
                    children: [
                      MarketGainerLosersDetailsPage(
                        activities: gainers,
                      ),
                      MarketGainerLosersDetailsPage(
                        activities: losers,
                      ),
                      MarketGainerLosersDetailsPage(
                        activities: mostActive,
                      ),
                    ],
                  ),
                ))));
  }
}

import 'package:custom_navigation_bar/custom_navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';
import 'package:signalbyt/pages/announcement/annoucement_page.dart';
import 'package:signalbyt/pages/market/marking_gainer_losers.dart';
import 'package:signalbyt/pages/news/news_page.dart';

import '../../../models_providers/navbar_provider.dart';
import '../constants/app_colors.dart';
import 'account/account_page.dart';
import 'signals/signals_aggrs_init_page.dart';

class AppNavbarPage extends StatefulWidget {
  const AppNavbarPage({Key? key}) : super(key: key);

  @override
  _AppNavbarPageState createState() => _AppNavbarPageState();
}

class _AppNavbarPageState extends State<AppNavbarPage> {
  late PageController _pageController;

  @override
  void initState() {
    final appProvider = Provider.of<NavbarProvider>(context, listen: false);
    _pageController = PageController(initialPage: appProvider.selectedPageIndex);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final appProvider = Provider.of<NavbarProvider>(context, listen: false);
    return Scaffold(
      body: AnimatedSwitcher(
          transitionBuilder: (Widget child, Animation<double> animation) {
            return FadeTransition(child: child, opacity: animation);
          },
          duration: const Duration(milliseconds: 300),
          child: pages.elementAt(appProvider.selectedPageIndex)),
      bottomNavigationBar: CustomNavigationBar(
        onTap: (v) {
          appProvider.selectedPageIndex = v;
          if (_pageController.hasClients) _pageController.animateToPage(v, duration: Duration(milliseconds: 300), curve: Curves.easeInOut);
        },
        iconSize: 24.0,
        selectedColor: Colors.white,
        strokeColor: Colors.white,
        backgroundColor: context.isDarkMode ? AppColors.dark3 : Colors.grey.shade300,
        borderRadius: Radius.circular(20.0),
        opacity: 1,
        elevation: 0,
        currentIndex: appProvider.selectedPageIndex,
        isFloating: true,
        items: [
          CustomNavigationBarItem(
            icon: SvgPicture.asset('assets/svg/home.svg', colorFilter: ColorFilter.mode(getIconColor(0), BlendMode.srcIn), height: getIconHeight(0), width: getIconHeight(0)),
            title: Text('Home', style: TextStyle(color: getIconColor(0), fontSize: 12, fontWeight: FontWeight.bold)),
          ),
          CustomNavigationBarItem(
            icon: SvgPicture.asset('assets/svg/trending.svg', colorFilter: ColorFilter.mode(getIconColor(1), BlendMode.srcIn), height: getIconHeight(1), width: getIconHeight(1)),
            title: Text('Trending', style: TextStyle(color: getIconColor(1), fontSize: 12, fontWeight: FontWeight.bold)),
          ),
          CustomNavigationBarItem(
            icon: SvgPicture.asset('assets/svg/signals.svg', colorFilter: ColorFilter.mode(getIconColor(2), BlendMode.srcIn), height: getIconHeight(2), width: getIconHeight(1)),
            title: Text('Signals', style: TextStyle(color: getIconColor(2), fontSize: 12, fontWeight: FontWeight.bold)),
          ),
          CustomNavigationBarItem(
            icon: SvgPicture.asset('assets/svg/news.svg', colorFilter: ColorFilter.mode(getIconColor(3), BlendMode.srcIn), height: getIconHeight(3), width: getIconHeight(2)),
            title: Text('News', style: TextStyle(color: getIconColor(3), fontSize: 12, fontWeight: FontWeight.bold)),
          ),
          CustomNavigationBarItem(
            icon: SvgPicture.asset('assets/svg/user.svg', colorFilter: ColorFilter.mode(getIconColor(4), BlendMode.srcIn), height: getIconHeight(4), width: getIconHeight(3)),
            title: Text('Profile', style: TextStyle(color: getIconColor(4), fontSize: 12, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  double getIconHeight(int index) {
    final appProvider = Provider.of<NavbarProvider>(context);
    final selectedIndex = appProvider.selectedPageIndex;
    return selectedIndex == index ? 24 : 24;
  }

  Color getIconColor(int index) {
    final appProvider = Provider.of<NavbarProvider>(context);
    final selectedIndex = appProvider.selectedPageIndex;
    final isLightTheme = Theme.of(context).brightness == Brightness.light;
    Color color = isLightTheme ? Colors.black26 : Colors.white24;
    if (selectedIndex == index) return isLightTheme ? AppColors.green : AppColors.green;
    return color;
  }

/* ----------------------------- NOTE UserPages ----------------------------- */

  List<Widget> pages = [
    AnnoucementsPage(),
    MarketGainerLosers(),
    SignalsAggrsInitPage(type: 'normal', key: ObjectKey('normal')),
    NewsPage(),
    MyAccountPage(),
  ];
}

import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:stockwatchalert/pages/subsciption/subscription_page.dart';

import '../../components/z_button.dart';
import '../../constants/app_colors.dart';
import '../../models_services/firebase_auth_service.dart';

class OnboardingPage1 extends StatefulWidget {
  const OnboardingPage1({super.key});

  @override
  State<OnboardingPage1> createState() => _OnboardingPage1State();
}

class _OnboardingPage1State extends State<OnboardingPage1> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // backgroundColor: Colors.black,
      extendBody: true,
      extendBodyBehindAppBar: true,
      appBar: AppBar(backgroundColor: Colors.transparent),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset('assets/images/logo.png', width: 80),
          SizedBox(height: 16),
          Text(
            'Welcome to StockWatchAlert! \nYour gateway to smart investing starts here.',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
            textAlign: TextAlign.center,
          ),
          Container(
            transform: Matrix4.rotationZ(-0.05),
            padding: EdgeInsets.fromLTRB(40, 8, 40, 16),
            margin: EdgeInsets.fromLTRB(0, 20, 0, 10),
            decoration: BoxDecoration(color: AppColors.green, borderRadius: BorderRadius.circular(0)),
            child: Container(
              transform: Matrix4.rotationZ(0.05),
              child: Text(
                'AI Signals, Learning, \nAnalysis',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                textAlign: TextAlign.center,
              ),
            ),
          ),
          Text(
            'Dive in and set the stage for your financial growth.',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 16),
          SvgPicture.asset('assets/svg/onboarding1.svg', height: 180, width: 200),
          SizedBox(height: 16),
          GestureDetector(
            onTap: () => Get.to(() => OnboardingPage2()),
            child: Stack(
              alignment: AlignmentDirectional.centerEnd,
              children: [
                ZButton(
                  borderRadius: BorderRadius.circular(20),
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  text: 'Start',
                  backgroundColor: AppColors.green,
                  onTap: () => Get.to(() => OnboardingPage2()),
                ),
                Container(child: Icon(Icons.arrow_forward_outlined), margin: EdgeInsets.only(right: 32)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class OnboardingPage2 extends StatefulWidget {
  const OnboardingPage2({super.key});

  @override
  State<OnboardingPage2> createState() => _OnboardingPage2State();
}

class _OnboardingPage2State extends State<OnboardingPage2> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // backgroundColor: Colors.black,
      extendBody: true,
      extendBodyBehindAppBar: true,
      appBar: AppBar(backgroundColor: Colors.transparent),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset(
            'assets/images/bull_bear.png',
            height: 160,
          ),
          Container(
            width: MediaQuery.of(context).size.width * 0.9,
            margin: EdgeInsets.symmetric(horizontal: 16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildSectionVertical(
                  title: '"Real-Time Alerts',
                  subtitle: 'Unlock the power of real-time signals and live news to make informed decisions on the go.',
                ),
                _buildSectionVertical(
                  title: 'Market Insights',
                  subtitle: 'Gain access to deep market insights and analysis, tailored to your trading strategy.',
                ),
              ],
            ),
          ),
          Container(
            width: MediaQuery.of(context).size.width * 0.9,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildSectionVertical(
                  title: 'Strategic Tools',
                  subtitle: 'Navigate the markets with confidence, using our cutting-edge tools for a competitive edge.',
                ),
                _buildSectionVertical(
                  title: 'Strategic Tools',
                  subtitle: 'Empower your trading with actionable intelligence and the latest market trends.',
                ),
              ],
            ),
          ),
          Container(
            width: MediaQuery.of(context).size.width * 0.9,
            child: _buildSectionHosizontal(
              title: '10+ AI Trading Signals Every Day',
              subtitle: 'Never miss a trading opportunity with our AI-powered signals.',
              imagePath: 'assets/svg/rocket.svg',
            ),
          ),
          Text(
            'Cancel Anytime',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
            textAlign: TextAlign.center,
          ),
          Text(
            'Cancel your subscriptions any time, \nno penalties or fees.',
            style: TextStyle(
              fontSize: 12,
            ),
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 16),
          GestureDetector(
            onTap: () => Get.to(() => SubscriptionPage(isOnboarding: true)),
            child: Stack(
              alignment: AlignmentDirectional.centerEnd,
              children: [
                ZButton(
                  borderRadius: BorderRadius.circular(20),
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  text: 'Continue',
                  backgroundColor: AppColors.green,
                  onTap: () {
                    FirebaseAuthService.setOnboarded();
                    Get.to(() => SubscriptionPage(isOnboarding: true));
                  },
                ),
                Container(child: Icon(Icons.arrow_forward_outlined), margin: EdgeInsets.only(right: 32)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  _buildSectionVertical({required String title, required String subtitle}) {
    return Expanded(
      child: Container(
        padding: EdgeInsets.fromLTRB(8, 16, 8, 16),
        margin: EdgeInsets.fromLTRB(0, 8, 0, 8),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(0),
          image: DecorationImage(image: AssetImage('assets/images/green-border-square.png'), fit: BoxFit.fill),
        ),
        child: Column(
          children: [
            // SvgPicture.asset(imagePath, height: 35, width: 35),
            SizedBox(height: 4),
            Text(
              title,
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, height: 1.2),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 4),
            Text(
              subtitle,
              style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  _buildSectionHosizontal({required String title, required String subtitle, required String imagePath}) {
    return Container(
      width: MediaQuery.of(context).size.width * 0.9,
      padding: EdgeInsets.fromLTRB(8, 16, 8, 16),
      margin: EdgeInsets.fromLTRB(0, 8, 0, 8),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(0),
        image: DecorationImage(image: AssetImage('assets/images/green-border-rectangle.png'), fit: BoxFit.fill),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SvgPicture.asset(imagePath, height: 40, width: 40),
          SizedBox(height: 4),
          Column(
            children: [
              Text(
                title,
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, height: 1.2),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 4),
              Text(
                subtitle,
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

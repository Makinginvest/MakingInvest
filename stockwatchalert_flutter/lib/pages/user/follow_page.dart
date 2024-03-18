import 'package:flutter/material.dart';
import 'package:stockwatchalert/constants/app_links.dart';
import 'package:smooth_star_rating_null_safety/smooth_star_rating_null_safety.dart';
import 'package:stockwatchalert/components/z_button.dart';
import 'package:stockwatchalert/components/z_card.dart';

import '../../utils/z_launch_url.dart';

class FollowPage extends StatefulWidget {
  FollowPage({Key? key}) : super(key: key);

  @override
  State<FollowPage> createState() => _FollowPageState();
}

class _FollowPageState extends State<FollowPage> {
  double rating = 5;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      appBar: AppBar(),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset('assets/images/star.png', height: 70),
          SizedBox(height: 30),
          Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text('Rate your experience', style: TextStyle(fontSize: 20)),
              SizedBox(height: 20),
              SmoothStarRating(
                rating: rating.toDouble(),
                size: 30,
                filledIconData: Icons.star,
                halfFilledIconData: Icons.star_half,
                defaultIconData: Icons.star_border,
                starCount: 5,
                allowHalfRating: true,
                color: Color(0xFFFDC413),
                borderColor: Color(0xFFFDC413),
                spacing: 2.0,
                onRatingChanged: (value) {
                  rating = value;
                  setState(() {});
                },
              ),
              SizedBox(height: 25),
              ZButton(
                margin: EdgeInsets.symmetric(horizontal: 48),
                text: 'Submit',
                onTap: () {},
              ),
              SizedBox(height: 20),
              Text('Follow our social media'),
              SizedBox(height: 20),
            ],
          ),
          Image.asset('assets/images/divider.png', height: 20),
          SizedBox(height: 20),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 24),
            child: Row(
              children: [
                Expanded(
                  child: ZCard(
                    onTap: () {
                      ZLaunchUrl.launchUrl(AppLINKS.facebookUrl);
                    },
                    color: Colors.transparent,
                    margin: EdgeInsets.zero,
                    padding: EdgeInsets.zero,
                    child: Column(
                      children: [
                        Image.asset('assets/images/icon_facebook.png', height: 35),
                        SizedBox(height: 8),
                        Text('Facebook'),
                      ],
                    ),
                  ),
                ),
                Expanded(
                  child: ZCard(
                    onTap: () {
                      ZLaunchUrl.launchUrl(AppLINKS.twitterUrl);
                    },
                    color: Colors.transparent,
                    margin: EdgeInsets.zero,
                    padding: EdgeInsets.zero,
                    child: Column(
                      children: [
                        Image.asset('assets/images/icon_twitter.png', height: 35),
                        SizedBox(height: 8),
                        Text('Twitter'),
                      ],
                    ),
                  ),
                ),
                Expanded(
                  child: ZCard(
                    onTap: () {
                      ZLaunchUrl.launchUrl(AppLINKS.instagramUrl);
                    },
                    color: Colors.transparent,
                    margin: EdgeInsets.zero,
                    padding: EdgeInsets.zero,
                    child: Column(
                      children: [
                        Image.asset('assets/images/icon_instagram.png', height: 35),
                        SizedBox(height: 8),
                        Text('Instagram'),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: MediaQuery.of(context).size.height * .2)
        ],
      ),
    );
  }
}

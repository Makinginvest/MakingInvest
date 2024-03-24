import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_appbar_title.dart';
import 'package:stockwatchalert/components/z_card.dart';
import 'package:stockwatchalert/components/z_image_display.dart';
import 'package:stockwatchalert/components/z_text_form_field_bottom_sheet.dart';
import 'package:stockwatchalert/models_providers/app_provider.dart';
import 'package:stockwatchalert/utils/z_format.dart';

class ScreenStockPage extends StatefulWidget {
  const ScreenStockPage({super.key});

  @override
  State<ScreenStockPage> createState() => _ScreenStockPageState();
}

class _ScreenStockPageState extends State<ScreenStockPage> {
  @override
  Widget build(BuildContext context) {
    final AppProvider appProvider = Provider.of<AppProvider>(context);
    final isLoadingStockScreener = appProvider.isLoadingStockScreener;
    final stockScreenerData = appProvider.stockScreenerDataFiltered;
    final filterRatingRecommendation = appProvider.filterStockRatingRecommendation;
    final selectedFilterStockRatingRecommendation = appProvider.selectedFilterStockRatingRecommendation;
    print(stockScreenerData.length);
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: Scaffold(
        appBar: AppBar(
          title: AppBarTitle(),
        ),
        body: ListView(
          padding: EdgeInsets.symmetric(horizontal: 16),
          children: [
            SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: ZTextFormFieldBottomSheet(
                    margin: EdgeInsets.symmetric(),
                    hint: 'Min Price',
                    items: ['0', '1', '2', '3', '4', '5', '10', '15', '20', '50', '100', '200', '500'],
                    initialValue: appProvider.stockScreenerMinClose.toString(),
                    onValueChanged: (v) {
                      appProvider.stockScreenerMinClose = num.parse(v);
                      setState(() {});
                    },
                  ),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: ZTextFormFieldBottomSheet(
                    margin: EdgeInsets.symmetric(),
                    hint: 'Max Price',
                    items: ['0', '1', '2', '3', '4', '5', '10', '15', '20', '50', '100', '200', '500', '1000', '50000', '500000'],
                    initialValue: appProvider.stockScreenerMaxClose.toString(),
                    onValueChanged: (v) {
                      appProvider.stockScreenerMaxClose = num.parse(v);
                      setState(() {});
                    },
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: ZTextFormFieldBottomSheet(
                    margin: EdgeInsets.symmetric(),
                    hint: 'Min Volume',
                    items: ['10000', '20000', '50000', '100000', '500000', '1000000'],
                    initialValue: appProvider.stockScreenerMinVolume.toString(),
                    onValueChanged: (v) {
                      appProvider.stockScreenerMinVolume = num.parse(v);
                      setState(() {});
                    },
                  ),
                ),
                IconButton(
                    onPressed: () async {
                      appProvider.getStockScreener();
                    },
                    icon: Icon(Icons.search))
              ],
            ),
            Container(
              margin: EdgeInsets.symmetric(vertical: 8),
              height: 30,
              child: ListView(
                shrinkWrap: true,
                scrollDirection: Axis.horizontal,
                children: [
                  for (var x in filterRatingRecommendation)
                    ZCard(
                      borderRadiusColor: selectedFilterStockRatingRecommendation == x ? Colors.blue : null,
                      onTap: () => appProvider.selectedFilterStockRatingRecommendation = x,
                      child: Text(x),
                      margin: EdgeInsets.symmetric(horizontal: 4),
                      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    )
                ],
              ),
            ),
            for (var c in stockScreenerData)
              ZCard(
                margin: EdgeInsets.symmetric(vertical: 4),
                padding: EdgeInsets.symmetric(vertical: 8, horizontal: 8),
                child: Row(children: [
                  ZImageDisplay(
                    image: c.image,
                    width: 40,
                    height: 40,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  SizedBox(width: 8),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(c.symbol),
                      if (c.ratingRecommendation != '') Text(c.ratingRecommendation),
                    ],
                  ),
                  Spacer(),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(ZFormat.numToMoney(c.close)),
                      Text(ZFormat.toPrecision(c.volume, 0).toString()),
                    ],
                  )
                ]),
              ),
            if (isLoadingStockScreener)
              Column(
                children: [
                  SizedBox(height: MediaQuery.of(context).size.height * .2),
                  Center(child: CircularProgressIndicator()),
                ],
              )
          ],
        ),
      ),
    );
  }
}

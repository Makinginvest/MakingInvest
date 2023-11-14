import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../components/z_card.dart';
import '../../components/z_image_display.dart';
import '../../models_providers/app_provider.dart';
import '../../utils/z_launch_url.dart';

class IcoPage extends StatefulWidget {
  const IcoPage({super.key});

  @override
  State<IcoPage> createState() => _IcoPageState();
}

class _IcoPageState extends State<IcoPage> {
  @override
  Widget build(BuildContext context) {
    final AppProvider appProvider = Provider.of<AppProvider>(context);
    final offeringAggr = appProvider.offeringAggr;

    return Scaffold(
      appBar: AppBar(
        title: Text('ICO'),
      ),
      body: Container(
        margin: EdgeInsets.symmetric(horizontal: 16),
        child: ListView(
          children: [
            for (var x in offeringAggr.data)
              ZCard(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                margin: EdgeInsets.symmetric(vertical: 8),
                onTap: () => ZLaunchUrl.launchUrl(x.link),
                child: Row(
                  children: [
                    ZImageDisplay(image: x.image, width: 80, height: 80, borderRadius: BorderRadius.circular(999)),
                    SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(x.title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                          SizedBox(height: 8),
                          Text(
                            x.body.trim(),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}

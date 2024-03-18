import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../../utils/z_launch_url.dart';

class RenderHTMLUrlPage extends StatefulWidget {
  const RenderHTMLUrlPage({required this.url, super.key});

  final String url;
  @override
  State<RenderHTMLUrlPage> createState() => _RenderHTMLUrlPageState();
}

class _RenderHTMLUrlPageState extends State<RenderHTMLUrlPage> {
  late final WebViewController controller;

  @override
  void initState() { 
    super.initState();

    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (int progress) {
            debugPrint('progress');
          },
          onPageStarted: (String url) {
            debugPrint('started');
          },
          onPageFinished: (String url) {
            debugPrint('finished');
          },
        ),
      )
      ..enableZoom(true)
      ..loadRequest(Uri.parse(widget.url));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          TextButton(
            onPressed: () => ZLaunchUrl.launchUrl(widget.url),
            child: Text(
              'Open in Browser',
              style: TextStyle(color: context.isDarkMode ? Colors.white : Colors.black),
            ),
          ),
        ],
      ),
      body: WebViewWidget(controller: controller),
    );
  }
}

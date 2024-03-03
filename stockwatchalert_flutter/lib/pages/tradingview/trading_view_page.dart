import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import 'trading_view_widget.dart';

class TradingViewPage extends StatefulWidget {
  const TradingViewPage({required this.symbol, super.key});

  final String symbol;
  @override
  State<TradingViewPage> createState() => _TradingViewPageState();
}

class _TradingViewPageState extends State<TradingViewPage> {
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
      ..loadHtmlString(TradingViewWidget.cryptoNameAndSource(widget.symbol));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.symbol),
      ),
      body: WebViewWidget(controller: controller),
    );
  }
}

class TradingViewWidget {
  static String cryptoNameAndSource(String name) {
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<title>Load file or HTML string example</title>
</head>
<body>
<div class="tradingview-widget-container">
<div id="tradingview_4418d">
</div>
<div class="tradingview-widget-copyright">
<a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
</a>
</div>
<script type="text/javascript" src="https://s3.tradingview.com/tv.js">
</script>
<script type="text/javascript">
new TradingView.widget({
  "width": "100%",
  "height": 1300,
  "symbol": "$name",
  "interval": "240",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "hide_top_toolbar": true,
  "save_image": false,
  "container_id": "tradingview_81f77",
   "studies": [
    "ROC@tv-basicstudies",
    "StochasticRSI@tv-basicstudies",
    "MASimple@tv-basicstudies"
  ],
  });
</script>
</div>
</body>
</html>''';
  }
}

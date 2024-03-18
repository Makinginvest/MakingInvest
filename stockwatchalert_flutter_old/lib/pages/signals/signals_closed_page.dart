import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../components/z_signal_card.dart';
import '../../components/z_text_form_field_search.dart';
import '../../models/signal_aggr.dart';
import '../../models_providers/app_controls_provider.dart';
import '../../models_services/api_signals_service.dart';

class SignalsClosedPage extends StatefulWidget {
  SignalsClosedPage({Key? key, required this.signalAggr, this.signal, this.showSearch = true}) : super(key: key);
  final SignalAggr signalAggr;
  final Signal? signal;
  final bool showSearch;

  @override
  State<SignalsClosedPage> createState() => _SignalsClosedPageState();
}

class _SignalsClosedPageState extends State<SignalsClosedPage> with TickerProviderStateMixin {
  String search = '';
  bool isLoadingInit = true;
  SignalAggr? signalAggrX = SignalAggr();
  List<Signal> signals = [];

  @override
  void initState() {
    getSignalAggrClose();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    List<Signal> _signals = getFilteredSignals(search, signals);
    return Scaffold(
      appBar: AppBar(
        title: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (widget.signal == null) Text('${widget.signalAggr.nameType}', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, height: 1.5)),
            if (widget.signal != null) Text('${widget.signal!.symbol}', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, height: 1.5)),
            SizedBox(width: 4),
            Text('Signals (${signals.length})', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, height: 1.5)),
          ],
        ),
        actions: [],
      ),
      body: Column(
        children: [
          if (isLoadingInit) Expanded(child: Center(child: CircularProgressIndicator())),
          if (!isLoadingInit && signals.isEmpty) Expanded(child: Center(child: Text('No Signals'))),
          if (signals.length != 0)
            Column(
              children: [
                if (widget.showSearch)
                  Container(
                    margin: EdgeInsets.symmetric(horizontal: 16),
                    child: ZSearch(
                      onValueChanged: ((v) {
                        search = v;
                        setState(() {});
                      }),
                    ),
                  ),
                SizedBox(height: 4)
              ],
            ),
          if (signals.length != 0) Expanded(child: _buildListView(_signals)),
        ],
      ),
    );
  }

  List<Signal> getFilteredSignals(String s, List<Signal> signals) {
    if (s == '') return signals;

    return signals.where((signal) {
      return signal.symbol.toLowerCase().contains(s.toLowerCase());
    }).toList();
  }

  void getSignalAggrClose() async {
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context, listen: false);
    SignalAggr? signalAggr;
    if (widget.signal == null) {
      signalAggr = await ApiSignalsService.getClosedSignalAggr(signalAggr: widget.signalAggr, apiUrl: appControlsProvider.appControls.apiUrl);
    }

    if (widget.signal != null) {
      signalAggr = await ApiSignalsService.getClosedSignalAggrBySymbol(signalAggrx: widget.signalAggr, signal: widget.signal!, apiUrl: appControlsProvider.appControls.apiUrl);
    }

    if (signalAggr == null) {
      isLoadingInit = false;
      setState(() {});
    }

    signalAggrX = signalAggr;
    signals = signalAggr?.signals ?? [];
    isLoadingInit = false;
    setState(() {});
  }

  Scrollbar _buildListView(List<Signal> signals) {
    return Scrollbar(
      child: ListView.builder(
        itemCount: signals.length,
        itemBuilder: ((context, index) => Column(
              children: [ZSignalCard(signal: signals[index], isClosed: true)],
            )),
      ),
    );
  }

  Expanded buildSignalItem({required String title, required String value, String type = 'Bull', isStopLoss = false}) {
    Color textColor = (isStopLoss && type == 'Bull')
        ? Color(0xFF0AD61E)
        : (isStopLoss && type == 'Bear')
            ? Color(0xFFFF0002)
            : Colors.white;
    return Expanded(
        child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: TextStyle(color: Color(0xFFA9A9A9), fontSize: 10)),
        SizedBox(height: 8),
        Text(value, style: TextStyle(fontSize: 13, color: textColor)),
      ],
    ));
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:stockwatchalert/components/z_signal_card_v1.dart';
import 'package:stockwatchalert/components/z_text_form_field_search.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';
import 'package:stockwatchalert/models_services/api_signals_service.dart';

import '../../models_providers/app_controls_provider.dart';

class SignalsClosedPageV1 extends StatefulWidget {
  SignalsClosedPageV1({Key? key, required this.signalAggr, this.signal, this.showSearch = true}) : super(key: key);
  final SignalAggrV1 signalAggr;
  final SignalV1? signal;
  final bool showSearch;

  @override
  State<SignalsClosedPageV1> createState() => _SignalsClosedPageV1State();
}

class _SignalsClosedPageV1State extends State<SignalsClosedPageV1> with TickerProviderStateMixin {
  String search = '';
  bool isLoadingInit = true;
  SignalAggrV1? signalAggrX = SignalAggrV1();
  List<SignalV1> signals = [];

  @override
  void initState() {
    getSignalAggrClose();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    List<SignalV1> _signals = getFilteredSignals(search, signals);
    return GestureDetector(
      onTap: () => FocusScope.of(context).requestFocus(FocusNode()),
      child: Scaffold(
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
                        hintText: 'Search symbols',
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
      ),
    );
  }

  List<SignalV1> getFilteredSignals(String s, List<SignalV1> signals) {
    if (s == '') return signals;

    return signals.where((signal) {
      return signal.symbol.toLowerCase().contains(s.toLowerCase());
    }).toList();
  }

  void getSignalAggrClose() async {
    AppControlsProvider appControlsProvider = Provider.of<AppControlsProvider>(context, listen: false);
    SignalAggrV1? signalAggr;
    if (widget.signal == null) {
      signalAggr = await ApiSignalsService.getClosedSignalAggrV1(signalAggr: widget.signalAggr, apiUrl: appControlsProvider.appControls.apiUrlV1);
    }

    if (widget.signal != null) {
      // signalAggr = await ApiSignalsService.getClosedSignalAggrBySymbol(signalAggrx: widget.signalAggr, signal: widget.signal!, apiUrl: appControlsProvider.appControls.apiUrl);
    }

    isLoadingInit = false;
    setState(() {});

    signalAggrX = signalAggr;
    signals = signalAggr?.signals ?? [];
    isLoadingInit = false;
    setState(() {});
  }

  Scrollbar _buildListView(List<SignalV1> signals) {
    return Scrollbar(
      child: ListView.builder(
        itemCount: signals.length,
        itemBuilder: ((context, index) => Column(
              children: [ZSignalCardV1(signal: signals[index], isClosed: true)],
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

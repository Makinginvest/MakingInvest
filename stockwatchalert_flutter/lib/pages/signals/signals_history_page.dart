import 'package:flutter/material.dart';

class SignalsHistoryPage extends StatefulWidget {
  SignalsHistoryPage({Key? key}) : super(key: key);

  @override
  State<SignalsHistoryPage> createState() => _SignalsHistoryPageState();
}

class _SignalsHistoryPageState extends State<SignalsHistoryPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('History')),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Row(),
          Text('Comming soon'),
        ],
      ),
    );
  }
}

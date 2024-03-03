import 'package:flutter/material.dart';

class SignalsHowPage extends StatefulWidget {
  SignalsHowPage({Key? key}) : super(key: key);

  @override
  State<SignalsHowPage> createState() => _SignalsHowPageState();
}

class _SignalsHowPageState extends State<SignalsHowPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('How')),
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

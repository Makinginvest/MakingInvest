import 'package:flutter/material.dart';

import '../../components/z_annoucement_card.dart';
import '../../models/announcement_aggr.dart';

class AnnoucementsPage extends StatefulWidget {
  const AnnoucementsPage({Key? key, required this.annoucements}) : super(key: key);
  final List<Announcement> annoucements;

  @override
  State<AnnoucementsPage> createState() => _AnnoucementsPageState();
}

class _AnnoucementsPageState extends State<AnnoucementsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Annoucements'),
      ),
      body: ListView.builder(
        shrinkWrap: true,
        physics: ClampingScrollPhysics(),
        itemCount: widget.annoucements.length,
        itemBuilder: ((context, index) => Column(
              children: [
                if (index == 0) SizedBox(height: 8),
                ZAnnoucementCard(announcement: (widget.annoucements[index])),
                if (index == widget.annoucements.length - 1) SizedBox(height: 8),
              ],
            )),
      ),
    );
  }
}

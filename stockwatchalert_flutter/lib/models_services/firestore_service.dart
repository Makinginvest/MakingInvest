import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:stockwatchalert/models/news_aggr.dart';
import 'package:stockwatchalert/models/signal_aggr_v1.dart';

import 'package:stockwatchalert/models/support.dart';

import 'package:stockwatchalert/models/video_lesson_aggr.dart';

import '../models/announcement_aggr.dart';
import '../models/app_controls_public.dart';
import '../models/post_aggr.dart';

class FirestoreService {
  static Stream<AppControlsPublic> streamAppControlsPublic() {
    var ref = FirebaseFirestore.instance.collection('appControlsPublic').doc('appControlsPublic').snapshots();
    return ref.map((doc) => AppControlsPublic.fromJson({...?doc.data(), "id": doc.id}));
  }

  static Future<AppControlsPublic> getAppControlsPublic() async {
    var ref = FirebaseFirestore.instance.collection('appControlsPublic').doc('appControlsPublic');
    var doc = await ref.get();
    return AppControlsPublic.fromJson({...?doc.data(), "id": doc.id});
  }

/* ---------------------------- NOTE NEWS SERVICE --------------------------- */
  static Stream<NewsAggr> streamNewsAggr() {
    var ref = FirebaseFirestore.instance.collection('newsAggr').doc('newsAggr').snapshots();
    return ref.map((doc) => NewsAggr.fromJson({...?doc.data(), "id": doc.id}));
  }

  static Stream<VideoLessonAggr> streamVideoLessonsAggr() {
    var ref = FirebaseFirestore.instance.collection('videoLessonsAggr').doc('videoLessonsAggr').snapshots();
    return ref.map((doc) => VideoLessonAggr.fromJson({...?doc.data(), "id": doc.id}));
  }

  static Stream<AnnouncementAggr> streamAnnoucementAggr() {
    var ref = FirebaseFirestore.instance.collection('announcementsAggr').doc('announcementsAggr').snapshots();
    return ref.map((doc) => AnnouncementAggr.fromJson({...?doc.data(), "id": doc.id}));
  }

  static Stream<PostAggr> streamPostsAggr() {
    var ref = FirebaseFirestore.instance.collection('postsAggr').doc('postsAggr').snapshots();
    return ref.map((doc) => PostAggr.fromJson({...?doc.data(), "id": doc.id}));
  }

  static Stream<List<SignalAggrV1>> streamSignalsXAggrOpenV1() {
    var ref = FirebaseFirestore.instance.collection('signalsAggrOpenV1').where('nameIsActive', isEqualTo: true).orderBy('nameSort', descending: false).snapshots();

    var x = ref.map((doc) => doc.docs.map((doc) => SignalAggrV1.fromJson({...doc.data(), "id": doc.id})).toList());
    x = x.map((list) => list.map((signalAggr) => signalAggr..signals.sort((a, b) => b.getEntryDateTimeUtc().compareTo(a.getEntryDateTimeUtc()))).toList());
    return x.map((list) => list..sort((a, b) => a.nameSort.compareTo(b.nameSort)));
  }

/* -------------------------- NOTE SUPPORT SERVICE -------------------------- */
  static Future<bool> addSupport(Support support) async {
    var ref = FirebaseFirestore.instance.collection('supports').doc();
    try {
      await ref.set(support.toJson());
      return true;
    } catch (e) {
      return false;
    }
  }
}

import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

const AndroidNotificationChannel channel = AndroidNotificationChannel(
  'high_importance_channel',
  "High Importance Notifcations",
  description: "This channel is used important notification",
  groupId: "Notification_group",
);

var androidPlatformChannelSpecifics = AndroidNotificationDetails(channel.id, channel.name,
    channelDescription: channel.description,
    importance: Importance.max,
    priority: Priority.high,
    ticker: 'ticker',
    groupKey: channel.groupId,
    setAsGroupSummary: true);

class FirebaseNotificationService {
  static init() async {
    final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;

    NotificationSettings settings = await _firebaseMessaging.requestPermission(
        alert: true, announcement: false, badge: true, carPlay: false, criticalAlert: false, provisional: false, sound: true);
    if (settings.authorizationStatus == AuthorizationStatus.authorized) print('User granted permission');
    if (settings.authorizationStatus == AuthorizationStatus.provisional) print('User granted provisional permission');
    if (settings.authorizationStatus == AuthorizationStatus.denied) print('User declined or has not accepted permission');

    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('onMessage: $message');
      _handleNotification(message);
    });

    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print('onMessageOpenedApp: $message');
      _handleNotification(message);
    });

    FirebaseMessaging.onBackgroundMessage(myBackgroundMessageHandler);
  }

  static Future<void> _handleNotification(RemoteMessage message) async {
    print('handleNotification, ${message.data.toString()}');
    String title = message.notification?.title ?? '';
    String body = message.notification?.body ?? '';

    if (message.data.isNotEmpty) {
      title = title == '' ? message.data['title'] : title;
      body = body == '' ? message.data['body'] : body;
    }

    try {
      FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = new FlutterLocalNotificationsPlugin();
      const AndroidInitializationSettings initializationSettingsAndroid = AndroidInitializationSettings('notification_icon');
      final DarwinInitializationSettings initializationSettingsDarwin = DarwinInitializationSettings();

      final InitializationSettings initializationSettings =
          InitializationSettings(android: initializationSettingsAndroid, iOS: initializationSettingsDarwin);
      await flutterLocalNotificationsPlugin.initialize(initializationSettings);

      var iOSPlatformChannelSpecifics = DarwinNotificationDetails();
      var platformChannelSpecifics = NotificationDetails(android: androidPlatformChannelSpecifics, iOS: iOSPlatformChannelSpecifics);
      await flutterLocalNotificationsPlugin.show(message.hashCode, title, body, platformChannelSpecifics, payload: 'Default_Sound');
    } catch (e) {
      print('myMessageHandlerERROR, ${e.toString()}');
    }
  }
}

Future<void> myBackgroundMessageHandler(RemoteMessage message) async {
  if (message.notification != null) return;

  String title = message.notification?.title ?? '';
  String body = message.notification?.body ?? '';

  if (message.data.isNotEmpty) {
    title = title == '' ? message.data['title'] : title;
    body = body == '' ? message.data['body'] : body;
  }

  try {
    FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = new FlutterLocalNotificationsPlugin();
    const AndroidInitializationSettings initializationSettingsAndroid = AndroidInitializationSettings('notification_icon');
    final DarwinInitializationSettings initializationSettingsDarwin = DarwinInitializationSettings();
    final InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid, iOS: initializationSettingsDarwin);
    await flutterLocalNotificationsPlugin.initialize(initializationSettings);

    var iOSPlatformChannelSpecifics = DarwinNotificationDetails();
    var platformChannelSpecifics = NotificationDetails(android: androidPlatformChannelSpecifics, iOS: iOSPlatformChannelSpecifics);
    await flutterLocalNotificationsPlugin.show(message.hashCode, title, body, platformChannelSpecifics, payload: 'Default_Sound');
  } catch (e) {
    print('myBackgroundMessageHandlerERROR, ${e.toString()}');
  }
}

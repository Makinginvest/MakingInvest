import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';

DateTime? parseToDateTime(dynamic date) {
  if (date == null) return null;

  DateTime? d;
  if (date is DateTime) d = date;
  if (date is Timestamp) d = date.toDate();
  if (date is String) d = DateTime.tryParse(date);
  if (date is num) d = DateTime.fromMillisecondsSinceEpoch(date.toInt());

  if (date is Timestamp) {
    return date.toDate();
  }

  if (d is DateTime) {
    if (d.isUtc == true) return d;
    return DateTime.utc(d.year, d.month, d.day, d.hour, d.minute, d.second, d.millisecond, d.microsecond);
  }

  return null;
}

String? parseToDatetimeIOSString(dynamic date) {
  if (date is DateTime) return date.toUtc().toIso8601String();
  if (date is Timestamp) return date.toDate().toUtc().toIso8601String();
  return '';
}

String? parseToDayString(dynamic date) {
  DateTime? dateTime = parseToDateTime(date);
  if (dateTime == null) return null;
  return DateFormat("d MMM, y").format(dateTime);
}

String? parseToDayUTCString(dynamic date) {
  DateTime? dateTime = parseToDateTime(date);
  if (dateTime == null) return null;
  dateTime = dateTime.toLocal();
  return DateFormat("d MMM, y").format(dateTime);
}

String? parseToDayTimeString(dynamic date) {
  DateTime? dateTime = parseToDateTime(date);
  if (dateTime == null) return null;
  return DateFormat("d MMM, y @ h:mm:ss a").format(dateTime);
}

String? parseToDayTimeUTCString(dynamic date) {
  DateTime? dateTime = parseToDateTime(date);
  if (dateTime == null) return null;
  dateTime = dateTime.toLocal();
  return DateFormat("d MMM, y @ h:mm:ss a").format(dateTime);
}

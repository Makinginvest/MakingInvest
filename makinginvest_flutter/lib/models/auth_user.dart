import 'package:json_annotation/json_annotation.dart';

import '../utils/z_format.dart';
import '_parsers.dart';

part 'auth_user.g.dart';

@JsonSerializable(explicitToJson: true)
class AuthUser {
  String? id;
  @JsonKey(defaultValue: '')
  String email;
  @JsonKey(defaultValue: '')
  String lastLoginDateTimeDevice;
  @JsonKey(defaultValue: [])
  List<String> favoriteSignals;
  @JsonKey(defaultValue: [])
  List<String> devTokens;
  @JsonKey(defaultValue: '')
  String appVersion;
  @JsonKey(defaultValue: 0)
  num appBuildNumber;
  //
  @JsonKey(defaultValue: [])
  List<String> notificationsDisabled;
  @JsonKey(defaultValue: [])
  List<String> notificationsRiskyEnabled;
  //
  bool isAnonymous;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? createdDateTime;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime)
  DateTime? lastLoginDateTime;

  // subcription
  @JsonKey(defaultValue: false)
  bool subRevenuecatIsActive;
  @JsonKey(defaultValue: false)
  bool subRevenuecatWillRenew;
  @JsonKey(defaultValue: '')
  String subRevenuecatPeriodType;
  @JsonKey(defaultValue: '')
  String subRevenuecatProductIdentifier;
  @JsonKey(defaultValue: false)
  bool subRevenuecatIsSandbox;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, defaultValue: null)
  DateTime? subRevenuecatOriginalPurchaseDateTime;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, defaultValue: null)
  DateTime? subRevenuecatLatestPurchaseDateTime;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, defaultValue: null)
  DateTime? subRevenuecatExpirationDateTime;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, defaultValue: null)
  DateTime? subRevenuecatUnsubscribeDetectedDateTime;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, defaultValue: null)
  DateTime? subRevenuecatBillingIssueDetectedDateTime;
  @JsonKey(defaultValue: false)
  bool subIsLifetime;
  @JsonKey(fromJson: parseToDateTime, toJson: parseToDateTime, defaultValue: null)
  DateTime? subIsLifetimeExpirationDateTime;

  AuthUser()
      : email = '',
        favoriteSignals = [],
        devTokens = [],
        lastLoginDateTimeDevice = '',
        appVersion = '',
        appBuildNumber = 0,
        notificationsDisabled = [],
        notificationsRiskyEnabled = [],
        isAnonymous = true,
        createdDateTime = null,
        lastLoginDateTime = null,
        subRevenuecatIsActive = false,
        subRevenuecatWillRenew = false,
        subRevenuecatPeriodType = '',
        subRevenuecatProductIdentifier = '',
        subRevenuecatIsSandbox = false,
        subRevenuecatOriginalPurchaseDateTime = null,
        subRevenuecatLatestPurchaseDateTime = null,
        subRevenuecatExpirationDateTime = null,
        subRevenuecatUnsubscribeDetectedDateTime = null,
        subRevenuecatBillingIssueDetectedDateTime = null,
        subIsLifetime = false,
        subIsLifetimeExpirationDateTime = null;

  factory AuthUser.fromJson(Map<String, dynamic> json) => _$AuthUserFromJson(json);
  Map<String, dynamic> toJson() => _$AuthUserToJson(this)..remove('id');

  // functions
  bool get hasActiveSubscription => verifyRevenuecatSubscription(this) || verifySubLifetime(this);
  bool get hasLifetime => verifySubLifetime(this);

  String getSubscriptionEndDateTime() {
    if (verifySubLifetime(this)) {
      if (subIsLifetimeExpirationDateTime == null) return 'Lifetime';
      return ZFormat.dateTimeFormatStr(subIsLifetimeExpirationDateTime);
    }
    if (verifyRevenuecatSubscription(this)) return ZFormat.dateTimeFormatStr(subRevenuecatExpirationDateTime);
    return '';
  }
}

bool verifyRevenuecatSubscription(AuthUser authUser) {
  if (authUser.subRevenuecatExpirationDateTime == null) return false;
  if (timeInUtc(authUser.subRevenuecatExpirationDateTime!).isAfter(timeInUtc(DateTime.now()))) return true;
  return false;
}

bool verifySubLifetime(AuthUser authUser) {
  if (authUser.subIsLifetime == false) return false;
  if (authUser.subIsLifetimeExpirationDateTime == null) return true;
  if (timeInUtc(authUser.subIsLifetimeExpirationDateTime!).isAfter(timeInUtc(DateTime.now()))) return true;
  return false;
}

DateTime timeInUtc(DateTime d) {
  return DateTime.utc(d.year, d.month, d.day, d.hour, d.minute, d.second, d.millisecond, d.microsecond);
}

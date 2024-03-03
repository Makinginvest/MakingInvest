// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'auth_user.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

AuthUser _$AuthUserFromJson(Map<String, dynamic> json) => AuthUser()
  ..id = json['id'] as String?
  ..email = json['email'] as String? ?? ''
  ..lastLoginDateTimeDevice = json['lastLoginDateTimeDevice'] as String? ?? ''
  ..favoriteSignals = (json['favoriteSignals'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      []
  ..devTokens =
      (json['devTokens'] as List<dynamic>?)?.map((e) => e as String).toList() ??
          []
  ..appVersion = json['appVersion'] as String? ?? ''
  ..appBuildNumber = json['appBuildNumber'] as num? ?? 0
  ..isOnboarded = json['isOnboarded'] as bool? ?? false
  ..notificationsDisabled = (json['notificationsDisabled'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      []
  ..notificationsRiskyEnabled =
      (json['notificationsRiskyEnabled'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          []
  ..isAnonymous = json['isAnonymous'] as bool
  ..createdDateTime = parseToDateTime(json['createdDateTime'])
  ..lastLoginDateTime = parseToDateTime(json['lastLoginDateTime'])
  ..subRevenuecatIsActive = json['subRevenuecatIsActive'] as bool? ?? false
  ..subRevenuecatWillRenew = json['subRevenuecatWillRenew'] as bool? ?? false
  ..subRevenuecatPeriodType = json['subRevenuecatPeriodType'] as String? ?? ''
  ..subRevenuecatProductIdentifier =
      json['subRevenuecatProductIdentifier'] as String? ?? ''
  ..subRevenuecatIsSandbox = json['subRevenuecatIsSandbox'] as bool? ?? false
  ..subRevenuecatOriginalPurchaseDateTime =
      parseToDateTime(json['subRevenuecatOriginalPurchaseDateTime'])
  ..subRevenuecatLatestPurchaseDateTime =
      parseToDateTime(json['subRevenuecatLatestPurchaseDateTime'])
  ..subRevenuecatExpirationDateTime =
      parseToDateTime(json['subRevenuecatExpirationDateTime'])
  ..subRevenuecatUnsubscribeDetectedDateTime =
      parseToDateTime(json['subRevenuecatUnsubscribeDetectedDateTime'])
  ..subRevenuecatBillingIssueDetectedDateTime =
      parseToDateTime(json['subRevenuecatBillingIssueDetectedDateTime'])
  ..subIsLifetime = json['subIsLifetime'] as bool? ?? false
  ..subIsLifetimeExpirationDateTime =
      parseToDateTime(json['subIsLifetimeExpirationDateTime']);

Map<String, dynamic> _$AuthUserToJson(AuthUser instance) => <String, dynamic>{
      'id': instance.id,
      'email': instance.email,
      'lastLoginDateTimeDevice': instance.lastLoginDateTimeDevice,
      'favoriteSignals': instance.favoriteSignals,
      'devTokens': instance.devTokens,
      'appVersion': instance.appVersion,
      'appBuildNumber': instance.appBuildNumber,
      'isOnboarded': instance.isOnboarded,
      'notificationsDisabled': instance.notificationsDisabled,
      'notificationsRiskyEnabled': instance.notificationsRiskyEnabled,
      'isAnonymous': instance.isAnonymous,
      'createdDateTime': parseToDateTime(instance.createdDateTime),
      'lastLoginDateTime': parseToDateTime(instance.lastLoginDateTime),
      'subRevenuecatIsActive': instance.subRevenuecatIsActive,
      'subRevenuecatWillRenew': instance.subRevenuecatWillRenew,
      'subRevenuecatPeriodType': instance.subRevenuecatPeriodType,
      'subRevenuecatProductIdentifier': instance.subRevenuecatProductIdentifier,
      'subRevenuecatIsSandbox': instance.subRevenuecatIsSandbox,
      'subRevenuecatOriginalPurchaseDateTime':
          parseToDateTime(instance.subRevenuecatOriginalPurchaseDateTime),
      'subRevenuecatLatestPurchaseDateTime':
          parseToDateTime(instance.subRevenuecatLatestPurchaseDateTime),
      'subRevenuecatExpirationDateTime':
          parseToDateTime(instance.subRevenuecatExpirationDateTime),
      'subRevenuecatUnsubscribeDetectedDateTime':
          parseToDateTime(instance.subRevenuecatUnsubscribeDetectedDateTime),
      'subRevenuecatBillingIssueDetectedDateTime':
          parseToDateTime(instance.subRevenuecatBillingIssueDetectedDateTime),
      'subIsLifetime': instance.subIsLifetime,
      'subIsLifetimeExpirationDateTime':
          parseToDateTime(instance.subIsLifetimeExpirationDateTime),
    };

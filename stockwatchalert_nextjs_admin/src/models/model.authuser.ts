import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';
import { X } from 'tabler-icons-react';
import { convertToDate } from '../utils/convert_to_date';

export class AuthUserModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() appBuildNumber: number = 0;
  @Expose() appVersion: string = '';
  @Expose() email: string = '';
  @Expose() isActive: boolean = true;
  @Expose() isNotificationEnabled: boolean = true;
  @Expose() profileImage: string = '';
  @Expose() userId: string = '';
  @Expose() username: string = '';
  @Expose() roles: string[] = [];
  @Expose() isSuperAdmin: boolean = false;
  @Expose() isAdmin: boolean = false;
  @Expose() isTestAdmin: boolean = false;
  @Expose() @Type(() => Date) createdDateTime?: Date | null = null;
  @Expose() @Type(() => Date) lastLoginDateTime?: Date | null = null;

  @Expose() subIsLifetime: boolean = false;
  @Expose() subIsLifetimeExpirationDateTime?: Date | null = null;
  @Expose() @Type(() => Date) subSubscriptionEndDate?: Date | null = null;

  @Expose() stripeLiveCustomerId?: string | null = null;
  @Expose() stripeTestCustomerId?: string | null = null;
  @Expose() @Type(() => Date) subStripeEnd?: Date | null = null;
  @Expose() subStripeLivemode: boolean = false;
  @Expose() subStripePlan: string = '';
  @Expose() subStripePlanAmt: number = 0;
  @Expose() subStripePlanId: string = '';
  @Expose() @Type(() => Date) subStripeStart?: Date | null = null;
  @Expose() subStripeStatus: string = '';

  @Expose() subRevenuecatIsActive: boolean = false;
  @Expose() subRevenuecatWillRenew: boolean = false;
  @Expose() subRevenuecatPeriodType: string = '';
  @Expose() subRevenuecatProductIdentifier: string = '';
  @Expose() subRevenuecatIsSandbox: boolean = false;
  @Expose() @Type(() => Date) subRevenuecatOriginalPurchaseDateTime?: Date | null = null;
  @Expose() @Type(() => Date) subRevenuecatLatestPurchaseDateTime?: Date | null = null;
  @Expose() @Type(() => Date) subRevenuecatExpirationDateTime?: Date | null = null;
  @Expose() @Type(() => Date) subRevenuecatUnsubscribeDetectedAt?: Date | null = null;
  @Expose() @Type(() => Date) subRevenuecatBillingIssueDetectedAt?: Date | null = null;

  static fromJson(json: any): AuthUserModel {
    json = convertObjectDate(json);
    return plainToInstance(AuthUserModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: AuthUserModel): any {
    return instanceToPlain(order);
  }

  get hasAdminRole(): boolean {
    if (this.isSuperAdmin || this.isAdmin || this.isTestAdmin) return true;
    return false;
  }

  get getRoleString(): string {
    if (this.isSuperAdmin) return 'SAdmin';
    if (this.isAdmin) return 'Admin';
    if (this.isTestAdmin) return 'TAdmin';
    return 'User';
  }

  get getHasSubscription(): boolean {
    if (this.subIsLifetime) return true;
    if (this.subStripeEnd && this.subStripeEnd > new Date()) return true;
    if (this.subRevenuecatExpirationDateTime && this.subRevenuecatExpirationDateTime > new Date()) return true;
    return false;
  }
  get getHasSubscriptionString(): String {
    if (this.subIsLifetime) return 'Lifetime';
    if (this.subStripeEnd && this.subStripeEnd > new Date()) return 'Stripe';
    if (this.subRevenuecatExpirationDateTime && this.subRevenuecatExpirationDateTime > new Date()) return 'Revenuecat';
    return 'None';
  }

  get getSubscriptionEndDate(): Date | null | undefined {
    if (this.subIsLifetime) {
      if (this.subIsLifetimeExpirationDateTime) return this.subIsLifetimeExpirationDateTime;
      return new Date(2099, 11, 31);
    }
    if (this.subRevenuecatExpirationDateTime == null && this.subStripeEnd == null) return null;
    if (this.subRevenuecatExpirationDateTime != null) return this.subRevenuecatExpirationDateTime;
    return this.subStripeEnd;
  }
}

function convertObjectDate(json: any) {
  json.createdDateTime = convertToDate(json.createdDateTime);
  json.lastLoginDateTime = convertToDate(json.lastLoginDateTime);
  json.subIsLifetimeExpirationDateTime = convertToDate(json.subIsLifetimeExpirationDateTime);
  json.subSubscriptionEndDateTime = convertToDate(json.subSubscriptionEndDateTime);
  json.subStripeEnd = convertToDate(json.subStripeEnd);
  json.subStripeStart = convertToDate(json.subStripeStart);
  json.subRevenuecatOriginalPurchaseDateTime = convertToDate(json.subRevenuecatOriginalPurchaseDateTime);
  json.subRevenuecatLatestPurchaseDateTime = convertToDate(json.subRevenuecatLatestPurchaseDateTime);
  json.subRevenuecatExpirationDateTime = convertToDate(json.subRevenuecatExpirationDateTime);
  json.subRevenuecatUnsubscribeDetectedAt = convertToDate(json.subRevenuecatUnsubscribeDetectedAt);
  json.subRevenuecatBillingIssueDetectedAt = convertToDate(json.subRevenuecatBillingIssueDetectedAt);

  return json;
}

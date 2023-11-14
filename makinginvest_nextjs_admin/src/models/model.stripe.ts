import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';

export class StripeModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() stripeTestKey: string = '';
  @Expose() stripeLiveKey: string = '';
  @Expose() stripeMonthlyProductTest: string = '';
  @Expose() stripeYearlyProductTest: string = '';
  @Expose() stripeMonthlyProductLive: string = '';
  @Expose() stripeYearlyProductLive: string = '';
  @Expose() isStripeKeyLive: boolean = false;

  static fromJson(json: any): StripeModel {
    return plainToInstance(StripeModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: StripeModel): any {
    return instanceToPlain(order);
  }
}

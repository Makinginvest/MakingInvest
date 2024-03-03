import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';

export class PrivacyModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() data: string = '';

  static fromJson(json: any): PrivacyModel {
    return plainToInstance(PrivacyModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: PrivacyModel): any {
    return instanceToPlain(order);
  }
}

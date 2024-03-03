import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';

export class TermsModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() data: string = '';

  static fromJson(json: any): TermsModel {
    return plainToInstance(TermsModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: TermsModel): any {
    return instanceToPlain(order);
  }
}

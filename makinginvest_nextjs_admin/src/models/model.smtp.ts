import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';

export class SMTPModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() password: string = '';
  @Expose() host: string = '';
  @Expose() port: string = '';
  @Expose() email: string = '';

  static fromJson(json: any): SMTPModel {
    return plainToInstance(SMTPModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: SMTPModel): any {
    return instanceToPlain(order);
  }
}

import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';
import { convertToDate } from '../utils/convert_to_date';

export class NotificationModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() title: string = '';
  @Expose() body: string = '';
  @Expose() @Type(() => Date) timestampCreated?: Date | null = null;

  static fromJson(json: any): NotificationModel {
    json = convertObjectDate(json);
    return plainToInstance(NotificationModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: NotificationModel): any {
    return instanceToPlain(order);
  }
}

function convertObjectDate(json: any) {
  json.timestampCreated = convertToDate(json.timestampCreated);
  json.timestampUpdated = convertToDate(json.timestampUpdated);

  return json;
}

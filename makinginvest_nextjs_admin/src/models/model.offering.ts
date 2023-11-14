import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';
import { convertToDate } from '../utils/convert_to_date';

export class OfferingModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() title: string = '';
  @Expose() body: string = '';
  @Expose() link: string = '';
  @Expose() image: string = '';
  @Expose() @Type(() => Date) timestampCreated?: Date | null = null;
  @Expose() @Type(() => Date) timestampUpdated?: Date | null = null;

  static fromJson(json: any): OfferingModel {
    json = convertObjectDate(json);
    return plainToInstance(OfferingModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: OfferingModel): any {
    return instanceToPlain(order);
  }
}

function convertObjectDate(json: any) {
  json.timestampCreated = convertToDate(json.timestampCreated);
  json.timestampUpdated = convertToDate(json.timestampUpdated);

  return json;
}

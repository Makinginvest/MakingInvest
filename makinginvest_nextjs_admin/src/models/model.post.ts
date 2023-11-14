import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';
import { convertToDate } from '../utils/convert_to_date';

export class PostModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() slug: string = '';
  @Expose() title: string = '';
  @Expose() body: string = '';
  @Expose() status: string = '';
  @Expose() image: string = '';
  @Expose() isFree: boolean = true;

  @Expose() @Type(() => Date) postDate?: Date | null = null;
  @Expose() @Type(() => Date) postTime?: Date | null = null;
  @Expose() @Type(() => Date) postDateTime?: Date | null = null;
  @Expose() @Type(() => Date) timestampCreated?: Date | null = null;
  @Expose() @Type(() => Date) timestampUpdated?: Date | null = null;

  static fromJson(json: any): PostModel {
    json = convertObjectDate(json);
    return plainToInstance(PostModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: PostModel): any {
    return instanceToPlain(order);
  }
}

function convertObjectDate(json: any) {
  json.timestampCreated = convertToDate(json.timestampCreated);
  json.timestampUpdated = convertToDate(json.timestampUpdated);
  json.postDate = convertToDate(json.postDate);
  json.postTime = convertToDate(json.postTime);
  json.postDateTime = convertToDate(json.postDateTime);

  return json;
}

import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';
import { convertToDate } from '../utils/convert_to_date';

export class VideoLessonModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() link: string = '';
  @Expose() title: string = '';
  @Expose() image: string = '';
  @Expose() status: string = '';
  @Expose() isFree: boolean = true;
  @Expose() @Type(() => Date) timestampCreated?: Date | null = null;
  @Expose() @Type(() => Date) timestampUpdated?: Date | null = null;

  static fromJson(json: any): VideoLessonModel {
    json = convertObjectDate(json);
    return plainToInstance(VideoLessonModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: VideoLessonModel): any {
    return instanceToPlain(order);
  }
}

function convertObjectDate(json: any) {
  json.timestampCreated = convertToDate(json.timestampCreated);
  json.timestampUpdated = convertToDate(json.timestampUpdated);

  return json;
}

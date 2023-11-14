import { Expose, instanceToPlain, plainToInstance } from 'class-transformer';
import 'reflect-metadata';

export class DashboardModel {
  @Expose({ name: 'id' }) id: string = '';

  @Expose() totalUsers: number = 0;
  @Expose() totalVideoLessons: number = 0;
  @Expose() totalAnnouncements: number = 0;
  @Expose() totalSignalsForexOpen: number = 0;
  @Expose() totalSignalsForexClosed: number = 0;
  @Expose() totalSignalsStocksOpen: number = 0;
  @Expose() totalSignalsStocksClosed: number = 0;
  @Expose() totalSignalsCryptoOpen: number = 0;
  @Expose() totalSignalsCryptoClosed: number = 0;
  @Expose() totalPosts: number = 0;

  static fromJson(json: any): DashboardModel {
    return plainToInstance(DashboardModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: DashboardModel): any {
    return instanceToPlain(order);
  }
}

function convertObjectDate(json: any) {
  return json;
}

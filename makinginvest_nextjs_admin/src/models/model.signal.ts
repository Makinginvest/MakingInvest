import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';
import { convertToDate } from '../utils/convert_to_date';

export class SignalModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() isAuto: boolean = false;
  @Expose() symbol: string = '';
  @Expose() entryPrice: number = 0;
  @Expose() entryType: string = '';
  @Expose() isFree: boolean = false;
  @Expose() analysisImage: string = '';
  @Expose() analysisText: string = '';
  @Expose() market: string = '';
  @Expose() comment: string = '';
  @Expose() @Type(() => Date) entryDateTime?: Date | null = null;
  //
  @Expose() stopLoss: number = 0;
  @Expose() stopLossPct: number = 0;
  @Expose() stopLossPips: number = 0;
  @Expose() @Type(() => Date) stopLossDateTime?: Date | null = null;
  @Expose() stopLossResult: string = '';
  @Expose() stopLossComment: string = '';
  @Expose() stopLossHit: boolean = false;
  //
  @Expose() takeProfit1: number = 0;
  @Expose() takeProfit1Pct: number = 0;
  @Expose() takeProfit1Pips: number = 0;
  @Expose() @Type(() => Date) takeProfit1DateTime?: Date | null = null;
  @Expose() takeProfit1Result: string = '';
  @Expose() takeProfit1Comment: string = '';
  @Expose() takeProfit1Hit: boolean = false;
  //
  @Expose() takeProfit2: number = 0;
  @Expose() takeProfit2Pct: number = 0;
  @Expose() takeProfit2Pips: number = 0;
  @Expose() @Type(() => Date) takeProfit2DateTime?: Date | null = null;
  @Expose() takeProfit2Result: string = '';
  @Expose() takeProfit2Comment: string = '';
  @Expose() takeProfit2Hit: boolean = false;
  //
  @Expose() takeProfit3: number = 0;
  @Expose() takeProfit3Pct: number = 0;
  @Expose() takeProfit3Pips: number = 0;
  @Expose() @Type(() => Date) takeProfit3DateTime?: Date | null = null;
  @Expose() takeProfit3Result: string = '';
  @Expose() takeProfit3Comment: string = '';
  @Expose() takeProfit3Hit: boolean = false;
  //
  @Expose() isClosed: boolean = false;
  @Expose() isClosedManual: boolean = false;
  @Expose() isClosedAuto: boolean = false;
  @Expose() @Type(() => Date) timestampClosed?: Date | null = null;

  @Expose() @Type(() => Date) timestampCreated?: Date | null = null;
  @Expose() @Type(() => Date) timestampUpdated?: Date | null = null;
  @Expose() @Type(() => Date) timestampLastAutoCheck?: Date | null = null;

  static fromJson(json: any): SignalModel {
    json = convertObjectDate(json);
    return plainToInstance(SignalModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: SignalModel): any {
    return instanceToPlain(order);
  }

  static toJsonRealtimeDB(order: SignalModel): any {
    return convertKeysValuesInObjectToTimestamps(instanceToPlain(order));
  }

  get getSignalOpenStatus(): string {
    if (this.takeProfit3Hit) return 'Take Profit 3';
    if (this.takeProfit2Hit) return 'Take Profit 2';
    if (this.takeProfit1Hit) return 'Take Profit 1';
    if (this.stopLossHit) return 'Stop Loss hit';
    return 'In progress';
  }

  get getEntryDate(): Date | null {
    return getDateDay(this.entryDateTime);
  }

  get getEntryTime(): Date | null {
    return getDateTime(this.entryDateTime);
  }

  get getStopLossDate(): Date | null {
    return getDateDay(this.stopLossDateTime);
  }

  get getStopLossTime(): Date | null {
    return getDateTime(this.stopLossDateTime);
  }

  get getTakeProfit1Date(): Date | null {
    return getDateDay(this.takeProfit1DateTime);
  }

  get getTakeProfit1Time(): Date | null {
    return getDateTime(this.takeProfit1DateTime);
  }

  get getTakeProfit2Date(): Date | null {
    return getDateDay(this.takeProfit2DateTime);
  }

  get getTakeProfit2Time(): Date | null {
    return getDateTime(this.takeProfit2DateTime);
  }

  get getTakeProfit3Date(): Date | null {
    return getDateDay(this.takeProfit3DateTime);
  }

  get getTakeProfit3Time(): Date | null {
    return getDateTime(this.takeProfit3DateTime);
  }
}

function getDateDay(date: Date | null | undefined): Date | null {
  if (!date) return null;
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function getDateTime(date: Date | null | undefined): Date | null {
  if (!date) return null;
  return new Date(0, 0, 0, date.getHours(), date.getMinutes(), date.getSeconds());
}

function convertKeysValuesInObjectToTimestamps(obj: any) {
  Object.keys(obj).forEach((key) => {
    if (obj[key] instanceof Date) {
      obj[key] = obj[key].toJSON();
    }
  });
  return obj;
}

function convertObjectDate(json: any) {
  json.timestampCreated = convertToDate(json.timestampCreated);
  json.timestampUpdated = convertToDate(json.timestampUpdated);
  json.entryDate = convertToDate(json.entryDate);
  json.entryTime = convertToDate(json.entryTime);
  json.entryDateTime = convertToDate(json.entryDateTime);
  json.stopLossDate = convertToDate(json.stopLossDate);
  json.stopLossTime = convertToDate(json.stopLossTime);
  json.stopLossDateTime = convertToDate(json.stopLossDateTime);
  json.takeProfit1Date = convertToDate(json.takeProfit1Date);
  json.takeProfit1Tim = convertToDate(json.takeProfit1Time);
  json.takeProfit1DateTime = convertToDate(json.takeProfit1DateTime);
  json.takeProfit2Date = convertToDate(json.takeProfit2Date);
  json.takeProfit2Time = convertToDate(json.takeProfit2Time);
  json.takeProfit2DateTime = convertToDate(json.takeProfit2DateTime);
  json.takeProfit3Date = convertToDate(json.takeProfit3Date);
  json.takeProfit3Time = convertToDate(json.takeProfit3Time);
  json.takeProfit3DateTime = convertToDate(json.takeProfit3DateTime);
  json.timestampClosed = convertToDate(json.timestampClosed);
  json.timestampLastAutoCheck = convertToDate(json.timestampLastAutoCheck);

  return json;
}

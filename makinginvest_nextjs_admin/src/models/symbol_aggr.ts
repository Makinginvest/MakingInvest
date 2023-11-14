import { Expose, instanceToPlain, plainToInstance, Type } from 'class-transformer';
import 'reflect-metadata';

export class SymbolsAggr {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() title: string = '';
  @Expose() body: string = '';
  @Expose() forex: Symbol[] = [];
  @Expose() crypto: Symbol[] = [];
  @Expose() stocks: Symbol[] = [];

  static fromJson(json: any): SymbolsAggr {
    json = convertObjectDate(json);
    return plainToInstance(SymbolsAggr, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: SymbolsAggr): any {
    return instanceToPlain(order);
  }
}

function convertObjectDate(json: any) {
  return json;
}

export class Symbol {
  @Expose() symbol: string = '';

  static fromJson(json: any): Symbol {
    return plainToInstance(Symbol, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: Symbol): any {
    return instanceToPlain(order);
  }
}

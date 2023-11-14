import { Expose, instanceToPlain, plainToInstance } from 'class-transformer';
import 'reflect-metadata';

export class AppControlsPublicModel {
  @Expose({ name: 'id' }) id: string = '';
  @Expose() name: string = 'MakingInvest';
  @Expose() adminUrl: string = '';
  @Expose() frontendUrl: string = '';
  @Expose() apiUrl: string = '';
  @Expose() apiWebSocketUrl: string = '';
  @Expose() logoImage: string = '';
  @Expose() isEnabledForexSignals: boolean = true;
  @Expose() isEnabledCryptoSignals: boolean = true;
  @Expose() isEnabledStocksSignals: boolean = true;
  @Expose() isEnabledForexNews: boolean = true;
  @Expose() isEnabledCryptoNews: boolean = true;
  @Expose() isEnabledStocksNews: boolean = true;
  @Expose() sortOrderCryptoSignals: number = 1;
  @Expose() sortOrderForexSignals: number = 2;
  @Expose() sortOrderStocksSignals: number = 3;
  @Expose() headingNameCrypto: string = 'Crypto';
  @Expose() headingNameForex: string = 'Forex';
  @Expose() headingNameStocks: string = 'Stocks';
  @Expose() apiHasAccess: boolean = false;

  @Expose() apiInfo: string = '';

  @Expose() linkGooglePlay: string = '';
  @Expose() linkAppStore: string = '';
  @Expose() linkFacebook: string = '';
  @Expose() linkInstagram: string = '';
  @Expose() linkTwitter: string = '';
  @Expose() linkYoutube: string = '';
  @Expose() linkTelegram: string = '';
  @Expose() linkWhatsapp: string = '';
  @Expose() linkSupport: string = '';
  @Expose() linkTerms: string = '';
  @Expose() linkPivacy: string = '';

  @Expose() apiEnableNewsCrypto: boolean = true;
  @Expose() apiEnableNewsForex: boolean = true;
  @Expose() apiEnableNewsStocks: boolean = true;

  static fromJson(json: any): AppControlsPublicModel {
    return plainToInstance(AppControlsPublicModel, json, { exposeDefaultValues: true, excludeExtraneousValues: true });
  }

  static toJson(order: AppControlsPublicModel): any {
    return instanceToPlain(order);
  }

  static toJsonLinks(order: AppControlsPublicModel): any {
    const json = instanceToPlain(order);

    return {
      linkGooglePlay: json.linkGooglePlay,
      linkAppStore: json.linkAppStore,
      linkFacebook: json.linkFacebook,
      linkInstagram: json.linkInstagram,
      linkTwitter: json.linkTwitter,
      linkYoutube: json.linkYoutube,
      linkTelegram: json.linkTelegram,
      linkWhatsapp: json.linkWhatsapp,
      linkSupport: json.linkSupport,
      linkTerms: json.linkTerms,
      linkPivacy: json.linkPivacy
    };
  }
}

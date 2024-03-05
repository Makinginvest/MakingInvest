import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    """User Model."""

    id: Optional[str] = Field(None)
    firebaseUserId: Optional[str] = Field("")
    email: Optional[str] = Field("")
    favoriteSignals: Optional[list] = Field([])
    devTokens: Optional[list] = Field([])
    isAnonymous: Optional[bool] = Field(False)
    #
    isNotificationsEnabledGeneral: Optional[bool] = Field(True)
    isNotificationsEnabledCrypto: Optional[bool] = Field(True)
    isNotificationsEnabledForex: Optional[bool] = Field(True)
    isNotificationsEnabledStocks: Optional[bool] = Field(True)
    isNotificationsEnabledCommodities: Optional[bool] = Field(True)
    #
    isNotificationsEnabledCryptoRisky: Optional[bool] = Field(True)
    isNotificationsEnabledForexRisky: Optional[bool] = Field(True)
    isNotificationsEnabledStocksRisky: Optional[bool] = Field(True)

    createdDateTime: Optional[dt.datetime] = Field(None)
    lastLoginDateTime: Optional[dt.datetime] = Field(None)
    #
    subRevenuecatIsActive: Optional[bool] = Field(False)
    subRevenuecatWillRenew: Optional[bool] = Field(False)
    subRevenuecatPeriodType: Optional[str] = Field("")
    subRevenuecatProductIdentifier: Optional[str] = Field("")
    subRevenuecatIsSandbox: Optional[bool] = Field(False)
    subRevenuecatOriginalPurchaseDateTime: Optional[dt.datetime] = Field(None)
    subRevenuecatLatestPurchaseDateTime: Optional[dt.datetime] = Field(None)
    subRevenuecatExpirationDateTime: Optional[dt.datetime] = Field(None)
    subRevenuecatUnsubscribeDetectedDateTime: Optional[dt.datetime] = Field(None)
    subRevenuecatBillingIssueDetectedDateTime: Optional[dt.datetime] = Field(None)
    subIsLifetime: Optional[bool] = Field(False)
    subIsLifetimeExpirationDateTime: Optional[dt.datetime] = Field(None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = "ignore"
        orm_mode = True
        json_encoders = {dt.datetime: lambda dt: dt.isoformat()}

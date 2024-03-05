import datetime as dt
from typing import Optional
import pandas as pd
from pydantic import BaseModel, Field


class SignalModel(BaseModel):
    """Signal Model."""

    analysisImage: Optional[str] = Field("")
    analysisText: Optional[str] = Field("")
    comment: Optional[str] = Field("")
    entryAllowNewSignalDateTimeEst: Optional[dt.datetime] = Field(None)
    entryAllowNewSignalDateTimeUtc: Optional[dt.datetime] = Field(None)
    entryDateTimeEst: Optional[dt.datetime] = Field(None)
    entryDateTimeUtc: Optional[dt.datetime] = Field(None)
    entryPrice: Optional[float] = Field(0.0)
    entryType: Optional[str] = Field("")
    entryResult: Optional[str] = Field("")
    entryProfitLevel: Optional[int] = Field(0)
    entryProfitPct: Optional[float] = Field(0.0)
    entryProfitPips: Optional[float] = Field(0.0)
    highestPct: Optional[float] = Field(0.0)
    highestPips: Optional[float] = Field(0.0)
    highestPctPipsDateTimeUtc: Optional[dt.datetime] = Field(None)
    highestPctPipsDateTimeEst: Optional[dt.datetime] = Field(None)
    id: Optional[str] = Field(None)
    isAlgo: Optional[bool] = Field(False)
    isFree: Optional[bool] = Field(False)
    isNew: Optional[bool] = Field(False)
    lastCheckDateTimeUtc: Optional[dt.datetime] = Field(None)
    lastCheckDateTimeEst: Optional[dt.datetime] = Field(None)
    #
    market: Optional[str] = Field("")
    signalName: Optional[str] = Field("")
    symbol: Optional[str] = Field("")
    timeframe: Optional[str] = Field("")
    #
    stopLoss: Optional[float] = Field(0.0)
    stopLossDateTimeEst: Optional[dt.datetime] = Field(None)
    stopLossDateTimeUtc: Optional[dt.datetime] = Field(None)
    stopLossHit: Optional[bool] = Field(False)
    stopLossPct: Optional[float] = Field(0.0)
    stopLossPips: Optional[float] = Field(0.0)
    #
    stopLossRevised: Optional[float] = Field(None)
    stopLossRevisedDateTimeEst: Optional[dt.datetime] = Field(None)
    stopLossRevisedDateTimeUtc: Optional[dt.datetime] = Field(None)
    stopLossRevisedHit: Optional[bool] = Field(None)
    stopLossRevisedPct: Optional[float] = Field(None)
    stopLossRevisedPips: Optional[float] = Field(None)
    stopLossRevisedTp1: Optional[bool] = Field(False)
    stopLossRevisedTp2: Optional[bool] = Field(False)
    stopLossRevisedTp3: Optional[bool] = Field(False)
    #
    takeProfit1: Optional[float] = Field(0.0)
    takeProfit1DateTimeEst: Optional[dt.datetime] = Field(None)
    takeProfit1DateTimeUtc: Optional[dt.datetime] = Field(None)
    takeProfit1Hit: Optional[bool] = Field(False)
    takeProfit1Pct: Optional[float] = Field(0.0)
    takeProfit1Pips: Optional[float] = Field(0.0)
    takeProfit1Result: Optional[str] = Field("")
    #
    takeProfit2: Optional[float] = Field(0.0)
    takeProfit2DateTimeEst: Optional[dt.datetime] = Field(None)
    takeProfit2DateTimeUtc: Optional[dt.datetime] = Field(None)
    takeProfit2Hit: Optional[bool] = Field(False)
    takeProfit2Pct: Optional[float] = Field(0.0)
    takeProfit2Pips: Optional[float] = Field(0.0)
    takeProfit2Result: Optional[str] = Field("")
    #
    takeProfit3: Optional[float] = Field(0.0)
    takeProfit3DateTimeEst: Optional[dt.datetime] = Field(None)
    takeProfit3DateTimeUtc: Optional[dt.datetime] = Field(None)
    takeProfit3Hit: Optional[bool] = Field(False)
    takeProfit3Pct: Optional[float] = Field(0.0)
    takeProfit3Pips: Optional[float] = Field(0.0)
    takeProfit3Result: Optional[str] = Field("")
    #
    takeProfit4: Optional[float] = Field(0.0)
    takeProfit4DateTimeEst: Optional[dt.datetime] = Field(None)
    takeProfit4DateTimeUtc: Optional[dt.datetime] = Field(None)
    takeProfit4Hit: Optional[bool] = Field(False)
    takeProfit4Pct: Optional[float] = Field(0.0)
    takeProfit4Pips: Optional[float] = Field(0.0)
    takeProfit4Result: Optional[str] = Field("")
    #
    isClosed: Optional[bool] = Field(False)
    isClosedManual: Optional[bool] = Field(False)
    isClosedAuto: Optional[bool] = Field(False)
    closedDateTimeUtc: Optional[dt.datetime] = Field(None)
    closedDateTimeEst: Optional[dt.datetime] = Field(None)
    #
    hasFutures: Optional[bool] = Field(False)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = "ignore"
        orm_mode = True
        json_encoders = {dt.datetime: lambda dt: dt.isoformat()}


# -------------------------  REQUIRED DF COLUMNS ------------------------- #
get_columns_signals = [
    "symbol",
    "entryAllowNewSignalDateTimeEst",
    "entryAllowNewSignalDateTimeUtc",
    "entryDateTimeUtc",
    "entryDateTimeEst",
    "entryPrice",
    "entryType",
    "entryResult",
    "entryProfitLevel",
    "entryProfitPct",
    "entryProfitPips",
    "isAlgo",
    "timeframe",
    "isFree",
    "market",
    "highestPct",
    "highestPips",
    "highestPctPipsDateTimeUtc",
    "highestPctPipsDateTimeEst",
    "signalName",
    "analysisImage",
    "analysisText",
    "comment",
    "lastCheckDateTimeUtc",
    "lastCheckDateTimeEst",
    "isNew",
    #
    "stopLoss",
    "stopLossHit",
    "stopLossPct",
    "stopLossPips",
    "stopLossDateTimeEst",
    "stopLossDateTimeUtc",
    #
    "stopLossRevised",
    "stopLossRevisedHit",
    "stopLossRevisedPct",
    "stopLossRevisedPips",
    "stopLossRevisedDateTimeEst",
    "stopLossRevisedDateTimeUtc",
    "stopLossRevisedTp1",
    "stopLossRevisedTp2",
    "stopLossRevisedTp3",
    #
    "takeProfit1",
    "takeProfit1Hit",
    "takeProfit1Pct",
    "takeProfit1Pips",
    "takeProfit1Result",
    "takeProfit1DateTimeEst",
    "takeProfit1DateTimeUtc",
    #
    "takeProfit2",
    "takeProfit2Hit",
    "takeProfit2Pct",
    "takeProfit2Pips",
    "takeProfit2Result",
    "takeProfit2DateTimeEst",
    "takeProfit2DateTimeUtc",
    #
    "takeProfit3",
    "takeProfit3Hit",
    "takeProfit3Pct",
    "takeProfit3Pips",
    "takeProfit3Result",
    "takeProfit3DateTimeEst",
    "takeProfit3DateTimeUtc",
    #
    "takeProfit4",
    "takeProfit4Hit",
    "takeProfit4Pct",
    "takeProfit4Pips",
    "takeProfit4Result",
    "takeProfit4DateTimeEst",
    "takeProfit4DateTimeUtc",
    #
    "isClosed",
    "isClosedManual",
    "isClosedAuto",
    "closedDateTimeUtc",
    "closedDateTimeEst",
]


def add_required_columns(df: pd.DataFrame, market="crypto") -> pd.DataFrame:
    """Add required columns to df."""
    df["signalName"] = ""
    df["entryResult"] = "in progress"
    df["entryAllowNewSignalDateTimeEst"] = None
    df["entryAllowNewSignalDateTimeUtc"] = None
    df["takeProfit1DateTimeEst"] = None
    df["takeProfit1DateTimeUtc"] = None
    df["takeProfit1Hit"] = False
    df["takeProfit2DateTimeEst"] = None
    df["takeProfit2DateTimeUtc"] = None
    df["takeProfit2Hit"] = False
    df["takeProfit3DateTimeEst"] = None
    df["takeProfit3DateTimeUtc"] = None
    df["takeProfit3Hit"] = False
    df["takeProfit4DateTimeEst"] = None
    df["takeProfit4DateTimeUtc"] = None
    df["takeProfit4Hit"] = False
    df["stopLossDateTimeEst"] = None
    df["stopLossDateTimeUtc"] = None
    #
    df["stopLossRevised"] = None
    df["stopLossRevisedDateTimeEst"] = None
    df["stopLossRevisedDateTimeUtc"] = None
    df["stopLossRevisedHit"] = None
    df["stopLossRevisedPct"] = None
    df["stopLossRevisedPips"] = None
    df["stopLossRevisedTp1"] = False
    df["stopLossRevisedTp2"] = False
    df["stopLossRevisedTp3"] = False
    #
    df["stopLossHit"] = False
    df["analysisImage"] = ""
    df["analysisText"] = ""
    df["isAlgo"] = True
    df["entryProfitLevel"] = 0
    df["entryProfitPct"] = 0
    df["entryProfitPips"] = 0
    df["isFree"] = False
    df["market"] = market
    df["highestPct"] = None
    df["highestPips"] = None
    df["highestPctPipsDateTimeUtc"] = None
    df["highestPctPipsDateTimeEst"] = None
    df["lastCheckDateTimeUtc"] = None
    df["lastCheckDateTimeEst"] = None
    df["isClosed"] = False
    df["isClosedManual"] = False
    df["isClosedAuto"] = False
    df["closedDateTimeUtc"] = None
    df["closedDateTimeEst"] = None
    df["takeProfit1Result"] = ""
    df["takeProfit2Result"] = ""
    df["takeProfit3Result"] = ""
    df["takeProfit4Result"] = ""

    # check if takeProfit4 is missing and add it
    if "takeProfit4" not in df.columns:
        df["takeProfit4"] = None
    if "takeProfit4Pct" not in df.columns:
        df["takeProfit4Pct"] = None
    if "takeProfit4Pips" not in df.columns:
        df["takeProfit4Pips"] = None

    return df

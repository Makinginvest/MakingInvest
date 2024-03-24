import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class RatingModel(BaseModel):

    symbol: Optional[str] = Field("")
    rating: Optional[str] = Field("")
    ratingRecomendation: Optional[list] = Field([])

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = "ignore"
        orm_mode = True
        json_encoders = {dt.datetime: lambda dt: dt.isoformat()}

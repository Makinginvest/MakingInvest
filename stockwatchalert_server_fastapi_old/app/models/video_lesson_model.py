import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class VideoLessonModel(BaseModel):
    """Video Model."""

    id: Optional[str] = Field(None)
    isFree: Optional[bool] = Field(True)
    timestampCreated: Optional[dt.datetime] = Field(None)
    timestampUpdated: Optional[dt.datetime] = Field(None)
    title: Optional[str] = Field("")
    link: Optional[str] = Field("")
    image: Optional[str] = Field("")
    status: Optional[str] = Field("")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = "ignore"
        orm_mode = True
        json_encoders = {dt.datetime: lambda dt: dt.isoformat()}

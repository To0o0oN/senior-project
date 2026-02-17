from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MatchCreate(BaseModel):
    match_name: str
    match_date: datetime
    status: str = "active"
    created_by: str

class MatchResponse(MatchCreate):
    id: str = Field(alias="_id")
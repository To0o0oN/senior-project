from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ข้อมูลย่อย: รายละเอียดของเสียงแต่ละท่อนที่ AI ตัดมา
class EventDetail(BaseModel):
    duration_sec: float
    prediction: str
    confidence: float
    syllables: int
    is_counted: bool
    spectrogram_url: str
    plotgraph_url: str
    segment_audio_url: str

# ข้อมูลหลัก: สรุปคะแนนใน 1 ยก
class ScoreCreate(BaseModel):
    match_id: str
    user_id: str
    cage_number: str
    round_no: int
    audio_file_path: str
    total_score: int
    events: List[EventDetail]

class ScoreResponse(ScoreCreate):
    id: str = Field(alias="_id")
    timestamp: datetime
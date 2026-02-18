from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Any

# ข้อมูลย่อย: รายละเอียดของเสียงแต่ละท่อนที่ AI ตัดมา
class EventDetail(BaseModel):
    event_no: int
    duration_sec: float
    prediction: str
    confidence: float
    syllables: int
    is_counted: bool
    spectrogram_url: str
    plotgraph_url: str
    segment_audio_url: str

# โครงสร้างสำหรับการส่งข้อมูลกลับ (Response)
class ResultResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    match_name: str
    mode: str
    session_id: Optional[str]
    cage_number: str
    round_no: int
    total_score: int
    audio_path: str
    details: List[EventDetail]  # รายละเอียดท่อนร้องทั้งหมด
    final_status: str
    created_at: datetime

    class Config:
        populate_by_name = True # ช่วยให้แปลงจาก _id ของ MongoDB เป็น id ได้ง่ายขึ้น
from pydantic import BaseModel, Field
from datetime import datetime

# ข้อมูลตอนที่ส่งมาสมัครสมาชิก (ไม่คืนค่า Password กลับไปเด็ดขาด)
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"  # ค่าเริ่มต้นให้เป็นผู้ใช้งานทั่วไป (user)

# ข้อมูลตอนส่งกลับไปให้หน้าเว็บแสดงผล
class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    username: str
    role: str
    created_at: datetime
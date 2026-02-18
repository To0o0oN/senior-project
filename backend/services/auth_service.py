import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# ดึงตั้งค่าจาก .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

# ตั้งค่าการเข้ารหัสผ่านเป็นแบบ bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """เข้ารหัสผ่านก่อนเก็บลงฐานข้อมูล"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> str:
    """ตรวจสอบรหัสผ่านตอน Login"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """สร้าง JWT Token สำหรับยืนยันตัวตน"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS) # Token มีอายุ 24 ชม.
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
import os
import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv

from backend.db.database import get_database

load_dotenv()

# ดึงตั้งค่าจาก .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """ยามเฝ้าประตู: ตรวจสอบความถูกต้องของ Token และคืนค่าข้อมูล User"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="ไม่สามารถยืนยันตัวตนได้ หรือ Token หมดอายุ",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. ถอดรหัส Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 2. ไปเช็กในฐานข้อมูลว่า User นี้ยังมีตัวตนอยู่จริงไหม
    db = get_database()
    user = await db.users.find_one({"username": username})

    if user is None:
        raise credentials_exception
    
    # 3. ส่งข้อมูล User กลับไป (เพื่อให้ API รู้ว่าใครเป็นคนเรียกใช้)
    # แปลง _id เป็น string เพื่อความสะดวก
    user["_id"] = str(user["_id"])
    return user

def hash_password(password: str) -> str:
    """เข้ารหัสผ่านก่อนเก็บลงฐานข้อมูล"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password) -> str:
    """ตรวจสอบรหัสผ่านตอน Login"""
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    """สร้าง JWT Token สำหรับยืนยันตัวตน"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS) # Token มีอายุ 24 ชม.
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_admin(current_user: dict = Depends(get_current_user)):
    """ยามตรวจระดับหัวหน้า: เช็กว่า User ที่ Login อยู่เป็น Admin หรือไม่"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="สิทธิ์การเข้าถึงจำกัดเฉพาะผู้ดูแลระบบ (Admin) เท่านั้นครับ"
        )
    return current_user
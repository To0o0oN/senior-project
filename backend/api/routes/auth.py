from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from zoneinfo import ZoneInfo

from backend.db.database import get_database
from backend.schemas.user import UserCreate, UserResponse
from backend.services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """API สำหรับสมัครสมาชิก (User / Admin)"""
    db = get_database()
    
    # 1. เช็กว่า Username ซ้ำในฐานข้อมูลหรือไม่
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username นี้ถูกใช้งานแล้วครับ"
        )

    # 2. แปลงข้อมูลเป็น Dict และแฮชรหัสผ่าน
    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user.password)
    
    # เพิ่ม Timestamp ลงไป (ใช้ timezone-aware ตามมาตรฐานใหม่)
    bangkok_tz = ZoneInfo("Asia/Bangkok")
    user_dict["created_at"] = datetime.now(bangkok_tz)

    # 3. บันทึกลง MongoDB
    new_user = await db.users.insert_one(user_dict)
    
    # 4. ส่งข้อมูลกลับไปให้หน้าบ้าน (ดึง _id มาแปลงเป็น string ใส่ในฟิลด์ id)
    user_dict["id"] = str(new_user.inserted_id)
    user_dict["_id"] = str(new_user.inserted_id)

    return user_dict


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """API สำหรับเข้าสู่ระบบเพื่อรับ Token"""
    db = get_database()
    
    # 1. ค้นหา User จาก username ที่กรอกเข้ามา
    user = await db.users.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="ไม่พบผู้ใช้งานนี้ในระบบ"
        )

    # 2. ตรวจสอบรหัสผ่านว่าตรงกับที่แฮชไว้หรือไม่
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="รหัสผ่านไม่ถูกต้อง"
        )

    # 3. สร้าง JWT Token พร้อมฝัง Role เข้าไปใน Token ด้วย
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user["role"],
        "username": user["username"]
    }
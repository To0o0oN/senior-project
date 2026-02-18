from fastapi import APIRouter, Depends, HTTPException
from backend.db.database import get_database
from backend.services.auth_service import get_current_admin # ใช้ยามตรวจ Admin

router = APIRouter()

@router.get("/users")
async def list_users(admin: dict = Depends(get_current_admin)):
    """ดึงรายชื่อผู้ใช้ทุกคน (เฉพาะ Admin)"""
    db = get_database()
    users = await db.users.find({}, {"password": 0}).to_list(100) # ไม่ส่ง password กลับไป
    for u in users:
        u["_id"] = str(u["_id"])
    return users

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: dict = Depends(get_current_admin)):
    """ลบผู้ใช้งาน (เฉพาะ Admin)"""
    db = get_database()
    # ป้องกัน Admin ลบตัวเอง (Optional)
    if user_id == str(admin["_id"]):
        raise HTTPException(status_code=400, detail="ไม่สามารถลบบัญชีตัวเองได้")
    
    await db.users.delete_one({"_id": user_id})
    return {"message": "ลบผู้ใช้งานเรียบร้อยแล้ว"}
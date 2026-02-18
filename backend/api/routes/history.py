from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from backend.db.database import get_database
from backend.services.auth_service import get_current_user

router = APIRouter()

@router.get("/")
async def get_history(
    match_name: Optional[str] = Query(None),
    cage_number: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    query = {}

    # 🔒 ถ้าไม่ใช่ Admin ให้เห็นเฉพาะของตัวเอง
    if current_user["role"] != "admin":
        query["user_id"] = str(current_user["_id"])
    
    # 🔍 ตัวกรองค้นหา (ถ้ามีการส่งมา)
    if match_name:
        query["match_name"] = {"$regex": match_name, "$options": "i"} # ค้นหาแบบไม่สนตัวพิมพ์เล็กใหญ่
    if cage_number:
        query["cage_number"] = cage_number

    # ดึงข้อมูล เรียงจากใหม่ไปเก่า
    results = await db.results.find(query).sort("created_at", -1).to_list(100)
    
    for r in results:
        r["_id"] = str(r["_id"])
        
    return results

@router.get("/session/{session_id}")
async def get_session_detail(session_id: str, current_user: dict = Depends(get_current_user)):
    """ดึงข้อมูล 4 ยกของนกตัวเดียวมาแสดงในหน้าสรุปผล"""
    db = get_database()
    rounds = await db.results.find({"session_id": session_id}).sort("round_no", 1).to_list(length=4)
    
    if not rounds:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลเซสชันนี้")
        
    # เช็กสิทธิ์ (ถ้าไม่ใช่เจ้าของ และไม่ใช่ Admin ห้ามดู)
    if rounds[0]["user_id"] != str(current_user["_id"]) and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="ไม่มีสิทธิ์ดูข้อมูลนี้")

    for r in rounds:
        r["_id"] = str(r["_id"])

    return {
        "summary": {
            "match_name": rounds[0]["match_name"],
            "cage_number": rounds[0]["cage_number"],
            "total_score": sum(r["total_score"] for r in rounds),
            "final_status": rounds[-1]["final_status"] # สถานะจากยกสุดท้าย
        },
        "rounds": rounds
    }
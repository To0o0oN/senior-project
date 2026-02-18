import os
import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from datetime import datetime
from zoneinfo import ZoneInfo

from backend.services.ml_service import analyze_audio_session
from backend.services.auth_service import get_current_user
from backend.db.database import get_database

router = APIRouter()

@router.post("/predict")
async def predict_audio(
    match_name: str = Form(...),
    cage_number: str = Form(...),
    round_no: int = Form(...),
    mode: str = Form("competition"),
    session_id: str = Form(None),
    file: UploadFile = File(...), 
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    bangkok_tz = ZoneInfo("Asia/Bangkok")

    print(f"👤 ผู้ใช้งาน {current_user['username']} กำลังส่งเสียงนกมาตรวจ...")

    # 1. ตรวจสอบนามสกุลไฟล์
    if not (file.filename.endswith('.wav') or file.filename.endswith('.mp3')):
        raise HTTPException(status_code=400, detail="กรุณาอัปโหลดไฟล์ .wav/.mp3 เท่านั้น")

    # 2. สร้างชื่อไฟล์ใหม่ให้ไม่ซ้ำกัน (ใช้ Timestamp + ชื่อเดิม)
    # วิธีนี้จะทำให้ไฟล์ในโฟลเดอร์เรียงลำดับตามเวลาที่อัปโหลดด้วย
    timestamp = int(time.time())
    unique_filename = f"{timestamp}_{file.filename}"
    save_path = os.path.join("uploads", "audio", unique_filename)
    
    try:
        # 3. บันทึกไฟล์เสียงต้นฉบับ (13 วินาที) ลงใน uploads/audio/ แบบถาวร
        with open(save_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 4. ส่ง Path ของไฟล์ที่บันทึกแล้วไปให้ ML Service วิเคราะห์
        analysis_result = analyze_audio_session(save_path)
        
        final_status = "n/a" # ค่าเริ่มต้นสำหรับโหมด Test

        if mode == "competition":
            if round_no < 4:
                final_status = "pending" # รอให้ครบ 4 ยก
            elif round_no == 4 and session_id:
                # คำนวณคะแนนรวมจากยกที่ 1-3 ที่อยู่ใน session_id เดียวกัน
                previous_rounds = await db.results.find({
                    "session_id": session_id,
                    "round_no": {"$lt": 4}
                }).to_list(length=4)

                prev_score = sum(r["total_score"] for r in previous_rounds)
                current_total = prev_score + analysis_result["total_score"]

                # กติกาจำลอง: ถ้าคะแนนรวม 4 ยก >= 8 คะแนน ถือว่าผ่าน (ปรับเปลี่ยนได้ตามต้องการ)
                final_status = "pass" if current_total >= 8 else "fail"
            
        result_doc = {
            "user_id": str(current_user["_id"]),
            "match_name": match_name,
            "mode": mode,
            "session_id": session_id,
            "cage_number": cage_number,
            "round_no": round_no,
            "total_score": analysis_result["total_score"],
            "audio_path": f"/uploads/audio/{unique_filename}",
            "details": analysis_result["events"], # ข้อมูลละเอียดแต่ละท่อนร้อง
            "final_status": final_status,
            "created_at": datetime.now(bangkok_tz)
        }

        new_result = await db.results.insert_one(result_doc)

        # 5. ส่งผลลัพธ์กลับ พร้อม URL ของไฟล์ต้นฉบับ
        # เพื่อให้นำไปบันทึกลง MongoDB ในฟิลด์ audio_file_path ได้ทันที
        return {
            "id": str(new_result.inserted_id),
            "status": "success",
            "final_status": final_status,
            "filename": unique_filename,
            "audio_full_url": f"/uploads/audio/{unique_filename}", 
            "summary": {
                "total_score": analysis_result["total_score"],
                "total_events": analysis_result["total_events"]
            },
            "events": analysis_result["events"]
        } 

    except Exception as e:
        # กรณีเกิด Error ระหว่างประมวลผล
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการประมวลผล: {str(e)}")
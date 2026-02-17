import os
import time
from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.ml_service import analyze_audio_session

router = APIRouter()

@router.post("/predict")
async def predict_audio(file: UploadFile = File(...)):
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
        
        # 5. ส่งผลลัพธ์กลับ พร้อม URL ของไฟล์ต้นฉบับ
        # เพื่อให้นำไปบันทึกลง MongoDB ในฟิลด์ audio_file_path ได้ทันที
        return {
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
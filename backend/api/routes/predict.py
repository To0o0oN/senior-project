import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.ml_service import analyze_audio_session

router = APIRouter()

@router.post("/predict")
async def predict_audio(file: UploadFile = File(...)):
    # 1. ตรวจสอบนามสกุลไฟล์
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="กรุณาอัปโหลดไฟล์ .wav เท่านั้น")
    
    # 2. บันทึกไฟล์เสียงต้นฉบับลงในโฟลเดอร์ uploads/audio/ เพื่อให้ ML Service นำไปประมวลผล
    # เราตั้งชื่อไฟล์ชั่วคราวโดยใช้ชื่อเดิมของมัน
    temp_audio_path = os.path.join("uploads", "audio", file.filename)
    
    try:
        with open(temp_audio_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 3. เรียกใช้ "สมองกลใหม่" (หั่นท่อน + AI คัดกรอง + นับพยางค์ + Noise Reduction)
        analysis_result = analyze_audio_session(temp_audio_path)
        
        # 4. ส่งผลลัพธ์กลับในรูปแบบที่ตรงกับ Schema และตารางในรายงาน
        return {
            "filename": file.filename,
            "summary": {
                "total_score": analysis_result["total_score"],
                "total_events": analysis_result["total_events"]
            },
            "events": analysis_result["events"]
        }

    except Exception as e:
        # กรณีเกิด Error ระหว่างประมวลผล
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดในการประมวลผล: {str(e)}")
    
    finally:
        # 5. ลบไฟล์ต้นฉบับที่อัปโหลดมาทิ้ง (เพื่อไม่ให้เปลืองพื้นที่) 
        # ส่วนไฟล์ที่ 'ตัดท่อนแล้ว' จะยังคงอยู่ในโฟลเดอร์ตามที่เขียนไว้ใน ml_service
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
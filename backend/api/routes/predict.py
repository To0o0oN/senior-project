import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.schemas.predict import PredictResponse
from backend.utils.audio import preprocess_audio
from backend.services.ml_service import predict_spectrogram

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict_audio(file: UploadFile = File(...)):
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="ระบบรองรับเฉพาะไฟล์ .wav เท่านั้นครับ")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name
        
    temp_image_path = temp_audio_path.replace('.wav', '.png')
    
    try:
        # 1. แปลงเสียงเป็นภาพ
        preprocess_audio(temp_audio_path, temp_image_path)
        
        # 2. ให้ AI ทำนาย
        result = predict_spectrogram(temp_image_path)
        
        # 3. ส่งผลลัพธ์กลับแบบ Pydantic Schema
        return PredictResponse(
            filename=file.filename,
            prediction=result["prediction"],
            confidence=result["confidence"]
        )
    finally:
        # ทำความสะอาดไฟล์ขยะ
        if os.path.exists(temp_audio_path): os.remove(temp_audio_path)
        if os.path.exists(temp_image_path): os.remove(temp_image_path)
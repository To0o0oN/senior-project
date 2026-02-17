import os
import time
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import soundfile as sf

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# --- การตั้งค่ามาตรฐาน (ต้องตรงกับตอนเตรียมข้อมูลเทรนโมเดล) ---
SR = 22050                  # Sample Rate
AI_INPUT_DURATION = 3.0     # ความยาวเสียงที่โมเดล AI รองรับ (วินาที)
CONFIDENCE_THRESHOLD = 0.6  # ค่าความมั่นใจขั้นต่ำที่ยอมรับว่าเป็นเสียงนกร้อง
TOP_DB = 25                 # ระดับความดังที่ใช้ตัดเสียง (ยิ่งน้อยยิ่งไวต่อเสียงเบา)
MIN_DURATION = 0.4          # ท่อนเสียงต้องยาวอย่างน้อย 0.5 วินาทีถึงจะนำมาคิด
MERGE_GAP = 0.25            # ถ้าเสียงห่างกันไม่เกิน 0.5 วิ ให้รวมเป็นท่อนเดียวกัน
PADDING_TIME = 0.15          # เผื่อขอบเสียงหน้า-หลังตอนตัด (วินาที)
MIN_SYLLABLES = 3           # กติกา: ต้องนับได้ 3 พยางค์ขึ้นไปถึงจะได้ 1 ดอก

# ตั้งค่าพาธที่เก็บไฟล์
UPLOAD_DIR = "uploads"
IMG_DIR = os.path.join(UPLOAD_DIR, "images")
AUDIO_DIR = os.path.join(UPLOAD_DIR, "audio")

# ตรวจสอบและสร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# --- โหลดโมเดล AI (CNN) ---
MODEL_PATH = "ml_pipeline/models/bird_song_model.keras"

print("⏳ กำลังโหลดโมเดล AI...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ โหลดโมเดลสำเร็จ พร้อมทำงาน!")
except Exception as e:
    print(f"❌ โหลดโมเดลไม่สำเร็จ: {e}")
    model = None

def merge_intervals(intervals, sr, gap_threshold):
    """ฟังก์ชันรวมท่อนเสียงที่อยู่ใกล้กันให้เป็นท่อนเดียว (เหมือนตอนเตรียมข้อมูลเทรน)"""
    if len(intervals) == 0: return []
    merged = []
    current_start, current_end = intervals[0]
    for i in range(1, len(intervals)):
        next_start, next_end = intervals[i]
        gap_duration = (next_start - current_end) / sr
        if gap_duration < gap_threshold:
            current_end = next_end
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    merged.append((current_start, current_end))
    return merged

def create_padded_spectrogram(y_segment, sr, save_path):
    """สร้าง Spectrogram ขนาด 128x130 (Grayscale) เพื่อส่งให้ AI ทายผล"""
    target_length = int(sr * AI_INPUT_DURATION)
    # ปรับความยาวให้พอดีกับที่ AI ต้องการ (Padding ด้วยความเงียบ)
    if len(y_segment) > target_length:
        y_segment = y_segment[:target_length]
    else:
        padding = target_length - len(y_segment)
        y_segment = np.pad(y_segment, (0, padding), mode='constant')

    S = librosa.feature.melspectrogram(y=y_segment, sr=sr, n_mels=128, fmax=8000)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # เซฟเป็นรูปภาพขาวดำ (Grayscale) ไม่เอาขอบและแกน
    fig = plt.figure(figsize=(1.30, 1.28), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    librosa.display.specshow(S_dB, sr=sr, cmap='gray', ax=ax)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close(fig)

def reduce_noise(y, sr):
    """ฟังก์ชันลดเสียงรบกวนเบื้องต้น (Simple Noise Gate)"""
    # ใช้การลบค่าเฉลี่ยของความดังที่ต่ำมากๆ ออกไป
    stft = librosa.stft(y)
    stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
    # ตัดเสียงที่ต่ำกว่า -30dB ออก (Noise Floor)
    stft_db[stft_db < -30] = -100 
    y_cleaned = librosa.istft(librosa.db_to_amplitude(stft_db) * np.exp(1j * np.angle(stft)))
    return y_cleaned

def count_syllables_and_plot(y_chunk, sr, save_path):
    """ฟังก์ชันนับคะแนน (นับพยางค์): คำนวณพลังงานเสียง (RMS) และหาจุดยอดคลื่น (Peaks)"""
    # 1. Normalization: ปรับความดังให้สูงสุดที่ 1.0 เสมอ
    if np.max(np.abs(y_chunk)) > 0:
        y_chunk = librosa.util.normalize(y_chunk)

    hop_length = 512
    # 2. คำนวณ RMS Energy
    rms = librosa.feature.rms(y=y_chunk, frame_length=2048, hop_length=hop_length)[0]
    rms_norm = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-6)

    # 3. Peak Detection (ปรับจูนระยะห่างระหว่างพยางค์)
    # นกปรอดร้องเร็วมาก ระยะห่างขั้นต่ำควรอยู่ที่ประมาณ 0.1 วินาที
    min_dist_frames = int((0.1 * sr) / hop_length)
    peaks, _ = find_peaks(rms_norm, height=0.10, distance=min_dist_frames)

    # วาดกราฟ RMS เพื่อโชว์บนแอป (ให้กรรมการดูว่านับตรงไหม)
    plt.figure(figsize=(8, 3))
    plt.plot(rms_norm, label='Normalized Energy', color='#2563eb')
    plt.plot(peaks, rms_norm[peaks], "rx", label='Syllable')
    plt.title(f'Syllable Counting (Total: {len(peaks)})')
    plt.legend()
    plt.savefig(save_path)
    plt.close()
    
    return len(peaks)

def analyze_audio_session(audio_path: str) -> dict:
    """ฟังก์ชันหลัก: รับไฟล์ 13 วินาที -> ตัดท่อน -> AI คัดกรอง -> นับพยางค์ -> สรุปคะแนน"""
    if model is None: raise RuntimeError("โมเดล AI ยังไม่ได้ถูกโหลด")

    # 1. โหลดและทำ Normalization ทั้งไฟล์
    y, sr = librosa.load(audio_path, sr=SR)
    y = librosa.util.normalize(y)

    # 2. ลดเสียงรบกวนเบื้องต้น
    y_clean = reduce_noise(y, sr)

    # 3. ตัดแบ่งท่อนเสียง (ใช้ MERGE_GAP ที่เล็กลง)
    raw_intervals = librosa.effects.split(y_clean, top_db=TOP_DB)

    # ฟังก์ชัน merge_intervals เดิม (แต่จะใช้ค่า MERGE_GAP 0.25)
    merged_intervals = merge_intervals(raw_intervals, sr, gap_threshold=MERGE_GAP)
    
    total_score = 0
    events_detail = []
    session_id = int(time.time()) # ใช้ timestamp เพื่อไม่ให้ชื่อไฟล์ซ้ำ

    file_prefix = os.path.splitext(os.path.basename(audio_path))[0]

    for i, (start_frame, end_frame) in enumerate(merged_intervals):
        # 1. คำนวณเวลาเริ่มต้นและสิ้นสุดเป็นวินาที
        start_sec = start_frame / sr
        end_sec = end_frame / sr
        duration = end_sec - start_sec

        if duration < MIN_DURATION: continue

        # 2. สร้างชื่อไฟล์โดยใช้ช่วงเวลา (ใช้ _ แทน . เพื่อความปลอดภัยของชื่อไฟล์)
        # ตัวอย่าง: bird01_02.50s-04.10s_spec.png
        time_range = f"{start_sec:.2f}s-{end_sec:.2f}s".replace(".", "_")
        base_name = f"{file_prefix}_{time_range}"

        spec_path = os.path.join(IMG_DIR, f"{base_name}_spec.png")
        plot_path = os.path.join(IMG_DIR, f"{base_name}_plot.png")
        audio_path_seg = os.path.join(AUDIO_DIR, f"{base_name}_seg.wav")

        # เผื่อขอบเสียงเล็กน้อย
        pad = int(PADDING_TIME * sr)
        y_chunk = y[max(0, start_frame-pad) : min(len(y), end_frame+pad)]
        
        # --- ขั้นตอนที่ 1: AI คัดกรอง (Classification) ---
        create_padded_spectrogram(y_chunk, sr, spec_path)
        img = tf.keras.utils.load_img(spec_path, target_size=(128, 130), color_mode='grayscale')
        img_array = tf.expand_dims(tf.keras.utils.img_to_array(img) / 255.0, 0)
        
        predictions = model.predict(img_array, verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))

        # --- ขั้นตอนที่ 2: ตัดสินคะแนน (Scoring Logic) ---
        syllables = 0
        is_counted = False
        
        # กติกา: ต้องเป็นเสียงนกร้อง (Class 1) และมีความมั่นใจสูง
        if class_idx == 1 and confidence >= CONFIDENCE_THRESHOLD:
            # เข้าสู่ฟังก์ชันนับพยางค์
            syllables = count_syllables_and_plot(y_chunk, sr, plot_path)
            
            # กติกา: ต้องมี 3 พยางค์ขึ้นไปถึงจะได้ 1 ดอก
            if syllables >= MIN_SYLLABLES:
                is_counted = True
                total_score += 1
        
        # เซฟไฟล์เสียงท่อนสั้นไว้ให้กรรมการฟังย้อนหลัง
        sf.write(audio_path_seg, y_chunk, sr)

        # เก็บข้อมูลลงรายการย่อย
        events_detail.append({
            "event_no": i + 1,
            "duration_sec": round(duration, 2),
            "prediction": "singing" if class_idx == 1 else "noise",
            "confidence": round(confidence, 4),
            "syllables": syllables,
            "is_counted": is_counted,
            "spectrogram_url": f"/uploads/images/{os.path.basename(spec_path)}",
            "plotgraph_url": f"/uploads/images/{os.path.basename(plot_path)}",
            "segment_audio_url": f"/uploads/audio/{os.path.basename(audio_path_seg)}"
        })

    # 3. สรุปผลลัพธ์ทั้งหมดของยกนี้
    return {
        "total_score": total_score,
        "total_events": len(events_detail),
        "events": events_detail
    }

def predict_spectrogram(image_path: str) -> dict:
    if model is None:
        raise RuntimeError("AI Model is not loaded.")
    
    img = load_img(image_path, target_size=(128, 130), color_mode='grayscale')
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))

    classes = ["0_noise", "1_singing"]

    return {
        "prediction": classes[class_idx],
        "confidence": f"{confidence * 100:.2f}%"
    }
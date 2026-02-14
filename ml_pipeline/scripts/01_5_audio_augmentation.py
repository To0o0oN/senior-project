import os
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm  # นำเข้า tqdm มาใช้งานแล้ว!

# --- 1. ตั้งค่าโฟลเดอร์ (Configuration) ---
INPUT_DIR = "ml_pipeline/data/03_labeled"
OUTPUT_DIR = "ml_pipeline/data/03_5_augmented"
TARGET_SR = 22050  # ตามรายงานกำหนดให้ใช้ 22,050 Hz

# --- 2. ฟังก์ชันแปลงร่างไฟล์เสียง (Augmentation Techniques) ---
def add_noise(data, noise_factor=0.005):
    """เทคนิคที่ 1: การเติมเสียงรบกวน (Noise Injection)"""
    noise = np.random.randn(len(data))
    return data + noise_factor * noise

def pitch_shift(data, sr, n_steps):
    """เทคนิคที่ 2: การปรับระดับเสียง (Pitch Shifting)"""
    return librosa.effects.pitch_shift(y=data, sr=sr, n_steps=n_steps)

def time_stretch(data, rate):
    """เทคนิคที่ 3: การปรับความเร็ว (Time Stretching)"""
    return librosa.effects.time_stretch(y=data, rate=rate)

def main():
    print("🚀 เริ่มกระบวนการเพิ่มข้อมูลเสียง (Data Augmentation)...")
    
    classes = ["0_noise", "1_singing"]
    
    for cls in classes:
        in_class_dir = os.path.join(INPUT_DIR, cls)
        out_class_dir = os.path.join(OUTPUT_DIR, cls)
        os.makedirs(out_class_dir, exist_ok=True)
        
        if not os.path.exists(in_class_dir):
            print(f"⚠️ ไม่พบโฟลเดอร์ {in_class_dir} ข้ามไปก่อน...")
            continue
            
        files = [f for f in os.listdir(in_class_dir) if f.endswith('.wav')]
        print(f"\nกำลังเตรียมข้อมูลคลาส {cls} ({len(files)} ไฟล์ต้นฉบับ)")
        
        # เพิ่ม tqdm ครอบตัวแปร files ตรงนี้เลยครับ
        for file in tqdm(files, desc=f"กำลังปั๊มไฟล์ {cls}", unit="file"):
            file_path = os.path.join(in_class_dir, file)
            filename = os.path.splitext(file)[0]
            
            # โหลดไฟล์เสียงต้นฉบับ ปรับเป็น 22,050 Hz
            y, sr = librosa.load(file_path, sr=TARGET_SR)
            
            # 1. เซฟไฟล์ต้นฉบับ (Original)
            sf.write(os.path.join(out_class_dir, f"{filename}_ori.wav"), y, sr)
            
            # 2. ทำ Pitch Shifting (ปรับเสียงแหลมขึ้น 2 สเตป)
            y_pitch = pitch_shift(y, sr, n_steps=2)
            sf.write(os.path.join(out_class_dir, f"{filename}_pitch.wav"), y_pitch, sr)
            
            # 3. ทำ Time Stretching (ปรับให้ร้องเร็วขึ้น 1.1 เท่า)
            y_stretch = time_stretch(y, rate=1.1)
            sf.write(os.path.join(out_class_dir, f"{filename}_stretch.wav"), y_stretch, sr)
            
            # 4. ทำ Noise Injection (แทรกเสียงซ่าเบาๆ)
            y_noise = add_noise(y)
            sf.write(os.path.join(out_class_dir, f"{filename}_noise.wav"), y_noise, sr)
            
    print(f"\n🎉 เสร็จสิ้น! ข้อมูลทั้งหมดถูกจัดเก็บไว้ที่: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
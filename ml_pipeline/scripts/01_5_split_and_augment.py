import os
import shutil
import librosa
import soundfile as sf
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# --- 1. ตั้งค่าโฟลเดอร์และพารามิเตอร์ ---
INPUT_DIR = "ml_pipeline/data/03_labeled"
OUTPUT_DIR = "ml_pipeline/data/dataset_audio"
TARGET_SR = 22050 # ตามรายงาน

def add_noise(data, noise_factor=0.005):
    noise = np.random.randn(len(data))
    return data + noise_factor * noise

def pitch_shift(data, sr, n_steps):
    return librosa.effects.pitch_shift(y=data, sr=sr, n_steps=n_steps)

def time_stretch(data, rate):
    return librosa.effects.time_stretch(y=data, rate=rate)

def process_and_save(file_path, save_dir, filename, is_train=False):
    """ฟังก์ชันโหลดเสียงและเซฟ (ทำ Augment เฉพาะตอน is_train=True)"""
    y, sr = librosa.load(file_path, sr=TARGET_SR)
    
    # เซฟไฟล์ต้นฉบับเสมอ ไม่ว่าจะอยู่ Train, Val หรือ Test
    sf.write(os.path.join(save_dir, f"{filename}_ori.wav"), y, sr)
    
    # ถ้าเป็นข้อมูล Train ให้ทำการปั๊มข้อมูลเพิ่ม (Augmentation)
    if is_train:
        sf.write(os.path.join(save_dir, f"{filename}_pitch.wav"), pitch_shift(y, sr, 2), sr)
        sf.write(os.path.join(save_dir, f"{filename}_stretch.wav"), time_stretch(y, 1.1), sr)
        sf.write(os.path.join(save_dir, f"{filename}_noise.wav"), add_noise(y), sr)

def main():
    print("🚀 เริ่มกระบวนการแบ่งกลุ่ม 80:10:10 และ Augment ข้อมูล...")
    classes = ["0_noise", "1_singing"]
    
    for cls in classes:
        in_class_dir = os.path.join(INPUT_DIR, cls)
        if not os.path.exists(in_class_dir):
            continue
            
        files = [f for f in os.listdir(in_class_dir) if f.endswith('.wav')]
        
        # 1. แบ่งข้อมูล Train (80%) และ Temp (20%)
        train_files, temp_files = train_test_split(files, test_size=0.2, random_state=42)
        # 2. แบ่ง Temp (20%) ออกเป็น Val (10%) และ Test (10%)
        val_files, test_files = train_test_split(temp_files, test_size=0.5, random_state=42)
        
        splits = {
            'train': (train_files, True),  # True = อนุญาตให้ทำ Augment
            'val': (val_files, False),     # False = ห้ามทำ Augment (ข้อสอบ)
            'test': (test_files, False)    # False = ห้ามทำ Augment (ข้อสอบ)
        }
        
        for split_name, (split_files, do_augment) in splits.items():
            out_dir = os.path.join(OUTPUT_DIR, split_name, cls)
            os.makedirs(out_dir, exist_ok=True)
            
            desc = f"ปั๊มข้อมูล {cls} ({split_name})" if do_augment else f"คัดลอก {cls} ({split_name})"
            for file in tqdm(split_files, desc=desc, unit="file"):
                file_path = os.path.join(in_class_dir, file)
                filename = os.path.splitext(file)[0]
                process_and_save(file_path, out_dir, filename, is_train=do_augment)
                
    print(f"\n🎉 แบ่งข้อมูลและ Augment เสร็จสมบูรณ์! เช็กไฟล์ได้ที่: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
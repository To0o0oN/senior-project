import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# --- 1. ตั้งค่าพื้นฐานให้ตรงกับรายงาน ---
# เปลี่ยนมาดึงไฟล์จากโฟลเดอร์ที่เราเพิ่งทำ Augmentation เสร็จ
INPUT_DIR = "ml_pipeline/data/03_5_augmented"
OUTPUT_DIR = "ml_pipeline/data/04_spectrograms"

# พารามิเตอร์ตามสเปกในรายงาน
SR = 22050               # อัตราการสุ่ม (Sampling Rate)
DURATION = 3.0           # ความยาว 3 วินาที (เพื่อให้ได้ความกว้างแกนเวลา ~130 time steps)
N_FFT = 2048             # ขนาดหน้าต่าง STFT
HOP_LENGTH = 512         # ระยะเลื่อนเฟรม
N_MELS = 128             # จำนวน Mel filter bands (ความสูงของภาพ = 128)

# ตั้งค่าขนาดภาพให้ได้ กว้าง 130 x สูง 128 pixels เป๊ะๆ
FIG_WIDTH = 1.30
FIG_HEIGHT = 1.28
DPI = 100

def create_mel_spectrogram(audio_path, save_path):
    # 1. โหลดไฟล์และปรับความยาวให้เป็น 3.0 วินาทีเป๊ะ (Center Padding)
    y, sr = librosa.load(audio_path, sr=SR)
    target_length = int(SR * DURATION)
    
    if len(y) > target_length:
        start = (len(y) - target_length) // 2
        y = y[start:start + target_length]
    else:
        pad_length = target_length - len(y)
        y = np.pad(y, (pad_length // 2, pad_length - pad_length // 2), mode='constant')

    # 2. แปลงคลื่นเสียงเป็น Mel-spectrogram (ตามสูตรในรายงาน)
    mel_signal = librosa.feature.melspectrogram(
        y=y, 
        sr=SR, 
        n_fft=N_FFT, 
        hop_length=HOP_LENGTH, 
        n_mels=N_MELS
    )
    
    # 3. แปลงพลังงานเสียงเป็นหน่วยเดซิเบล (Log-Amplitude)
    spectrogram = librosa.power_to_db(mel_signal, ref=np.max)

    # 4. วาดภาพและเซฟเป็นขาวดำ (Grayscale)
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]) # ให้รูปเต็มกรอบ 100%
    ax.axis('off') # ปิดตัวเลขแกน
    
    # ใช้ cmap='gray' เพื่อให้ได้ภาพขาวดำ 1 Channel สำหรับป้อนให้ AI
    librosa.display.specshow(spectrogram, sr=SR, hop_length=HOP_LENGTH, cmap='gray', ax=ax)
    
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=DPI, format='png')
    plt.close(fig)

def main():
    print("🖼️ กำลังแปลงไฟล์เสียงเป็นภาพ Mel-spectrogram ขาวดำ (128x130)...")
    
    classes = ["0_noise", "1_singing"]
    
    for cls in classes:
        in_class_dir = os.path.join(INPUT_DIR, cls)
        out_class_dir = os.path.join(OUTPUT_DIR, cls)
        os.makedirs(out_class_dir, exist_ok=True)
        
        if not os.path.exists(in_class_dir):
            print(f"⚠️ ไม่พบโฟลเดอร์ {in_class_dir}")
            continue
            
        files = [f for f in os.listdir(in_class_dir) if f.endswith('.wav')]
        print(f"กำลังสร้างภาพคลาส {cls}: {len(files)} ไฟล์...")

        for file in tqdm(files, desc=f"กำลังสร้างภาพคลาส {cls}"):
            audio_path = os.path.join(in_class_dir, file)
            save_path = os.path.join(out_class_dir, file.replace('.wav', '.png'))
            create_mel_spectrogram(audio_path, save_path) 
            
    print(f"\n✅ เสร็จสิ้น! รูปภาพทั้งหมดถูกบันทึกไว้ที่: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
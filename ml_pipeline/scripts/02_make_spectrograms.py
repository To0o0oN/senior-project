import os
import glob
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tqdm import tqdm

# --- ตั้งค่า Configuration ---
SR = 22050
DURATION = 3.0
TARGET_LENGTH = int(SR * DURATION)
IMAGE_SIZE = 2.24  # นิ้ว (เพื่อให้ได้ 224x224 pixels ที่ 100 DPI)

def create_spectrogram(audio_path, save_path):
    try:
        # 1. โหลดไฟล์เสียง
        y, sr = librosa.load(audio_path, sr=SR)
        
        # 2. ปรับความยาวให้เป็น 3.0 วินาทีเป๊ะ (Padding / Trimming)
        if len(y) > TARGET_LENGTH:
            # ถ้ายาวเกิน ให้ตัดเอาตรงกลาง (Center Crop)
            start = (len(y) - TARGET_LENGTH) // 2
            y = y[start:start + TARGET_LENGTH]
        else:
            # ถ้าสั้นไป ให้เติมความเงียบ (Zero Padding) แบ่งใส่หัว-ท้ายเท่าๆ กัน
            padding = TARGET_LENGTH - len(y)
            pad_left = padding // 2
            pad_right = padding - pad_left
            y = np.pad(y, (pad_left, pad_right), 'constant')
            
        # 3. สร้าง Mel-spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        # 4. วาดกราฟและเซฟเป็นรูปภาพ 224x224 (ไม่เอาแกน ตัวหนังสือ และขอบขาว)
        fig = plt.figure(figsize=(IMAGE_SIZE, IMAGE_SIZE), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        librosa.display.specshow(S_dB, sr=sr, fmax=8000, ax=ax)
        
        # เซฟภาพทับด้วยคุณภาพสูง
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        
        return True
    except Exception as e:
        print(f"❌ Error processing {audio_path}: {e}")
        return False

def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    audio_files = glob.glob(os.path.join(input_folder, "*.wav"))
    
    if not audio_files:
        print(f"⚠️ ไม่พบไฟล์ .wav ใน {input_folder}")
        return

    print(f"กำลังประมวลผลโฟลเดอร์: {os.path.basename(input_folder)} ({len(audio_files)} ไฟล์)")
    
    success_count = 0
    for audio_path in tqdm(audio_files):
        filename = os.path.splitext(os.path.basename(audio_path))[0]
        save_path = os.path.join(output_folder, f"{filename}.png")
        
        if create_spectrogram(audio_path, save_path):
            success_count += 1
            
    print(f"✅ แปลงสำเร็จ: {success_count}/{len(audio_files)} ภาพ\n")

def main():
    # โฟลเดอร์ต้นทาง (ที่คุณคัดแยกไว้)
    labeled_dir = "ml_pipeline/data/03_labeled"
    noise_dir_in = os.path.join(labeled_dir, "0_noise")
    singing_dir_in = os.path.join(labeled_dir, "1_singing")
    
    # โฟลเดอร์ปลายทาง (สำหรับเก็บรูปภาพ)
    spec_dir = "ml_pipeline/data/04_spectrograms"
    noise_dir_out = os.path.join(spec_dir, "0_noise")
    singing_dir_out = os.path.join(spec_dir, "1_singing")
    
    print("🚀 เริ่มกระบวนการแปลงเสียงเป็นรูปภาพ Spectrogram (ขนาด 224x224)...\n")
    
    process_folder(noise_dir_in, noise_dir_out)
    process_folder(singing_dir_in, singing_dir_out)
    
    print(f"🎉 เสร็จสิ้นกระบวนการทั้งหมด! เชิญดูรูปภาพได้ที่โฟลเดอร์: {spec_dir}")

if __name__ == "__main__":
    main()
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

INPUT_BASE_DIR = "ml_pipeline/data/dataset_audio"
OUTPUT_BASE_DIR = "ml_pipeline/data/dataset_spectrograms"

# พารามิเตอร์ตามสเปก
SR, DURATION = 22050, 3.0
N_FFT, HOP_LENGTH, N_MELS = 2048, 512, 128
FIG_WIDTH, FIG_HEIGHT, DPI = 1.30, 1.28, 100

def create_mel_spectrogram(audio_path, save_path):
    y, sr = librosa.load(audio_path, sr=SR)
    target_length = int(SR * DURATION)
    
    if len(y) > target_length:
        start = (len(y) - target_length) // 2
        y = y[start:start + target_length]
    else:
        pad_length = target_length - len(y)
        y = np.pad(y, (pad_length // 2, pad_length - pad_length // 2), mode='constant')

    mel_signal = librosa.feature.melspectrogram(y=y, sr=SR, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS)
    spectrogram = librosa.power_to_db(mel_signal, ref=np.max)

    fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    librosa.display.specshow(spectrogram, sr=SR, hop_length=HOP_LENGTH, cmap='gray', ax=ax)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=DPI, format='png')
    plt.close(fig)

def main():
    print("🖼️ กำลังแปลงไฟล์เสียงเป็นภาพ Mel-spectrogram ขาวดำ...")
    splits = ['train', 'val', 'test']
    classes = ["0_noise", "1_singing"]
    
    for split in splits:
        for cls in classes:
            in_dir = os.path.join(INPUT_BASE_DIR, split, cls)
            out_dir = os.path.join(OUTPUT_BASE_DIR, split, cls)
            
            if not os.path.exists(in_dir):
                continue
                
            os.makedirs(out_dir, exist_ok=True)
            files = [f for f in os.listdir(in_dir) if f.endswith('.wav')]
            
            for file in tqdm(files, desc=f"สร้างภาพ {split}/{cls}", unit="img"):
                audio_path = os.path.join(in_dir, file)
                save_path = os.path.join(out_dir, file.replace('.wav', '.png'))
                create_mel_spectrogram(audio_path, save_path)
                
    print(f"\n✅ เสร็จสิ้น! รูปภาพจัดกลุ่มพร้อมเทรนแล้วที่: {OUTPUT_BASE_DIR}")

if __name__ == "__main__":
    main()
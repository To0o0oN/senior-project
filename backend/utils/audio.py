import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# พารามิเตอร์ตามสเปก
SR, DURATION = 22050, 3.0
N_FFT, HOP_LENGTH, N_MELS = 2048, 512, 128
FIG_WIDTH, FIG_HEIGHT, DPI = 1.30, 1.28, 100

def preprocess_audio(audio_path: str, save_image_path: str):
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
    plt.savefig(save_image_path, bbox_inches='tight', pad_inches=0, dpi=DPI, format='png')
    plt.close(fig)
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

MODEL_PATH = "ml_pipeline/models/bird_song_model.keras"

print("⏳ กำลังโหลดโมเดล AI...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ โหลดโมเดลสำเร็จ พร้อมทำงาน!")
except Exception as e:
    print(f"❌ โหลดโมเดลไม่สำเร็จ: {e}")
    model = None

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
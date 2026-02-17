import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. ตั้งค่าพื้นฐาน ---
IMG_HEIGHT = 128
IMG_WIDTH = 130
BATCH_SIZE = 32

MODEL_PATH = "ml_pipeline/models/bird_song_model.keras"
TEST_DIR = "ml_pipeline/data/dataset_spectrograms/test"
CM_SAVE_PATH = "ml_pipeline/models/confusion_matrix.png" # ที่เซฟรูปกราฟ

def main():
    print("🔍 กำลังโหลดโมเดลและเตรียมชุดข้อมูลทดสอบ (Test Set)...")
    
    # โหลดโมเดลที่เทรนเสร็จแล้ว
    if not os.path.exists(MODEL_PATH):
        print(f"❌ ไม่พบไฟล์โมเดลที่ {MODEL_PATH} กรุณาเทรนโมเดลก่อนครับ")
        return
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # เตรียมข้อมูล Test (หาร 255 อย่างเดียว ห้ามทำ Augment และ ห้าม Shuffle)
    datagen = ImageDataGenerator(rescale=1./255)
    test_generator = datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        shuffle=False # สำคัญมาก! ต้อง False เพื่อให้เฉลยตรงกับลำดับไฟล์
    )
    
    # --- 2. ให้ AI ทำข้อสอบ ---
    print("\n🤖 กำลังให้ AI ทำนายผลจากภาพที่ทดสอบ...")
    predictions = model.predict(test_generator, verbose=1)
    
    # แปลงความน่าจะเป็นให้เป็นคลาสที่โมเดลเลือก (0 หรือ 1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_generator.classes # เฉลยที่ถูกต้อง
    class_names = list(test_generator.class_indices.keys()) # ['0_noise', '1_singing']

    # --- 3. คำนวณตัวชี้วัดประสิทธิภาพ (Evaluation Metrics) ---
    print("\n📊 --- ผลการทดสอบประสิทธิภาพของโมเดล ---")
    
    # ใช้ average='macro' เพื่อหาค่าเฉลี่ยของทั้ง 2 คลาสอย่างเป็นธรรม
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='macro')
    rec = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    
    print(f"✅ Accuracy  (ความแม่นยำ) : {acc * 100:.2f}%")
    print(f"🎯 Precision (ความเที่ยงตรง): {prec * 100:.2f}%")
    print(f"🔍 Recall    (ความรำลึก)  : {rec * 100:.2f}%")
    print(f"⚖️ F1-Score  (ค่าเฉลี่ย)    : {f1 * 100:.2f}%")
    print("-" * 40)

    # --- 4. วาดกราฟ Confusion Matrix ---
    print("\n🎨 กำลังสร้างกราฟ Confusion Matrix...")
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                annot_kws={"size": 16})
    
    plt.title('Confusion Matrix: Bird Song Classification', fontsize=16)
    plt.ylabel('True Label', fontsize=14)
    plt.xlabel('Predicted Label', fontsize=14)
    
    # บันทึกรูปภาพ
    plt.savefig(CM_SAVE_PATH, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"🎉 เสร็จสมบูรณ์! บันทึกภาพ Confusion Matrix ไว้ที่: {CM_SAVE_PATH}")
    print("นำตัวเลขและรูปภาพนี้ไปใส่ในรายงานบทที่ 4 ได้เลยครับ!")

if __name__ == "__main__":
    main()
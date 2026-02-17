import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# --- 1. ตั้งค่าไฮเปอร์พารามิเตอร์ (ตามสเปกในรายงาน) ---
IMG_HEIGHT = 128    # ความสูงภาพ [cite: 320]
IMG_WIDTH = 130     # ความกว้างภาพ [cite: 320]
CHANNELS = 1        # สีขาวดำ (1 Channel) [cite: 320]
BATCH_SIZE = 32     # จำนวนข้อมูลต่อรอบ [cite: 320]
EPOCHS = 50         # จำนวนรอบสูงสุด [cite: 320]

# ชี้เป้าไปที่โฟลเดอร์ใหม่ที่เราเพิ่งจัดกลุ่มเสร็จ
TRAIN_DIR = "ml_pipeline/data/dataset_spectrograms/train"
VAL_DIR = "ml_pipeline/data/dataset_spectrograms/val"
MODEL_SAVE_PATH = "ml_pipeline/models/bird_song_model.keras"

def main():
    print("🚀 กำลังเตรียมข้อมูลภาพเข้าสู่ระบบ (แบบไร้ Data Leakage)...")
    
    # --- 2. สร้าง Data Generator (ดึงจากโฟลเดอร์ตรงๆ ไม่ง้อ validation_split) ---
    # แค่ปรับสเกลสีให้เป็น 0-1 ก็พอครับ
    datagen = ImageDataGenerator(rescale=1./255)

    # โหลดชุดข้อมูลฝึกสอน (Training Set)
    train_generator = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',          
        batch_size=BATCH_SIZE,
        class_mode='sparse',             
        shuffle=True
    )

    # โหลดชุดข้อมูลตรวจสอบ (Validation Set)
    val_generator = datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        shuffle=False # ข้อสอบไม่ต้องสับไพ่
    )

    # --- 3. สร้างสถาปัตยกรรมโมเดล 2D CNN ---
    print("🧠 กำลังสร้างโครงข่ายประสาทเทียม (Custom 2D CNN)...")
    model = Sequential([
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, CHANNELS)),
        
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        Flatten(),
        Dropout(0.3), 
        
        Dense(2, activation='softmax') 
    ])
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
                  
    model.summary()

    # --- 4. ตั้งค่าเงื่อนไขการหยุดและการบันทึก ---
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    checkpoint = ModelCheckpoint(
        MODEL_SAVE_PATH, 
        monitor='val_accuracy', 
        save_best_only=True,     
        verbose=1 
    )
    
    # [cite_start]ตั้งค่าหยุดเมื่อไม่ดีขึ้น 5 รอบ [cite: 320]
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=5,             
        restore_best_weights=True
    )

    # --- 5. เริ่มต้นการฝึกสอน (Training) ---
    print("🔥 เริ่มต้นกระบวนการฝึกสอน AI ของจริง!")
    
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=[checkpoint, early_stop],
        verbose=1 
    )
    
    print(f"\n🎉 เทรนเสร็จสมบูรณ์! โมเดลที่ดีที่สุดถูกบันทึกไว้ที่: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    main()
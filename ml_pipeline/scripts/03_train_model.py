import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# --- 1. ตั้งค่าไฮเปอร์พารามิเตอร์ตามตารางที่ 3.9 ---
IMG_HEIGHT = 128    # ความสูงภาพ (n_mels)
IMG_WIDTH = 130     # ความกว้างภาพ (เวลา)
CHANNELS = 1        # สีขาวดำ (1 Channel)
BATCH_SIZE = 32     # จำนวนข้อมูลต่อรอบ
EPOCHS = 50         # จำนวนรอบสูงสุด
DATA_DIR = "ml_pipeline/data/04_spectrograms"
MODEL_SAVE_PATH = "ml_pipeline/models/bird_song_model.keras"

def main():
    print("🚀 กำลังเตรียมข้อมูลภาพเข้าสู่ระบบ...")
    
    # --- 2. สร้าง Data Generator (แบ่งข้อมูล 80:20) ---
    datagen = ImageDataGenerator(
        rescale=1./255, 
        validation_split=0.2 
    )

    # โหลดชุดข้อมูลฝึกสอน (Training Set 80%)
    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',          
        batch_size=BATCH_SIZE,
        class_mode='sparse',             
        subset='training',
        shuffle=True
    )

    # โหลดชุดข้อมูลตรวจสอบ (Validation Set 20%)
    val_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='validation',
        shuffle=False
    )

    # --- 3. สร้างสถาปัตยกรรมโมเดล 2D CNN (มาตรฐานใหม่) ---
    print("🧠 กำลังสร้างโครงข่ายประสาทเทียม (Custom 2D CNN)...")
    model = Sequential([
        # เลเยอร์รับข้อมูล (Input Layer) มาตรฐานใหม่ Keras 3!
        Input(shape=(IMG_HEIGHT, IMG_WIDTH, CHANNELS)),
        
        # 2DConv Layer 1 (Filter 32) + Max Pooling (2, 2)
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # 2DConv Layer 2 (Filter 64) + Max Pooling (2, 2)
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Flatten เตรียมส่งเข้า Dense Layer
        Flatten(),
        Dropout(0.3), 
        
        # Dense + Softmax Output (จำแนก 2 คลาส: 0=Noise, 1=Singing)
        Dense(2, activation='softmax') 
    ])
    
    # กำหนด Optimizer และ Loss Function 
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
                  
    model.summary()

    # --- 4. ตั้งค่าเงื่อนไขการหยุดและการบันทึก (Callbacks) ---
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    checkpoint = ModelCheckpoint(
        MODEL_SAVE_PATH, 
        monitor='val_accuracy', 
        save_best_only=True,     
        verbose=1 
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=5,             
        restore_best_weights=True
    )

    # --- 5. เริ่มต้นการฝึกสอน (Training) ---
    print("🔥 เริ่มต้นกระบวนการฝึกสอน AI (Training)...")
    print("💡 สังเกตหลอด Progress Bar ในแต่ละ Epoch ได้เลยครับ!")
    
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=[checkpoint, early_stop],
        verbose=1 # โชว์ Progress Bar
    )
    
    print(f"\n🎉 เทรนเสร็จสมบูรณ์! โมเดลสุดยอด AI ของคุณถูกบันทึกไว้ที่: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    main()
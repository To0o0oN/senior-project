import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    """เปิดการเชื่อมต่อตอนเริ่มรันเซิร์ฟเวอร์"""
    print("⏳ กำลังเชื่อมต่อฐานข้อมูล MongoDB...")
    try:
        db_instance.client = AsyncIOMotorClient(MONGO_URL)
        db_instance.db = db_instance.client[DATABASE_NAME]
        print(f"✅ เชื่อมต่อ MongoDB (ฐานข้อมูล: {DATABASE_NAME}) สำเร็จ!")
    except Exception as e:
        print(f"❌ เชื่อมต่อฐานข้อมูลล้มเหลว: {e}")

async def close_mongo_connection():
    """ปิดการเชื่อมต่อเมื่อหยุดรันเซิร์ฟเวอร์"""
    if db_instance.client:
        db_instance.client.close()
        print("✅ ปิดการเชื่อมต่อ MongoDB เรียบร้อย")
    
async def create_indexes():
    db = get_database()
    # สร้าง Index ให้ session_id (1 หมายถึงเรียงลำดับจากน้อยไปมาก)
    await db.results.create_index("session_id")
    print("✅ Index for 'session_id' created successfully.")
    
def get_database():
    """เรียกใช้ฟังก์ชันนี้ใน API เพื่อเข้าถึงฐานข้อมูล"""
    return db_instance.db
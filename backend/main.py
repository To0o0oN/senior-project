import os
from contextlib import asynccontextmanager 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.db.database import connect_to_mongo, close_mongo_connection
from backend.api.routes import predict, auth

# ตั้งค่า Lifespan ให้เปิด-ปิด DB อัตโนมัติ
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Bulbul Contests API", version="1.0.0", lifespan=lifespan)

# สร้างโฟลเดอร์เก็บไฟล์ (ถ้ายังไม่มี)
os.makedirs("uploads/images", exist_ok=True)
os.makedirs("uploads/audio", exist_ok=True)

# --- การตั้งค่า CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # อนุญาตให้ทุกโดเมนยิง API เข้ามาได้ (ตอน Deploy จริงค่อยล็อกเป็น URL ของเว็บคุณ)
    allow_credentials=True,
    allow_methods=["*"], # อนุญาตทุก Method (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# เปิดให้ Frontend เข้าถึงรูปภาพได้
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# รวม Router
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Bulbul Contests Classification Backend is Ready!"}

def main():
    print("Hello from senior-project!")

if __name__ == "__main__":
    main()

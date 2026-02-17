from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import predict

app = FastAPI(title="Bulbul Contests API", version="1.0.0")

# --- การตั้งค่า CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # อนุญาตให้ทุกโดเมนยิง API เข้ามาได้ (ตอน Deploy จริงค่อยล็อกเป็น URL ของเว็บคุณ)
    allow_credentials=True,
    allow_methods=["*"], # อนุญาตทุก Method (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api", tags=["Prediction"])

@app.get("/")
def read_root():
    return {"message": "Bulbul Contests Classification Backend is Ready!"}

def main():
    print("Hello from senior-project!")


if __name__ == "__main__":
    main()

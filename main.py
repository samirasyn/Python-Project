import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Geçici lead hafızası (veya veritabanı bağlantısı)
fake_leads_db = []

class SohbetRequest(BaseModel):
    mesaj: str

class LeadRequest(BaseModel):
    isim: str
    telefon: str

@app.get("/")
def home():
    return {"message": "Staj Projesi API calisiyor!"}

# 1. Yönergeye Uygun Sohbet Uç Noktası
@app.post("/api/sohbet")
def sohbet_et(request: SohbetRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.mesaj,
                }
            ],
            model="openai/gpt-oss-20b",
        )
        return {"cevap": chat_completion.choices[0].message.content}
    except Exception as e:
        print("HATA OLUSTU:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# 2. Yönergeye Uygun Lead Kaydetme Uç Noktası (POST /api/leads)
@app.post("/api/leads")
def lead_kaydet(request: LeadRequest):
    new_lead = {
        "_id": str(len(fake_leads_db) + 1),
        "isim": request.isim,
        "telefon": request.telefon
    }
    fake_leads_db.append(new_lead)
    return {"status": "success", "data": new_lead}

# 3. Yönergeye Uygun Lead Listeleme Uç Noktası (GET /api/leads)
@app.get("/api/leads")
def lead_getir():
    return fake_leads_db

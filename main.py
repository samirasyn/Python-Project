import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

app = FastAPI()

# Bellekte lead'leri tutmak için geçici liste (GET /api/leads için şart)
fake_leads_db = []

class SohbetRequest(BaseModel):
    mesaj: str

class LeadRequest(BaseModel):
    isim: str
    telefon: str

@app.get("/")
def home():
    return {"message": "API calisiyor!"}

# 1. Sohbet Uç Noktası (Modül G: /api/sohbet)
@app.post("/api/sohbet")
def sohbet_et(request: SohbetRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": request.mesaj}],
            model="openai/gpt-oss-20b",
        )
        return {"cevap": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Lead Kayıt Uç Noktası (Modül G: /api/leads - POST)
@app.post("/api/leads")
def lead_kaydet(request: LeadRequest):
    new_lead = {
        "_id": str(len(fake_leads_db) + 1), # Yönerge: "her objede _id zorunlu"
        "isim": request.isim,
        "telefon": request.telefon
    }
    fake_leads_db.append(new_lead)
    return {"status": "success", "data": new_lead}

# 3. Lead Listeleme Uç Noktası (Modül G: Yönetim Paneli için GET /api/leads)
@app.get("/api/leads")
def lead_getir():
    return fake_leads_db

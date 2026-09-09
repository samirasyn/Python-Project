import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "Staj Projesi API calisiyor!"}

@app.post("/generate")
def generate_text(request: PromptRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.prompt,
                }
            ],
            model="openai/gpt-oss-20b",
        )
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        print("HATA OLUSTU:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
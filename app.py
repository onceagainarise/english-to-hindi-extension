from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer
import uvicorn


model_name = "Helsinki-NLP/opus-mt-en-hi"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["POST"],  
    allow_headers=["*"],  
)

class TranslationRequest(BaseModel):
    text: str


def translate(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)


@app.get("/")
async def root():
    return {"message": "Welcome to the English to Hindi Translator API!"}

@app.post("/translate")
async def translate_api(request: TranslationRequest, response: Response):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    translated_text = translate(request.text)
    response.headers["Cache-Control"] = "public, max-age=3600"  
    response.headers["X-Content-Type-Options"] = "nosniff"  
    return {"translatedText": translated_text}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
from fastapi import FastAPI, HTTPException

from app.schemas import HealthResponse, MessageResponse, PromptRequest, PromptResponse
from app.services.llm import LLMError, generate_response

app = FastAPI(title="AI Engineering Lab")


@app.get("/", response_model=MessageResponse)
def home():
    return {"message": "Hola mundo", "service": "AI Engineering Lab"}


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.post("/generate", response_model=PromptResponse)
def generate(request: PromptRequest):
    try:
        result = generate_response(request.prompt)
    except LLMError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    return {"prompt": request.prompt, "message": result}

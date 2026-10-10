from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message: str
    service: str


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    prompt: str
    message: str

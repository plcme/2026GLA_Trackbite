from pydantic import BaseModel


class GeminiTestRequest(BaseModel):
    prompt: str


class GeminiTestResponse(BaseModel):
    response: str


class HealthResponse(BaseModel):
    status: str

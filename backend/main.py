import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import GeminiTestRequest, GeminiTestResponse, HealthResponse
from services.gemini_service import test_prompt

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("TrackBite backend starting up...")
    yield
    print("TrackBite backend shutting down...")


app = FastAPI(
    title="TrackBite API",
    version="0.1.0",
    lifespan=lifespan,
)

cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok"}


@app.post("/gemini-test", response_model=GeminiTestResponse)
async def gemini_test(body: GeminiTestRequest):
    try:
        result = await test_prompt(body.prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

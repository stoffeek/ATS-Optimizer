from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import cv

app = FastAPI(title="CV Optimizer API")

# CORS-konfiguration för att frontend ska kunna prata med backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.router)

@app.get("/")
async def root():
    return {"message": "CV Optimizer API is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
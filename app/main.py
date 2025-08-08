from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.mr_router import router as mr_router

app = FastAPI(title="MR Auto-Generate (Demo)", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(mr_router, prefix="/mr", tags=["materials-request"])

@app.get("/")
def root():
    return {"ok": True, "service": "MR Auto-Generate (Demo)"}

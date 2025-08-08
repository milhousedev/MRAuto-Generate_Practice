from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateMRRequest, MRResponse
from app.services.mr_generator import generate_mr
from app.storage.memory_store import save_mr, get_mr

router = APIRouter()

@router.post("/generate", response_model=MRResponse)
def mr_generate(payload: GenerateMRRequest):
    mr = generate_mr(payload.description, options=payload.options or {})
    mr_id = save_mr(mr)
    mr["mr_id"] = mr_id
    return mr

@router.get("/{mr_id}", response_model=MRResponse)
def mr_get(mr_id: str):
    mr = get_mr(mr_id)
    if not mr:
        raise HTTPException(status_code=404, detail="MR not found")
    return mr

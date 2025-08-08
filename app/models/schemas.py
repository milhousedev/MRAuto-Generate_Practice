from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

class GenerateOptions(BaseModel):
    return_format: Optional[Literal["json", "table", "both"]] = "json"

class GenerateMRRequest(BaseModel):
    description: str = Field(..., min_length=5)
    options: Optional[GenerateOptions] = None

class MRLineItem(BaseModel):
    item_code: str
    description: str
    category: str
    unit: str
    qty: float
    source_rule: str
    confidence: float
    notes: str = ""

class MRResponse(BaseModel):
    mr_id: Optional[str] = None
    project_meta: Dict
    assumptions: List[str]
    line_items: List[MRLineItem]
    totals: Dict
    export: Dict
    generated_at: str

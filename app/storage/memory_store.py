from typing import Dict, Optional
from datetime import datetime

_store: Dict[str, Dict] = {}
_counter = 1

def save_mr(mr: Dict) -> str:
    global _counter
    mr_id = f"MR-{datetime.utcnow().strftime('%Y%m%d')}-{_counter:04d}"
    _counter += 1
    _store[mr_id] = mr | {"mr_id": mr_id}
    return mr_id

def get_mr(mr_id: str) -> Optional[Dict]:
    return _store.get(mr_id)

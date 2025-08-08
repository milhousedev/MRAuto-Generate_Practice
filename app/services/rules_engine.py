from __future__ import annotations
from typing import Dict, List, Any
from pathlib import Path
import json, yaml, math

from app.core.config import CATALOG_PATH, RULES_PATH

class Catalog:
    _items: Dict[str, Dict] | None = None

    @classmethod
    def load(cls):
        if cls._items is None:
            with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            cls._items = {row["item_code"]: row for row in data}
        return cls._items

def _substitute_voltage(code: str, voltage_kv: int) -> str:
    return code.replace("<voltage>", str(voltage_kv))

def _safe_eval(expr: str, context: Dict[str, Any]) -> float:
    # Very small whitelist eval for qty formulas
    allowed_names = {"feeders": context.get("num_feeders", 0),
                     "transformers": context.get("num_transformers", 0)}
    return float(eval(expr, {"__builtins__": {}}, allowed_names))

def _mk_line(item_code: str, catrow: Dict, qty: float, source: str, confidence: float | None = None, notes: str = "") -> Dict:
    return {
        "item_code": item_code,
        "description": catrow["description"],
        "category": catrow["category"],
        "unit": catrow["unit"],
        "qty": float(qty),
        "source_rule": source,
        "confidence": float(confidence if confidence is not None else 0.7),
        "notes": notes or "",
    }

def load_rules() -> Dict:
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def apply_rules(features: Dict) -> List[Dict]:
    cat = Catalog.load()
    rules = load_rules()
    voltage = features["voltage_kv"]
    feeders = features["num_feeders"]
    transformers = features["num_transformers"]
    greenfield = features["greenfield"]

    items: List[Dict] = []

    # per_feeder block
    for item in rules.get("per_feeder", []):
        code = _substitute_voltage(item["item_code"], voltage)
        catrow = cat.get(code)
        if not catrow: 
            # if exact code not in catalog, try generic key like 'SA-69' etc.
            if code in cat: catrow = cat[code]
            else: continue

        if "qty_formula" in item:
            qty = _safe_eval(item["qty_formula"], {"num_feeders": feeders, "num_transformers": transformers})
        else:
            qty = item.get("qty", 1) * feeders

        items.append(_mk_line(code, catrow, qty, "per_feeder", item.get("confidence"), item.get("notes", "")))

    # per_transformer block
    for item in rules.get("per_transformer", []):
        code = _substitute_voltage(item["item_code"], voltage)
        catrow = cat.get(code)
        if not catrow: 
            if code in cat: catrow = cat[code]
            else: continue
        if "qty_formula" in item:
            qty = _safe_eval(item["qty_formula"], {"num_feeders": feeders, "num_transformers": transformers})
        else:
            qty = item.get("qty", 1) * transformers
        items.append(_mk_line(code, catrow, qty, "per_transformer", item.get("confidence"), item.get("notes", "")))

    # site_wide with simple conditions (currently only 'greenfield')
    for sw in rules.get("site_wide", []):
        cond = sw.get("when")
        if cond == "greenfield" and not greenfield:
            continue
        for item in sw.get("items", []):
            code = _substitute_voltage(item["item_code"], voltage)
            catrow = cat.get(code)
            if not catrow: 
                if code in cat: catrow = cat[code]
                else: continue
            if "qty_formula" in item:
                qty = _safe_eval(item["qty_formula"], {"num_feeders": feeders, "num_transformers": transformers})
            else:
                qty = item.get("qty", 1)
            items.append(_mk_line(code, catrow, qty, "site_wide", item.get("confidence"), item.get("notes", "")))

    # merge duplicates by item_code + unit
    merged: Dict[tuple, Dict] = {}
    for li in items:
        key = (li["item_code"], li["unit"])
        if key not in merged:
            merged[key] = li.copy()
        else:
            merged[key]["qty"] += li["qty"]
            # keep higher confidence if different
            merged[key]["confidence"] = max(merged[key]["confidence"], li["confidence"])

    # round ft quantities cleanly
    for li in merged.values():
        if li["unit"] in ("ft",):
            li["qty"] = round(li["qty"])
        else:
            # keep two decimals for everything else
            li["qty"] = float(f"{li['qty']:.2f}") if not li["qty"].is_integer() else int(li["qty"])

    return list(merged.values())

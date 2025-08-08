from typing import Dict
from app.services.parsers import parse_description, now_iso
from app.services.rules_engine import apply_rules

def _totals(line_items):
    line_count = len(line_items)
    by_category = {}
    for li in line_items:
        by_category[li["category"]] = by_category.get(li["category"], 0) + 1
    return {"line_count": line_count, "by_category": by_category}

def generate_mr(description: str, options: Dict):
    features, assumptions = parse_description(description)
    line_items = apply_rules(features)

    resp = {
        "mr_id": None,
        "project_meta": {
            "utility": features.get("utility"),
            "voltage_kv": features["voltage_kv"],
            "num_feeders": features["num_feeders"],
            "num_transformers": features["num_transformers"],
            "bus_scheme": features["bus_scheme"],
            "greenfield": features["greenfield"],
        },
        "assumptions": assumptions + [
            "Control house, 125 VDC system, and SCADA panel assumed for greenfield.",
            "Quantities are placeholders for demo and should be validated by engineering."
        ],
        "line_items": line_items,
        "totals": _totals(line_items),
        "export": {"csv_available": True, "markdown_available": True},
        "generated_at": now_iso(),
    }
    return resp

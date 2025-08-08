from typing import Dict, Tuple, List
from datetime import datetime
from app.utils.text import (
    find_voltage_kv, find_num_feeders, find_num_transformers,
    find_bus_scheme, find_utility, is_greenfield
)

DEFAULTS = {
    "voltage_kv": 69,
    "num_feeders": 2,
    "num_transformers": 1,
    "bus_scheme": "breaker-per-feeder",
    "greenfield": True,
    "utility": None,
    "control_house": True,
    "dc_system_v": 125,
    "scada": True,
}

def parse_description(desc: str) -> Tuple[Dict, List[str]]:
    assumptions = []
    features = {}

    features["voltage_kv"] = find_voltage_kv(desc) or DEFAULTS["voltage_kv"]
    if not find_voltage_kv(desc): assumptions.append("Voltage not specified; assumed 69 kV.")

    features["num_feeders"] = find_num_feeders(desc) or DEFAULTS["num_feeders"]
    if not find_num_feeders(desc): assumptions.append("Feeder count not specified; assumed 2 feeders.")

    features["num_transformers"] = find_num_transformers(desc) or DEFAULTS["num_transformers"]
    if not find_num_transformers(desc): assumptions.append("Transformer count not specified; assumed 1 transformer.")

    features["bus_scheme"] = find_bus_scheme(desc) or DEFAULTS["bus_scheme"]
    if not find_bus_scheme(desc): assumptions.append('Bus scheme not specified; assumed "breaker-per-feeder."')

    gf = is_greenfield(desc)
    features["greenfield"] = gf if gf is not None else DEFAULTS["greenfield"]
    if gf is None: assumptions.append("Site type not specified; assumed Greenfield.")

    features["utility"] = find_utility(desc) or DEFAULTS["utility"]
    if features["utility"] is None: assumptions.append("Utility not specified.")

    features["control_house"] = DEFAULTS["control_house"]
    features["dc_system_v"] = DEFAULTS["dc_system_v"]
    features["scada"] = DEFAULTS["scada"]

    return features, assumptions

def now_iso() -> str:
    # simple ISO stamp (local offset doesn’t matter for demo)
    return datetime.utcnow().isoformat() + "Z"

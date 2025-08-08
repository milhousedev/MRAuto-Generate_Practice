import re

def find_voltage_kv(text: str) -> int | None:
    m = re.search(r"(\d{2,3})\s*(kV|kv)\b", text)
    return int(m.group(1)) if m else None

def find_num_feeders(text: str) -> int | None:
    m = re.search(r"(\d+)\s*(feeders?|feeder bays?)", text, re.I)
    return int(m.group(1)) if m else None

def find_num_transformers(text: str) -> int | None:
    m = re.search(r"(\d+)\s*x?\s*(transformers?|power\s*xfmrs?)", text, re.I)
    return int(m.group(1)) if m else None

def find_bus_scheme(text: str) -> str | None:
    patterns = ["ring bus", "breaker[- ]?and[- ]?a[- ]?half", "b[- ]?and[- ]?a[- ]?half",
                "breaker[- ]?per[- ]?feeder", "double bus", "single bus"]
    for p in patterns:
        if re.search(p, text, re.I):
            return p.lower().replace("  ", " ")
    return None

def find_utility(text: str) -> str | None:
    m = re.search(r"\b(ComEd|Ameren|PGE|SCE|Duke|FPL|APS|SRP|Xcel Energy)\b", text, re.I)
    return m.group(1) if m else None

def is_greenfield(text: str) -> bool | None:
    if re.search(r"\bgreenfield\b", text, re.I): return True
    if re.search(r"\bbrownfield\b", text, re.I): return False
    return None

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "app" / "data"
CATALOG_PATH = DATA_DIR / "catalog" / "material_catalog.json"
RULES_PATH = DATA_DIR / "rules" / "mr_rules.yml"

TZ = os.getenv("TZ", "America/Phoenix")

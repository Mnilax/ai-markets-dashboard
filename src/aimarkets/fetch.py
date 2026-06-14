"""Fetch AI-category markets."""
from __future__ import annotations
import json
from pathlib import Path
from aimarkets.models import AIMarket

SNAPSHOT_PATH = Path(__file__).parent.parent.parent / "data" / "snapshot.json"

def load_snapshot() -> list[AIMarket]:
    """Load markets from cached snapshot."""
    if not SNAPSHOT_PATH.exists():
        return []
    data = json.loads(SNAPSHOT_PATH.read_text())
    return [AIMarket(**m) for m in data]

def save_snapshot(markets: list[AIMarket]) -> None:
    """Save markets to snapshot file."""
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps([m.model_dump() for m in markets], indent=2))

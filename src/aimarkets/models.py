"""Data models for AI markets."""
from __future__ import annotations
from pydantic import BaseModel

class AIMarket(BaseModel):
    id: str
    question: str
    category: str  # model_release, regulation, capability, corporate
    yes_price: float
    volume: float = 0
    close_date: str = ""
    url: str = ""
    source: str = ""

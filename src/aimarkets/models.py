"""Data models for AI markets."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AIMarket(BaseModel):
    id: str
    question: str
    category: str  # model_release, regulation, capability, corporate
    yes_price: float = Field(ge=0, le=1, allow_inf_nan=False)
    volume: float = Field(default=0, ge=0, allow_inf_nan=False)
    close_date: str = ""
    url: str = ""
    source: str = ""

"""Curate and categorize AI markets."""
from __future__ import annotations
import re
from aimarkets.models import AIMarket

CATEGORY_PATTERNS = {
    "model_release": r"(gpt|claude|gemini|llama|mistral|release|launch|ship|model)",
    "regulation": r"(regulation|act|bill|law|ban|policy|eu ai|congress|senate)",
    "capability": r"(agi|benchmark|pass|score|capability|human.level|superhuman)",
    "corporate": r"(ipo|acquisition|valuation|ceo|openai|anthropic|google|meta|funding)",
}

def categorize(question: str) -> str:
    """Categorize a market question."""
    q_lower = question.lower()
    for cat, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, q_lower):
            return cat
    return "other"

def group_by_category(markets: list[AIMarket]) -> dict[str, list[AIMarket]]:
    """Group markets by category."""
    groups: dict[str, list[AIMarket]] = {}
    for m in markets:
        cat = m.category or categorize(m.question)
        groups.setdefault(cat, []).append(m)
    return groups

def sort_markets(markets: list[AIMarket], by: str = "probability") -> list[AIMarket]:
    """Sort markets by probability, volume, or close date."""
    if by == "volume":
        return sorted(markets, key=lambda m: m.volume, reverse=True)
    elif by == "close_date":
        return sorted(markets, key=lambda m: m.close_date)
    return sorted(markets, key=lambda m: m.yes_price, reverse=True)

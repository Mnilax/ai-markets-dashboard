"""Tests for AI markets curation."""
from aimarkets.curate import categorize, group_by_category, sort_markets
from aimarkets.models import AIMarket
from aimarkets.fetch import load_snapshot

def test_categorize_model():
    assert categorize("Will GPT-5 be released?") == "model_release"
    assert categorize("Claude 4 launch date") == "model_release"

def test_categorize_regulation():
    assert categorize("EU AI Act enforcement") == "regulation"
    assert categorize("California AI safety bill") == "regulation"

def test_categorize_capability():
    assert categorize("AI achieves AGI by 2027") == "capability"
    assert categorize("Benchmark score surpasses human level") == "capability"

def test_categorize_corporate():
    assert categorize("OpenAI IPO filing") == "corporate"
    assert categorize("Anthropic valuation") == "corporate"

def test_group_by_category():
    markets = [
        AIMarket(id="1", question="GPT-5?", category="model_release", yes_price=0.7),
        AIMarket(id="2", question="EU AI Act?", category="regulation", yes_price=0.9),
        AIMarket(id="3", question="Claude 4?", category="model_release", yes_price=0.5),
    ]
    groups = group_by_category(markets)
    assert len(groups["model_release"]) == 2
    assert len(groups["regulation"]) == 1

def test_sort_markets():
    markets = [
        AIMarket(id="1", question="A", category="c", yes_price=0.3, volume=100),
        AIMarket(id="2", question="B", category="c", yes_price=0.8, volume=500),
        AIMarket(id="3", question="C", category="c", yes_price=0.5, volume=200),
    ]
    by_prob = sort_markets(markets, "probability")
    assert by_prob[0].id == "2"
    by_vol = sort_markets(markets, "volume")
    assert by_vol[0].id == "2"

def test_snapshot_loads():
    markets = load_snapshot()
    assert len(markets) == 12
    assert all(m.yes_price > 0 for m in markets)

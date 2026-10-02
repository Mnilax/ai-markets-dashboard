import pytest
from pydantic import ValidationError

from aimarkets import fetch
from aimarkets.curate import categorize, sort_markets
from aimarkets.models import AIMarket


def test_snapshot_utf8_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "SNAPSHOT_PATH", tmp_path / "snapshot.json")
    markets = [AIMarket(id="1", question="ИИ 출시?", category="other", yes_price=0)]
    fetch.save_snapshot(markets)
    assert fetch.load_snapshot() == markets


@pytest.mark.parametrize("price", [-0.1, 1.1, float("nan"), float("inf")])
def test_invalid_market_probability(price):
    with pytest.raises(ValidationError):
        AIMarket(id="1", question="Q", category="other", yes_price=price)


def test_category_matches_whole_words():
    assert categorize("Will a bank increase rates?") == "other"
    assert categorize("Contract expires this year?") == "other"


def test_missing_close_date_sorts_last():
    markets = [AIMarket(id="1", question="Q", category="other", yes_price=0.5),
               AIMarket(id="2", question="Q", category="other", yes_price=0.5, close_date="2027-01-01")]
    assert [m.id for m in sort_markets(markets, "close_date")] == ["2", "1"]

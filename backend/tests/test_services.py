from datetime import date, timedelta
from types import SimpleNamespace
from app.services import estimate_risk, match_score

def test_risk_estimate_is_bounded_and_disclaimed():
    item=SimpleNamespace(crop="Tomato",harvest_date=date.today()-timedelta(days=5))
    result=estimate_risk(item)
    assert 0 <= result["risk_percent"] <= 100
    assert result["days_remaining"] == 2
    assert "does not measure freshness" in result["disclaimer"]

def test_matching_uses_listing_and_requirement_fields():
    product=SimpleNamespace(crop="Tomato",harvest_date=date.today(),quantity_kg=500,price_per_kg=20,quality="Good",pickup_date=None,organic=False,village="",district="Tumakuru",state="Karnataka")
    requirement=SimpleNamespace(crop="Tomato",min_quantity_kg=200,quantity_kg=400,max_price_per_kg=25,quality="Good",pickup_by=None,location="Tumakuru",organic=False)
    score,reasons=match_score(product,requirement)
    assert score == 90
    assert "Location matches" in reasons

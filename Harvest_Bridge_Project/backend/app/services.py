from datetime import date
from .models import Product, BuyerRequirement

# Illustrative planning windows, not measured spoilage. Administrators can extend this table.
SHELF_DAYS = {"tomato": 7, "onion": 35, "potato": 45, "ragi": 180, "rice": 180,
              "maize": 90, "beans": 5, "chilli": 14, "coconut": 30, "spinach": 3, "leafy greens": 3}

def estimate_risk(product: Product):
    shelf = SHELF_DAYS.get(product.crop.lower(), 10)
    elapsed = max(0, (date.today() - product.harvest_date).days)
    remaining = max(0, shelf - elapsed)
    risk = min(100, round(elapsed / shelf * 100))
    label = "Critical urgency" if remaining <= 1 else "High risk" if risk >= 70 else "Moderate risk" if risk >= 35 else "Low risk"
    return {"risk_percent": risk, "days_remaining": remaining, "status": label,
            "disclaimer": "Planning estimate based on crop and harvest date; it does not measure freshness or prove spoilage."}

def match_score(product: Product, requirement: BuyerRequirement):
    score, reasons = 20, ["Crop matches"]
    if product.quantity_kg >= requirement.min_quantity_kg:
        score += 15; reasons.append("Meets minimum quantity")
    elif product.quantity_kg >= requirement.quantity_kg * .5:
        score += 8; reasons.append("Part of requested quantity available")
    if requirement.location and requirement.location.lower() in f"{product.village} {product.district} {product.state}".lower():
        score += 15; reasons.append("Location matches")
    if requirement.max_price_per_kg is None or product.price_per_kg <= requirement.max_price_per_kg:
        score += 15; reasons.append("Within buyer price limit")
    if requirement.quality == "Any" or requirement.quality.lower() == product.quality.lower():
        score += 10; reasons.append("Quality preference matches")
    if not requirement.pickup_by or not product.pickup_date or product.pickup_date <= requirement.pickup_by:
        score += 10; reasons.append("Pickup date is suitable")
    if not requirement.organic or product.organic:
        score += 5; reasons.append("Organic preference matches")
    risk = estimate_risk(product)
    score += 10 if risk["days_remaining"] <= 2 else 5 if risk["days_remaining"] <= 5 else 0
    if risk["days_remaining"] <= 5: reasons.append("Urgent lot prioritized")
    return min(100, score), reasons

def product_dict(p: Product, db=None):
    from .models import User, FarmerProfile
    risk = estimate_risk(p)
    farmer = db.get(User, p.farmer_id) if db else None
    profile = db.query(FarmerProfile).filter_by(user_id=p.farmer_id).first() if db else None
    phone = farmer.phone if farmer and p.phone_visible and profile and profile.show_phone else None
    return {"id":p.id,"farmer_id":p.farmer_id,"farmer_name":farmer.name if farmer else "Farmer",
      "phone":phone,"crop":p.crop,"category":p.category,"quantity_kg":p.quantity_kg,"price_per_kg":p.price_per_kg,
      "harvest_date":str(p.harvest_date),"pickup_date":str(p.pickup_date) if p.pickup_date else None,"quality":p.quality,
      "organic":p.organic,"organic_status":p.organic_status,"image_url":p.image_url,"village":p.village,
      "district":p.district,"state":p.state,"description":p.description,"status":p.status,"priority":p.priority,**risk}

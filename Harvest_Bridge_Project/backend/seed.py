import os
from datetime import date, timedelta
from app.database import Base, engine, SessionLocal
from app.models import User, FarmerProfile, BuyerProfile, AdminProfile, Product, BuyerRequirement
from app.security import hash_password

Base.metadata.create_all(bind=engine)
db=SessionLocal()
try:
    if db.query(User).count():
        print("Database already has users; seed skipped.")
    else:
        demo=[
          User(name="Ananya Demo Farm",email="farmer@harvestbridge.demo",phone="0000000001",role="farmer",password_hash=hash_password("2026"),language="en"),
          User(name="Kiran Demo Produce",email="farmer.kn@harvestbridge.demo",phone="0000000002",role="farmer",password_hash=hash_password("2026"),language="kn"),
          User(name="Green Basket Demo",email="buyer@harvestbridge.demo",phone="0000000003",role="buyer",password_hash=hash_password("BuyerDemo!2026")),
          User(name="Market Link Demo",email="buyer2@harvestbridge.demo",phone="0000000004",role="buyer",password_hash=hash_password("BuyerDemo!2026")),
          User(name="Harvest Bridge Admin",email=os.getenv("ADMIN_EMAIL","admin@harvestbridge.demo"),role="admin",password_hash=hash_password(os.getenv("ADMIN_PASSWORD","HarvestDemo!2026")))
        ]
        db.add_all(demo);db.flush()
        db.add_all([FarmerProfile(user_id=demo[0].id,village="Demo Village",district="Tumakuru",state="Karnataka"),FarmerProfile(user_id=demo[1].id,village="Sample Hobali",district="Mandya",state="Karnataka"),BuyerProfile(user_id=demo[2].id,business_name="Green Basket Demo",location="Tumakuru, Karnataka"),BuyerProfile(user_id=demo[3].id,business_name="Market Link Demo",location="Mandya, Karnataka")])
        db.add(AdminProfile(user_id=demo[4].id))
        crops=[("Tomato",420,18,5,True,"Farmer-declared Organic"),("Onion",900,24,9,False,"Conventional"),("Potato",650,21,4,False,"Conventional"),("Ragi",1200,36,12,False,"Conventional"),("Rice",800,42,7,False,"Conventional"),("Maize",700,19,6,False,"Conventional"),("Beans",160,48,2,True,"Verification Pending"),("Chilli",250,55,8,False,"Conventional"),("Coconut",300,28,10,False,"Conventional")]
        for i,(crop,qty,price,age,organic,status) in enumerate(crops):
            db.add(Product(farmer_id=demo[i%2].id,crop=crop,quantity_kg=qty,price_per_kg=price,harvest_date=date.today()-timedelta(days=age),pickup_date=date.today()+timedelta(days=2),organic=organic,organic_status=status,quality="Good",village="Demo Village",district="Tumakuru" if i%2==0 else "Mandya",state="Karnataka",description="Fictional demonstration listing. Prices are seller-entered, not mandi data."))
        db.add_all([BuyerRequirement(buyer_id=demo[2].id,crop="Tomato",quantity_kg=300,min_quantity_kg=200,max_price_per_kg=25,quality="Good",location="Tumakuru"),BuyerRequirement(buyer_id=demo[3].id,crop="Beans",quantity_kg=100,min_quantity_kg=50,max_price_per_kg=60,organic=True,location="Mandya")])
        db.commit();print("Demo accounts and fictional marketplace listings created.")
finally:
    db.close()

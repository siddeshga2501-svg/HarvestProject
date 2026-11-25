"""Health behavior checks that do not contact external providers."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, _otp_codes, _otp_verified, health, request_otp, verify_otp, register, login
from app.schemas import LoginIn, OtpIn, RegisterIn

def test_health_reports_unconfigured_live_integrations():
    body=health()
    assert body["status"] == "ok"
    assert "unavailable" in body["integrations"]["mandi"]


def test_farmer_can_register_and_sign_in_with_mobile_and_four_digit_pin():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    db = Session(engine)
    phone = "9000000001"
    try:
        assert "/api/auth/otp/request" in app.openapi()["paths"]
        sent = request_otp(OtpIn(phone=phone), None)
        code = sent["dev_otp"]
        assert verify_otp(OtpIn(phone=phone, code=code), None)["verified"] is True

        registered = register(RegisterIn(
            role="farmer", name="Demo Farmer", phone=phone,
            pin="4826", otp="verified", language="en",
        ), db, None)
        assert registered["user"]["role"] == "farmer"

        signed_in = login(LoginIn(username=phone, pin="4826"), db, None)
        assert signed_in["user"]["role"] == "farmer"
    finally:
        db.close()
        _otp_codes.pop(phone, None)
        _otp_verified.pop(phone, None)
        engine.dispose()

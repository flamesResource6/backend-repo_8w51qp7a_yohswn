import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Booking, Advisor

app = FastAPI(title="Spiritual Advice Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateBookingResponse(BaseModel):
    id: str
    status: str


def to_serializable(doc: dict) -> dict:
    d = doc.copy()
    if d.get("_id") is not None:
        d["id"] = str(d.pop("_id"))
    return d


@app.on_event("startup")
def seed_advisors_if_empty():
    try:
        if db is None:
            return
        existing = db["advisor"].count_documents({})
        if existing == 0:
            seed_data = [
                {
                    "name": "Ava Ocean",
                    "specialties": ["Mindfulness", "Meditation", "Breathwork"],
                    "bio": "Guiding you to inner calm through ocean-inspired mindfulness.",
                    "rating": 4.9,
                    "photo": "https://images.unsplash.com/photo-1527980965255-d3b416303d12?q=80&w=800&auto=format&fit=crop"
                },
                {
                    "name": "Kai Rivers",
                    "specialties": ["Life Purpose", "Clarity", "Intuition"],
                    "bio": "Find your flow and align with your natural rhythm.",
                    "rating": 4.8,
                    "photo": "https://images.unsplash.com/photo-1544006659-f0b21884ce1d?q=80&w=800&auto=format&fit=crop"
                },
                {
                    "name": "Mira Tide",
                    "specialties": ["Energy Healing", "Emotional Balance"],
                    "bio": "Gentle guidance for healing and emotional harmony.",
                    "rating": 4.9,
                    "photo": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=800&auto=format&fit=crop"
                }
            ]
            for item in seed_data:
                db["advisor"].insert_one(item)
    except Exception:
        # If seeding fails, ignore to keep API running
        pass


@app.get("/")
def read_root():
    return {"message": "Spiritual Advice Booking API is running"}


@app.get("/api/advisors")
def list_advisors(limit: Optional[int] = 12):
    try:
        docs = get_documents("advisor", {}, limit)
        return [to_serializable(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/bookings", response_model=CreateBookingResponse)
def create_booking(payload: Booking):
    try:
        inserted_id = create_document("booking", payload)
        return {"id": inserted_id, "status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/bookings")
def list_bookings(limit: Optional[int] = 20):
    try:
        docs = get_documents("booking", {}, limit)
        return [to_serializable(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

"""
KrishiJal Mitra – backend/main.py
FastAPI backend for Farmer Profile
Run with:  uvicorn backend.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import get_db, init_db
import json

app = FastAPI(title="KrishiJal Mitra API", version="1.0")

# ── CORS: lets your index.html talk to this server ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change to your domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables on startup
init_db()


# ── Data Model ───────────────────────────────────────
class FarmerProfile(BaseModel):
    device_id:        str
    language:         str   | None = None   # 'marathi' | 'hindi' | 'english'
    mode:             str   | None = None   # 'quick_advice' | 'detailed_plan'
    district:         str   | None = None
    taluka:           str   | None = None
    village:          str   | None = None
    pincode:          str   | None = None
    lat:              float | None = None
    lng:              float | None = None
    farm_size_bucket: str   | None = None   # '<1_ha' | '1_2_ha' | '2_5_ha' | '>5_ha'
    farmer_type:      str   | None = None   # 'small' | 'marginal' | 'other'
    irrigation_source:str   | None = None   # 'borewell' | 'canal' | 'rainfed' | 'farm_pond'
    crop:             str   | None = None
    growth_stage:     str   | None = None   # 'sowing' | 'vegetative' | 'flowering' | 'fruiting' | 'harvest'


# ── POST /api/profile  →  Save / Update profile ──────
@app.post("/api/profile")
def save_profile(profile: FarmerProfile):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO farmers (
            device_id, language, mode,
            district, taluka, village, pincode, lat, lng,
            farm_size_bucket, farmer_type, irrigation_source, crop, growth_stage
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        ON CONFLICT(device_id) DO UPDATE SET
            language          = excluded.language,
            mode              = excluded.mode,
            district          = excluded.district,
            taluka            = excluded.taluka,
            village           = excluded.village,
            pincode           = excluded.pincode,
            lat               = excluded.lat,
            lng               = excluded.lng,
            farm_size_bucket  = excluded.farm_size_bucket,
            farmer_type       = excluded.farmer_type,
            irrigation_source = excluded.irrigation_source,
            crop              = excluded.crop,
            growth_stage      = excluded.growth_stage,
            updated_at        = CURRENT_TIMESTAMP
    """, (
        profile.device_id, profile.language, profile.mode,
        profile.district, profile.taluka, profile.village,
        profile.pincode, profile.lat, profile.lng,
        profile.farm_size_bucket, profile.farmer_type,
        profile.irrigation_source, profile.crop, profile.growth_stage
    ))

    # Log every save to history table
    cursor.execute(
        "INSERT INTO profiles_history (device_id, profile_json) VALUES (?,?)",
        (profile.device_id, json.dumps(profile.model_dump()))
    )

    conn.commit()
    conn.close()
    return {"success": True, "message": "Profile saved 🌾"}


# ── GET /api/profile/{device_id}  →  Fetch profile ───
@app.get("/api/profile/{device_id}")
def get_profile(device_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farmers WHERE device_id = ?", (device_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"success": True, "profile": dict(row)}


# ── DELETE /api/profile/{device_id}  →  Remove profile
@app.delete("/api/profile/{device_id}")
def delete_profile(device_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM farmers WHERE device_id = ?", (device_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Profile not found")

    cursor.execute("DELETE FROM farmers WHERE device_id = ?", (device_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Profile '{device_id}' deleted"}


# ── GET /api/health  →  Health check ─────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "app": "KrishiJal Mitra 🌾"}
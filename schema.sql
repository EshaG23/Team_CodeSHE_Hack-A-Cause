-- =============================
-- ONBOARDING / FARMERS TABLE
-- 30 sec onboarding: language, mode, location, optional profile
-- =============================
-- language: 'marathi' | 'hindi' | 'english'
-- mode: 'quick_advice' (30 sec) | 'detailed_plan' (2 min)
-- location: auto GPS (lat,lng) OR manual (district, taluka, village/pincode)
-- farm_size_bucket: '<1_ha' | '1_2_ha' | '2_5_ha' | '>5_ha'
-- farmer_type: 'small' | 'marginal' | 'other'
-- irrigation_source: 'borewell' | 'canal' | 'rainfed' | 'farm_pond'
-- crop: 'cotton' | 'soybean' | 'wheat' | etc.
-- growth_stage: 'sowing' | 'vegetative' | 'flowering' | 'fruiting' | 'harvest'
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT UNIQUE NOT NULL,

    -- 1. Select Language
    language TEXT CHECK (language IN ('marathi', 'hindi', 'english') OR language IS NULL),

    -- 2. Choose Mode
    mode TEXT CHECK (mode IN ('quick_advice', 'detailed_plan') OR mode IS NULL),

    -- 3. Location: GPS or manual (offline-friendly)
    district TEXT,
    taluka TEXT,
    village TEXT,
    pincode TEXT,
    lat REAL,
    lng REAL,

    -- 4. Farmer profile (optional, for scheme matching)
    farm_size_bucket TEXT CHECK (farm_size_bucket IN ('<1_ha', '1_2_ha', '2_5_ha', '>5_ha') OR farm_size_bucket IS NULL),
    farmer_type TEXT CHECK (farmer_type IN ('small', 'marginal', 'other') OR farmer_type IS NULL),
    irrigation_source TEXT CHECK (irrigation_source IN ('borewell', 'canal', 'rainfed', 'farm_pond') OR irrigation_source IS NULL),
    crop TEXT,
    growth_stage TEXT CHECK (growth_stage IN ('sowing', 'vegetative', 'flowering', 'fruiting', 'harvest') OR growth_stage IS NULL),

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_farmers_device_id ON farmers(device_id);

-- =============================
-- PROFILE HISTORY (OPTIONAL)
-- =============================
CREATE TABLE IF NOT EXISTS profiles_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    profile_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================
-- OFFLINE SYNC QUEUE (OPTIONAL)
-- =============================
CREATE TABLE IF NOT EXISTS sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    action TEXT,
    payload TEXT,
    synced INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
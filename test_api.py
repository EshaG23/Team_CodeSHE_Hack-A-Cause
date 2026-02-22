import requests
import json

# Test data for farmer profile
test_profile = {
    "device_id": "test_device_123",
    "language": "english",
    "mode": "quick_advice",
    "district": "Pune",
    "taluka": "Haveli",
    "village": "Test Village",
    "pincode": "411001",
    "lat": 18.5204,
    "lng": 73.8567,
    "farm_size_bucket": "1_2_ha",
    "farmer_type": "small",
    "irrigation_source": "borewell",
    "crop": "Wheat",
    "growth_stage": "vegetative"
}

try:
    # Test POST to save profile
    response = requests.post("http://127.0.0.1:8000/api/profile", 
                           json=test_profile,
                           headers={"Content-Type": "application/json"})
    
    print("POST Response Status:", response.status_code)
    print("POST Response:", response.json())
    
    # Test GET to retrieve profile
    get_response = requests.get(f"http://127.0.0.1:8000/api/profile/{test_profile['device_id']}")
    print("\nGET Response Status:", get_response.status_code)
    print("GET Response:", get_response.json())
    
except Exception as e:
    print("Error:", e)

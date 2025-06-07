#!/usr/bin/env python3
"""
Simple test script to verify TSA API is working and storing data in Supabase
"""

import requests
import json

def test_tsa_api():
    """Test the TSA API with a sample item"""
    
    # API endpoint
    url = "http://localhost:8000/check-item"
    
    # Test data
    test_items = [
        "laptop",
        "toothpaste",
        "knife",
        "water bottle"
    ]
    
    print("Testing TSA Item Checker API with Supabase integration...")
    print("=" * 60)
    
    for item in test_items:
        print(f"\n🔍 Testing item: {item}")
        
        # Make the API request
        response = requests.post(
            url,
            json={"item_name": item},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Carry-on: {data['carry_on']}")
            print(f"✅ Checked bag: {data['checked_bag']}")
            print(f"📝 Description: {data['description']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    print("\n" + "=" * 60)
    print("Test completed! Check your Supabase dashboard to see the logged data.")

if __name__ == "__main__":
    test_tsa_api() 
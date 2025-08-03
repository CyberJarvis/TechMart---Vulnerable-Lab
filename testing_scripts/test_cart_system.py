#!/usr/bin/env python3
"""
Test Cart System for Vulnerable E-commerce Lab
Tests the new Amazon-like cart functionality with business logic vulnerability
"""

import requests
import json

def test_cart_system():
    session = requests.Session()
    base_url = "http://127.0.0.1:5002"
    
    print("🛒 Testing Cart System for Vulnerable E-commerce Lab")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_data = {
        'username': 'john_doe',
        'password': 'password123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data)
    if response.status_code == 200 and "Dashboard" in response.text:
        print("   ✅ Login successful")
    else:
        print("   ❌ Login failed")
        return False
    
    # Step 2: Add items to cart
    print("\n2. Adding items to cart...")
    
    # Add Laptop (product_id = 1)
    cart_data = {
        'product_id': '1',
        'quantity': '2'
    }
    
    response = session.post(f"{base_url}/add_to_cart", data=cart_data)
    if response.status_code == 200:
        print("   ✅ Added 2x Laptop to cart")
    else:
        print(f"   ❌ Failed to add laptop to cart: {response.status_code}")
    
    # Add Phone (product_id = 2)
    cart_data = {
        'product_id': '2',
        'quantity': '1'
    }
    
    response = session.post(f"{base_url}/add_to_cart", data=cart_data)
    if response.status_code == 200:
        print("   ✅ Added 1x Phone to cart")
    else:
        print(f"   ❌ Failed to add phone to cart: {response.status_code}")
    
    # Step 3: View cart
    print("\n3. Viewing cart...")
    response = session.get(f"{base_url}/cart")
    if response.status_code == 200 and "Shopping Cart" in response.text:
        print("   ✅ Cart view successful")
        # Extract cart total from response
        if "Total:" in response.text:
            print("   💰 Cart contains items with total price")
    else:
        print("   ❌ Failed to view cart")
    
    # Step 4: Test business logic vulnerability - Apply coupon multiple times
    print("\n4. Testing Business Logic Vulnerability...")
    print("   🎯 Attempting to apply MEGA50 coupon multiple times during checkout")
    
    # Go to checkout
    checkout_data = {
        'coupon_code': 'MEGA50'
    }
    
    # Apply coupon first time
    response = session.post(f"{base_url}/purchase", data=checkout_data)
    if "successfully applied" in response.text.lower():
        print("   ✅ First application of MEGA50 coupon successful")
        
        # Try to apply same coupon again (vulnerability)
        response = session.post(f"{base_url}/purchase", data=checkout_data)
        if "successfully applied" in response.text.lower():
            print("   🚨 VULNERABILITY CONFIRMED: Coupon applied multiple times!")
            print("   💸 Business logic flaw allows coupon reuse")
        else:
            print("   ℹ️  Coupon reuse properly prevented")
    
    # Step 5: Complete purchase
    print("\n5. Completing purchase...")
    purchase_data = {}  # Empty data to complete purchase
    
    response = session.post(f"{base_url}/purchase", data=purchase_data)
    if "Order placed successfully" in response.text or "Purchase completed" in response.text:
        print("   ✅ Purchase completed successfully")
        print("   🛍️  Amazon-like cart system working correctly")
    else:
        print("   ⚠️  Purchase completion status unclear")
    
    print("\n" + "=" * 60)
    print("🎉 Cart system test completed!")
    print("🔍 The new system provides realistic shopping flow for vulnerability testing")

if __name__ == "__main__":
    test_cart_system()

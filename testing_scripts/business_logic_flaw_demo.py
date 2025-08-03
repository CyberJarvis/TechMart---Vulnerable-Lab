#!/usr/bin/env python3
"""
Business Logic Flaw Demonstration
=================================

This script demonstrates the business logic flaw in the coupon system
where applying coupons gives more discount than intended.
"""

import requests
import json

def test_business_logic_flaw():
    print("🎯 BUSINESS LOGIC FLAW TESTING")
    print("=" * 50)
    
    session = requests.Session()
    
    # Login
    print("🔑 Logging in...")
    response = session.post('http://127.0.0.1:5002/login', 
                           data={'username': 'john_doe', 'password': 'password123'})
    
    if 'dashboard' not in response.url and response.status_code != 302:
        print("❌ Login failed")
        return
    
    print("✅ Login successful")
    
    # Add items to cart
    print("🛒 Adding items to cart...")
    session.post('http://127.0.0.1:5002/add_to_cart', data={'product_id': 1, 'quantity': 2})  # Smartphone - $899.99 x 2
    session.post('http://127.0.0.1:5002/add_to_cart', data={'product_id': 3, 'quantity': 1})  # Gaming Mouse - $79.99 x 1
    
    print("✅ Added items: 2x Smartphone ($899.99 each), 1x Gaming Mouse ($79.99)")
    print(f"   Expected total: ${2 * 899.99 + 79.99:.2f}")
    
    print("\n🎫 TESTING DIFFERENT COUPONS:")
    
    # Test different coupons to show business logic flaws
    coupons_to_test = [
        {'code': 'SAVE10', 'expected': '10%', 'description': 'Should be 10% off'},
        {'code': 'WELCOME5', 'expected': '5%', 'description': 'Should be 5% off'}, 
        {'code': 'MEGA50', 'expected': '50%', 'description': 'Should be 50% off'}
    ]
    
    for coupon in coupons_to_test:
        print(f"\n🧪 Testing coupon: {coupon['code']}")
        print(f"   Expected: {coupon['description']}")
        
        # Apply coupon
        response = session.post('http://127.0.0.1:5002/apply_coupon', 
                               data={'coupon_code': coupon['code']})
        
        if response.status_code == 200:
            # Parse response to extract discount information
            content = response.text
            if 'You save $' in content:
                # Extract discount amount from response
                import re
                discount_match = re.search(r'You save \$([0-9.]+)', content)
                percent_match = re.search(r'\(([0-9.]+)% off\)', content)
                
                if discount_match and percent_match:
                    actual_discount = float(discount_match.group(1))
                    actual_percent = float(percent_match.group(1))
                    
                    print(f"   🚨 ACTUAL: ${actual_discount:.2f} ({actual_percent:.1f}% off)")
                    
                    # Calculate what it should have been
                    original_total = 2 * 899.99 + 79.99
                    if coupon['code'] == 'SAVE10':
                        expected_discount = original_total * 0.10
                        print(f"   ✅ Expected: ${expected_discount:.2f} (10.0% off)")
                        print(f"   💰 EXTRA SAVINGS: ${actual_discount - expected_discount:.2f}")
                    elif coupon['code'] == 'WELCOME5':
                        expected_discount = original_total * 0.05
                        print(f"   ✅ Expected: ${expected_discount:.2f} (5.0% off)")
                        print(f"   💰 EXTRA SAVINGS: ${actual_discount - expected_discount:.2f}")
                    elif coupon['code'] == 'MEGA50':
                        expected_discount = original_total * 0.50
                        print(f"   ✅ Expected: ${expected_discount:.2f} (50.0% off)")
                        print(f"   💰 EXTRA SAVINGS: ${actual_discount - expected_discount:.2f}")
                        
                else:
                    print("   ❌ Could not parse discount information")
            else:
                print("   ❌ No discount information found")
        else:
            print(f"   ❌ Failed to apply coupon: HTTP {response.status_code}")
    
    print(f"\n🎉 BUSINESS LOGIC FLAW SUMMARY:")
    print(f"   • SAVE10: Gives 15% instead of 10% (extra 5%)")
    print(f"   • WELCOME5: Gives $X per item instead of 5% total")
    print(f"   • MEGA50: Gives 50% + $10 bonus per item type")
    print(f"   • Other coupons: Double the discount rate")
    print(f"   • If discount > total: Items become FREE!")

if __name__ == "__main__":
    test_business_logic_flaw()

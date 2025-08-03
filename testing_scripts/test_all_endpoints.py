#!/usr/bin/env python3
"""
Comprehensive Endpoint Status Checker for Vulnerable E-Commerce Lab
This script tests all endpoints and identifies issues.
"""

import requests
import json
from urllib.parse import urljoin

class EndpointTester:
    def __init__(self, base_url="http://127.0.0.1:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.issues = []
        
    def test_endpoint(self, endpoint, method='GET', data=None, expected_status=200, description=""):
        """Test a single endpoint and return results"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, allow_redirects=False)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=data, allow_redirects=False)
            else:
                response = self.session.request(method, url, data=data, allow_redirects=False)
            
            status = response.status_code
            
            # Analyze response
            result = {
                'endpoint': endpoint,
                'method': method,
                'status': status,
                'description': description,
                'url': url,
                'response_length': len(response.text),
                'headers': dict(response.headers),
                'has_error': False,
                'error_type': None,
                'issues': []
            }
            
            # Check for common issues
            if status == 500:
                result['has_error'] = True
                result['error_type'] = 'Internal Server Error'
                result['issues'].append('500 Internal Server Error - Backend issue')
                
            elif status == 404:
                result['has_error'] = True
                result['error_type'] = 'Not Found'
                result['issues'].append('404 Not Found - Endpoint missing')
                
            elif status == 405:
                result['has_error'] = True
                result['error_type'] = 'Method Not Allowed'
                result['issues'].append('405 Method Not Allowed - HTTP method issue')
                
            elif 'error' in response.text.lower() or 'exception' in response.text.lower():
                result['has_error'] = True
                result['error_type'] = 'Application Error'
                result['issues'].append('Application error detected in response')
            
            # Check for template issues
            if 'TemplateNotFound' in response.text:
                result['has_error'] = True
                result['error_type'] = 'Template Missing'
                result['issues'].append('Template file missing')
                
            # Check for database issues
            if 'no such column' in response.text.lower():
                result['has_error'] = True
                result['error_type'] = 'Database Schema Error'
                result['issues'].append('Database column missing')
                
            return result
            
        except requests.exceptions.ConnectionError:
            return {
                'endpoint': endpoint,
                'method': method,
                'status': 'Connection Error',
                'description': description,
                'has_error': True,
                'error_type': 'Connection Failed',
                'issues': ['Cannot connect to server - is it running?']
            }
        except Exception as e:
            return {
                'endpoint': endpoint,
                'method': method,
                'status': 'Exception',
                'description': description,
                'has_error': True,
                'error_type': 'Test Exception',
                'issues': [f'Test error: {str(e)}']
            }
    
    def run_comprehensive_test(self):
        """Test all endpoints comprehensively"""
        
        print("🔍 COMPREHENSIVE ENDPOINT STATUS CHECK")
        print("=" * 60)
        
        # Define all endpoints to test
        endpoints = [
            # Basic pages
            ('/', 'GET', None, 'Homepage'),
            ('/login', 'GET', None, 'Login page'),
            ('/register', 'GET', None, 'Registration page'),
            ('/dashboard', 'GET', None, 'User dashboard'),
            ('/profile', 'GET', None, 'User profile'),
            ('/logout', 'GET', None, 'Logout'),
            
            # Product pages
            ('/product/1', 'GET', None, 'Product details'),
            
            # Admin pages
            ('/admin', 'GET', None, 'Admin panel'),
            ('/admin/users', 'GET', None, 'Admin user management'),
            ('/admin/add_user', 'GET', None, 'Admin add user form'),
            ('/admin/wallet', 'GET', None, 'Admin wallet management'),
            
            # User features
            ('/wallet', 'GET', None, 'User wallet'),
            ('/news', 'GET', None, 'News page'),
            ('/support', 'GET', None, 'Support page'),
            ('/support/create', 'GET', None, 'Create support ticket'),
            
            # Vulnerable endpoints
            ('/secret_add_money', 'GET', None, 'Secret money addition'),
            ('/quick_money', 'GET', None, 'Quick money feature'),
            ('/file_manager', 'GET', None, 'File manager'),
            ('/xml_import', 'GET', None, 'XML import feature'),
            ('/render_template', 'GET', None, 'Template rendering'),
            ('/view_file', 'GET', None, 'File viewer'),
            
            # API endpoints
            ('/api/users', 'GET', None, 'Users API'),
            ('/api/products', 'GET', None, 'Products API'),
            
            # Role-based pages
            ('/moderator', 'GET', None, 'Moderator panel'),
            ('/seller_dashboard', 'GET', None, 'Seller dashboard'),
            
            # POST endpoints (basic test)
            ('/login', 'POST', {'username': 'test', 'password': 'test'}, 'Login POST'),
            ('/add_comment', 'POST', {'product_id': '1', 'comment': 'test'}, 'Add comment'),
            ('/check_url', 'POST', {'url': 'http://example.com'}, 'URL checker'),
            ('/ping', 'POST', {'host': 'google.com'}, 'Ping command'),
        ]
        
        results = []
        error_count = 0
        
        for endpoint, method, data, description in endpoints:
            print(f"\n🧪 Testing: {method} {endpoint}")
            result = self.test_endpoint(endpoint, method, data, description=description)
            results.append(result)
            
            if result['has_error']:
                error_count += 1
                print(f"   ❌ {result['status']} - {result['error_type']}")
                for issue in result['issues']:
                    print(f"      • {issue}")
            else:
                print(f"   ✅ {result['status']} - OK")
        
        # Summary report
        print("\n" + "=" * 60)
        print("📊 ENDPOINT STATUS SUMMARY")
        print("=" * 60)
        
        total_endpoints = len(results)
        working_endpoints = total_endpoints - error_count
        
        print(f"Total Endpoints Tested: {total_endpoints}")
        print(f"Working Endpoints: {working_endpoints}")
        print(f"Endpoints with Issues: {error_count}")
        print(f"Success Rate: {(working_endpoints/total_endpoints)*100:.1f}%")
        
        if error_count > 0:
            print(f"\n🚨 ISSUES FOUND ({error_count} endpoints):")
            print("-" * 40)
            for result in results:
                if result['has_error']:
                    print(f"❌ {result['method']} {result['endpoint']}")
                    print(f"   Status: {result['status']}")
                    print(f"   Error: {result['error_type']}")
                    for issue in result['issues']:
                        print(f"   • {issue}")
                    print()
        
        return results, error_count

if __name__ == "__main__":
    tester = EndpointTester()
    results, error_count = tester.run_comprehensive_test()
    
    if error_count == 0:
        print("\n🎉 All endpoints are working correctly!")
    else:
        print(f"\n⚠️  {error_count} endpoints need attention!")

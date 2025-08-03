# 🧪 Testing Scripts Directory

This directory contains all vulnerability testing and exploitation scripts for the Vulnerable E-Commerce Lab.

## 📋 **Script Categories**

### **🔍 Comprehensive Testing**
- **`comprehensive_scanner.py`** - Tests all vulnerabilities in sequence
- **`test_all_vulnerabilities.py`** - Complete vulnerability assessment
- **`test_all_endpoints.py`** - Tests all application endpoints
- **`max_impact_exploiter.py`** - Maximum impact exploitation tool

### **💉 SQL Injection Testing**
- **`SQLI_WORKING_PROOF.py`** - SQL injection proof of concept
- **`test_sql_injection.py`** - SQL injection vulnerability tester

### **🔍 Search Vulnerabilities**
- **`search_vulnerability_tester.py`** - Tests SQL injection, XSS, and SSTI in search

### **🔓 Broken Access Control (BAC)**
- **`bac_test.py`** - General BAC vulnerability testing
- **`bac_comment_exploit.py`** - Comment impersonation exploit
- **`bac_curl_examples.sh`** - cURL commands for BAC testing

### **🏃‍♂️ Race Condition Exploits**
- **`race_condition_exploit.py`** - General race condition testing
- **`apply_coupon_race_exploit.py`** - Coupon race condition exploit
- **`aggressive_race_test.py`** - Advanced race condition testing
- **`turbo_intruder_race_condition_manual.py`** - Burp Suite Turbo Intruder script

### **💰 Business Logic Flaws**
- **`business_logic_flaw_demo.py`** - Business logic vulnerability demonstration

### **🌐 Network Vulnerabilities**
- **`ssrf_exploit.py`** - Server-Side Request Forgery testing

### **🛒 Shopping Cart Testing**
- **`test_cart_system.py`** - Shopping cart functionality tests

### **🌐 Browser-Based Exploits**
- **`simple_browser_race.js`** - Simple browser race condition
- **`apply_coupon_browser_race.js`** - Coupon race condition in browser
- **`browser_race_condition_exploit.js`** - Advanced browser race condition

### **🎯 Professional Testing Tools**
- **`burp_suite_payloads.py`** - Payloads for Burp Suite Intruder

---

## 🚀 **Quick Start Guide**

### **Comprehensive Testing**
```bash
# Test all vulnerabilities automatically
python testing_scripts/comprehensive_scanner.py

# Maximum impact exploitation
python testing_scripts/max_impact_exploiter.py
```

### **Specific Vulnerability Testing**
```bash
# SQL Injection
python testing_scripts/test_sql_injection.py

# Search vulnerabilities
python testing_scripts/search_vulnerability_tester.py

# BAC in comments
python testing_scripts/bac_comment_exploit.py

# Race conditions
python testing_scripts/apply_coupon_race_exploit.py

# Business logic flaws
python testing_scripts/business_logic_flaw_demo.py
```

### **Browser Console Testing**
```javascript
// Copy and paste into browser console (F12)

// Load any race condition script
fetch('/testing_scripts/apply_coupon_browser_race.js')
  .then(response => response.text())
  .then(script => eval(script));
```

### **Burp Suite Integration**
1. Load payloads from `burp_suite_payloads.py`
2. Use `turbo_intruder_race_condition_manual.py` for race conditions
3. Configure Intruder with provided payload lists

### **Manual Testing with cURL**
```bash
# BAC vulnerability examples
./testing_scripts/bac_curl_examples.sh
```

---

## 📊 **Script Usage Matrix**

| Vulnerability Type | Primary Scripts | Difficulty | Impact |
|-------------------|----------------|------------|---------|
| SQL Injection | `test_sql_injection.py`, `SQLI_WORKING_PROOF.py` | Easy | High |
| XSS | `search_vulnerability_tester.py` | Easy | Medium |
| BAC | `bac_comment_exploit.py`, `bac_test.py` | Easy | High |
| Race Condition | `apply_coupon_race_exploit.py`, `aggressive_race_test.py` | Medium | High |
| Business Logic | `business_logic_flaw_demo.py` | Easy | High |
| SSRF | `ssrf_exploit.py` | Medium | High |
| Search Vulns | `search_vulnerability_tester.py` | Easy | Medium |

---

## 🎯 **Testing Workflows**

### **Beginner Workflow**
1. `comprehensive_scanner.py` - Overview of all vulnerabilities
2. `test_sql_injection.py` - Easy SQL injection
3. `bac_comment_exploit.py` - Simple impersonation
4. `business_logic_flaw_demo.py` - Free items exploit

### **Intermediate Workflow**
1. `max_impact_exploiter.py` - High impact exploits
2. `apply_coupon_race_exploit.py` - Race condition mastery
3. `search_vulnerability_tester.py` - Multiple search vulns
4. `ssrf_exploit.py` - Network-based attacks

### **Advanced Workflow**
1. `aggressive_race_test.py` - Complex race conditions
2. `turbo_intruder_race_condition_manual.py` - Professional tools
3. `burp_suite_payloads.py` - Advanced payloads
4. Custom payload development

### **Penetration Testing Workflow**
1. **Reconnaissance**: `test_all_endpoints.py`
2. **Vulnerability Scanning**: `comprehensive_scanner.py`
3. **Exploitation**: `max_impact_exploiter.py`
4. **Advanced Techniques**: Burp Suite integration
5. **Report Generation**: Document findings

---

## ⚠️ **Important Notes**

### **Educational Use Only**
- These scripts are for educational purposes
- Only test on systems you own or have permission to test
- Do not use on production systems

### **Prerequisites**
- Python 3.7+ installed
- `requests` library: `pip install requests`
- `concurrent.futures` for race conditions
- Modern web browser for JavaScript exploits

### **Lab Requirements**
- Vulnerable lab must be running: `python app.py`
- Default URL: `http://127.0.0.1:5002`
- Valid user accounts for authentication testing

---

## 🔧 **Troubleshooting**

### **Common Issues**
1. **Connection Refused**: Ensure lab is running on port 5002
2. **Import Errors**: Install required Python packages
3. **Authentication Required**: Some scripts need valid login
4. **Rate Limiting**: Add delays between requests if needed

### **Debug Mode**
Most scripts support verbose output for debugging:
```bash
python testing_scripts/script_name.py --verbose
```

---

## 📚 **Learning Resources**

### **Related Documentation**
- `../COMPLETE_EXPLOITATION_GUIDE.md` - Comprehensive exploitation guide
- `../QUICK_REFERENCE.md` - Quick vulnerability reference
- `../VULNERABILITY_GUIDE.md` - Detailed vulnerability explanations

### **Professional Tools**
- **Burp Suite Professional** - Use with provided payloads
- **OWASP ZAP** - Alternative security testing tool
- **SQLMap** - Advanced SQL injection testing

---

**🎊 Happy Ethical Hacking! Use these tools responsibly for learning and authorized testing only!**

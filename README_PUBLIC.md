# 🚨 Cybersecurity Education Lab - Vulnerable E-Commerce Platform

> **⚠️ WARNING**: This application contains **INTENTIONAL SECURITY VULNERABILITIES** for educational purposes only. **DO NOT** use in production environments!

## 🎯 Purpose

This is a **deliberately vulnerable** web application designed for:
- **Cybersecurity education and training**
- **Penetration testing practice**
- **Security awareness demonstrations**
- **Vulnerability assessment learning**

## 🚀 Live Demo

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/vulnerable-ecommerce-lab)

**🔗 Live Demo**: [https://your-app.onrender.com](https://your-app.onrender.com)

## 🔑 Access Credentials

### Lab Access (Required for hosted version)
Choose any of these credentials to access the lab:
```
guest_user / guest123
test_user  / test123
lab_user   / lab123  
demo_user  / demo123
```

### Application User Accounts
```
Admin:     admin / admin123
Moderator: moderator / mod123
User:      user1 / password123
Guest:     guest_user / guest123
```

## 🛡️ Vulnerabilities Included

This lab contains **18+ vulnerability categories** covering:

### OWASP Top 10 2021
1. **SQL Injection** - Login bypass, data extraction
2. **XSS (Cross-Site Scripting)** - Stored and reflected
3. **Broken Access Control** - IDOR, privilege escalation
4. **Security Misconfiguration** - Debug mode, weak secrets
5. **Vulnerable Components** - Insecure dependencies
6. **Authentication Failures** - Weak passwords, session issues

### Additional Vulnerabilities
7. **Business Logic Flaws** - Coupon abuse, race conditions
8. **CSRF (Cross-Site Request Forgery)** - State-changing operations
9. **Directory Traversal** - File system access
10. **SSRF (Server-Side Request Forgery)** - Internal network access
11. **SSTI (Server-Side Template Injection)** - Code execution
12. **Insecure Deserialization** - Object injection
13. **Command Injection** - System command execution
14. **File Inclusion** - Local file access
15. **XXE (XML External Entity)** - XML parsing attacks
16. **Information Disclosure** - Sensitive data exposure
17. **Race Conditions** - Concurrent request abuse
18. **Weak Cryptography** - MD5 hashes, weak secrets

## 🏃‍♂️ Quick Start

### Option 1: Deploy to Render.com (Recommended)
1. **Fork this repository**
2. **Connect to Render.com**
3. **Deploy automatically** (uses `render.yaml`)
4. **Access with lab credentials**

### Option 2: Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vulnerable-ecommerce-lab.git
cd vulnerable-ecommerce-lab

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python app.py

# Access at http://127.0.0.1:5002
```

## 🎓 Learning Objectives

- **Identify common vulnerabilities** in web applications
- **Practice exploitation techniques** in a safe environment
- **Understand security implications** of poor coding practices
- **Learn secure coding** by seeing what NOT to do

## 🧪 Testing Examples

### SQL Injection
```sql
admin' OR '1'='1' --
' UNION SELECT username,password FROM users --
```

### XSS Payloads
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

### Directory Traversal
```
/files/app.py
/read/etc/passwd
/download/../app.py
```

## ⚖️ Legal and Ethical Use

### ✅ Permitted: Educational training, security research, authorized testing
### ❌ Prohibited: Unauthorized testing, malicious attacks, production use

## 📄 License

MIT License - Educational use only

---

**Remember**: This lab is for **EDUCATIONAL PURPOSES ONLY**! 🎓🔒

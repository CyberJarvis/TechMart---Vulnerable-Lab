# TechMart - Vulnerable Web Application Lab

[![Security Lab](https://img.shields.io/badge/Type-Security%20Lab-red.svg)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-Educational%20Use-orange.svg)](#license)

## 📋 Overview

TechMart is a realistic e-commerce platform intentionally designed with security vulnerabilities for educational and training purposes. This application serves as a comprehensive testing ground for security professionals, students, and researchers to practice identifying and exploiting common web application vulnerabilities in a controlled environment.

### 🎯 Educational Objectives

- **Penetration Testing Training**: Practice systematic vulnerability discovery
- **Security Assessment Skills**: Learn to identify real-world security flaws
- **Secure Development**: Understand common pitfalls in web application development
- **Bug Bounty Preparation**: Simulate realistic target environments
- **Security Research**: Study vulnerability patterns and exploitation techniques

## �️ Architecture

```
TechMart Lab
├── Web Application (Flask)
├── SQLite Database
├── File System Components
├── Network Services
└── Authentication System
```

### Technology Stack
- **Backend**: Python 3.13 + Flask 2.3.3
- **Database**: SQLite3
- **Frontend**: Bootstrap 5 + Jinja2 Templates
- **Additional**: Requests library for SSRF capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Recommended: 3.13)
- Git
- Virtual environment support

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd TechMart-VulnLab
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python app.py
```

5. **Access the application**
- Navigate to `http://127.0.0.1:5001`
- The application will automatically create sample data

### Docker Deployment (Optional)
```bash
docker-compose up -d
```

## 🔐 Security Scope

This lab contains **12+ distinct vulnerability categories** designed to simulate real-world security issues:

### Authentication & Authorization
- Broken authentication mechanisms
- Insufficient authorization controls
- Session management flaws

### Input Validation
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Command injection flaws

### Business Logic
- Payment processing vulnerabilities
- Workflow bypass issues
- Rate limiting failures

### Server-Side Issues
- Server-side template injection
- Server-side request forgery
- File inclusion vulnerabilities

### Configuration & Design
- Insecure direct object references
- Missing security headers
- Information disclosure

## 👥 Default Test Accounts

The application includes pre-configured accounts for testing:

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| Administrator | `admin` | `admin123` | Full system access |
| Standard User | `john_doe` | `password123` | Regular customer account |
| Test User | `test_user` | `test123` | Additional test account |

## 🧪 Testing Methodology

### Systematic Approach
1. **Reconnaissance**: Explore the application functionality
2. **Authentication Testing**: Test login mechanisms
3. **Input Validation**: Test all input fields
4. **Business Logic**: Examine purchase flows
5. **Access Controls**: Test authorization boundaries
6. **Server-Side**: Test server functionality

### Recommended Tools
- **Burp Suite Community/Professional**
- **OWASP ZAP**
- **Postman** for API testing
- **Browser Developer Tools**
- **Custom Python scripts** (organized in `/testing_scripts`)

## 📁 Project Structure

```
TechMart-VulnLab/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker configuration
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── exploits/               # Browser-based exploit examples
├── testing_scripts/        # Comprehensive vulnerability testing tools
├── database/               # SQLite database files
├── uploads/                # File upload directory
├── documentation/          # Additional documentation
└── tests/                  # Automated test suites
```

## 🧪 Testing Scripts

The `testing_scripts/` directory contains comprehensive vulnerability testing tools:

- **`comprehensive_scanner.py`** - Complete vulnerability assessment
- **`max_impact_exploiter.py`** - Maximum impact exploitation
- **`test_all_vulnerabilities.py`** - All vulnerability tests
- **Individual testers** - SQL injection, XSS, CSRF, BAC, IDOR, SSRF, and more
- **Race condition exploits** - Advanced concurrency testing
- **Burp Suite integration** - Professional tools compatibility

### Quick Start Testing
```bash
# Run comprehensive scan
python testing_scripts/comprehensive_scanner.py

# Test specific vulnerabilities
python testing_scripts/test_sql_injection.py
python testing_scripts/bac_comment_exploit.py

# Test new search functionality
python testing_scripts/search_vulnerability_tester.py
```

For detailed testing documentation, see [`testing_scripts/README.md`](testing_scripts/README.md).

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for detailed error messages
- `SECRET_KEY`: Application secret (intentionally weak for lab purposes)
- `DATABASE_URL`: SQLite database path

### Security Notes
- Debug mode is **intentionally enabled** for educational visibility
- Error messages are **verbose** to assist learning
- Logging is **comprehensive** for analysis purposes

## 🎓 Learning Paths

### Beginner Level
1. Start with authentication bypass
2. Practice basic XSS identification
3. Explore file upload vulnerabilities

### Intermediate Level
1. SQL injection exploitation
2. Business logic flaw analysis
3. CSRF attack construction

### Advanced Level
1. Server-side template injection
2. Command injection chaining
3. Complete application compromise

## ⚠️ Legal and Ethical Notice

### Educational Use Only
This application is designed exclusively for educational purposes in controlled environments. Users must:

- **Only test on owned/authorized systems**
- **Respect all applicable laws and regulations**
- **Use for learning and improvement purposes only**
- **Not deploy in production environments**

### Disclaimer
The maintainers assume no responsibility for misuse of this software. This tool is provided "as-is" for educational purposes only.

## 🤝 Contributing

Contributions are welcome! Please read our contribution guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for new vulnerabilities
4. Submit a detailed pull request

### Areas for Contribution
- Additional vulnerability types
- Enhanced exploitation scripts
- Better documentation
- Docker improvements
- CI/CD integration

## 📚 Additional Resources

### Learning Materials
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Application Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bug Bounty Methodology](https://github.com/jhaddix/tbhm)

### Similar Projects
- DVWA (Damn Vulnerable Web Application)
- WebGoat
- bWAPP

## 📄 License

This project is licensed for educational use only. See LICENSE file for details.

## 📞 Support

For questions, issues, or educational guidance:
- Open an issue on GitHub
- Review the documentation
- Check existing discussions

---

**Remember: With great power comes great responsibility. Use this knowledge to build more secure applications and make the web safer for everyone.**

### 7. Server-Side Request Forgery (SSRF)
- **Location**: `/check_url` endpoint
- **Description**: No URL validation for internal requests
- **Test Payload**: `http://127.0.0.1:22` or `file:///etc/passwd`
- **Impact**: Internal network access, data exfiltration

### 8. Server-Side Template Injection (SSTI)
- **Location**: `/render_template` endpoint
- **Description**: Direct template rendering without sanitization
- **Test Payload**: `{{ 7*7 }}` or `{{ config }}`
- **Impact**: Remote code execution, server compromise

### 9. Insecure Deserialization
- **Location**: User preferences functionality
- **Description**: Uses Python pickle for serialization
- **Test Method**: Modify preferences cookie with malicious payload
- **Impact**: Remote code execution

### 10. Command Injection
- **Location**: `/ping` endpoint
- **Description**: Unsanitized input in shell commands
- **Test Payload**: `127.0.0.1; cat /etc/passwd`
- **Impact**: System command execution

### 11. Broken Authentication & Authorization
- **Location**: Admin panel (`/admin`)
- **Description**: No authentication checks
- **Test Method**: Direct access to admin URLs
- **Impact**: Administrative access, data exposure

### 12. Additional Vulnerabilities
- Weak session management
- Information disclosure through debug mode
- Insecure password storage (MD5)
- Missing security headers
- Verbose error messages

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

### Default Credentials

| Role  | Username | Password    |
|-------|----------|-------------|
| Admin | admin    | admin123    |
| User  | john_doe | password123 |
| User  | jane_smith | secret456  |

## 🧪 Testing Scenarios

### SQL Injection Testing
1. Navigate to `/login`
2. Enter `' OR '1'='1' --` in username field
3. Enter any password
4. Observe successful login bypass

### XSS Testing
1. Navigate to any product page
2. Add comment: `<script>alert('XSS')</script>`
3. Refresh page to see XSS execution

### IDOR Testing
1. Make a purchase and note the receipt URL
2. Change the order ID to access other users' receipts
3. Try URLs like `/receipt/1`, `/receipt/2`, etc.

### CSRF Testing
1. Create HTML file with malicious password change form
2. Host it on different domain/port
3. Visit while logged into VulnShop
4. Observe password change

### Directory Traversal Testing
1. Navigate to `/view_file?file=../../../etc/passwd`
2. Try other system files like `/etc/hosts`, `/proc/version`

### Automated Testing
For comprehensive vulnerability testing, use the organized scripts in `testing_scripts/`:

```bash
# Quick comprehensive scan
python testing_scripts/comprehensive_scanner.py

# Individual vulnerability tests
python testing_scripts/test_sql_injection.py
python testing_scripts/search_vulnerability_tester.py
python testing_scripts/bac_comment_exploit.py

# Race condition exploits
python testing_scripts/apply_coupon_race_exploit.py
python testing_scripts/quick_race_exploit.py
```

See [`testing_scripts/README.md`](testing_scripts/README.md) for complete documentation.

## ⚠️ Security Disclaimer

**IMPORTANT SECURITY NOTICE:**

This application is intentionally vulnerable and designed for educational purposes only.

### Do NOT:
- Deploy this application on public servers
- Use this code as a template for real applications
- Leave this application running on shared networks
- Use real credentials or sensitive data

### Recommended Usage:
- Local development environments only
- Isolated virtual machines
- Educational lab environments
- Security training sessions

## 📞 Support

For educational use and questions:
- Create an issue in the repository
- Check existing documentation
- Review OWASP resources

Remember: This is for learning purposes only. Always follow responsible disclosure practices in real-world scenarios.

---

**Happy Learning! 🔐**

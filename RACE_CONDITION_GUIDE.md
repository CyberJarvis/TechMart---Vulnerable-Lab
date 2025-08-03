# Race Condition Vulnerability - Coupon Application Exploit

## 🎯 Vulnerability Overview

**Vulnerability Type**: Business Logic Flaw + Race Condition  
**OWASP Category**: A04:2021 - Insecure Design  
**Severity**: High  
**Affected Endpoint**: `POST /purchase`

## 📝 Vulnerability Description

The application contains a race condition vulnerability in the coupon application logic. When multiple concurrent requests are sent to apply the same coupon code (SAVE10), the application fails to properly synchronize coupon usage validation, allowing the same coupon to be applied multiple times in rapid succession.

### Root Cause Analysis

```python
# VULNERABLE CODE in app.py
if coupon_code:
    # 1. Check coupon usage (non-atomic)
    cursor.execute("SELECT discount_percent, used_count, usage_limit FROM coupons WHERE code = ? AND active = 1", (coupon_code,))
    coupon = cursor.fetchone()
    
    if coupon:
        # 2. Critical race condition window (100ms delay)
        import time
        time.sleep(0.1)  # Processing time allows concurrent requests
        
        # 3. Apply discount without proper locking
        discount = (discount_percent / 100) * total_price
        total_price -= discount
        
        # 4. Non-atomic increment (happens after discount applied)
        cursor.execute("UPDATE coupons SET used_count = used_count + 1 WHERE code = ?", (coupon_code,))
```

### Vulnerability Chain

1. **Time-of-Check-Time-of-Use (TOCTOU)**: Gap between coupon validation and usage increment
2. **Non-Atomic Operations**: Coupon check and update are separate operations
3. **No Concurrency Control**: No database locks or application-level synchronization
4. **Processing Delay**: Intentional 100ms delay creates exploitable race window

## 🔧 Exploitation Methods

### Method 1: Automated Script (`race_condition_exploit.py`)

```bash
# Run the automated exploit
python race_condition_exploit.py

# Expected Output:
# 🚨 RACE CONDITION EXPLOITED!
#    Multiple coupon applications likely occurred!
#    Expected: 1 coupon application
#    Actual: 15 requests succeeded
```

### Method 2: Burp Suite + Turbo Intruder

1. **Capture the Request**:
   ```http
   POST /purchase HTTP/1.1
   Host: 127.0.0.1:5002
   Cookie: session=eyJ1c2VyX2lkIjoxfQ...
   Content-Type: application/x-www-form-urlencoded
   
   coupon_code=SAVE10
   ```

2. **Send to Turbo Intruder**:
   - Right-click → Extensions → Turbo Intruder → Send to Turbo Intruder
   - Use the provided `turbo_intruder_race_condition.py` script
   - Set concurrency to 15-20 threads

3. **Expected Results**:
   - Multiple HTTP 302 responses (successful purchases)
   - Same coupon applied multiple times
   - Excessive discount applied

### Method 3: Burp Suite Repeater (Manual)

1. **Capture** the POST /purchase request with coupon_code=SAVE10
2. **Send to Repeater** and create 10+ tabs with identical requests  
3. **Simultaneous Send**: Use Ctrl+Click to send all requests at once
4. **Observe**: Multiple successful responses with same coupon

## 🕰️ Timing Analysis

- **Race Condition Window**: 100ms (time.sleep(0.1))
- **Optimal Thread Count**: 10-20 concurrent requests
- **Success Rate**: ~90-95% with proper timing
- **Detection Method**: Monitor debug logs for multiple "Applied discount" messages

## 📊 Impact Assessment

### Business Impact
- **Financial Loss**: Customers get excessive discounts (multiple 10% applications)
- **Coupon Budget Depletion**: Single coupon can be used far beyond intended limits
- **Revenue Impact**: Products sold at unintended deep discounts

### Technical Impact
- **Database Inconsistency**: Coupon usage counts become inaccurate
- **Audit Trail Corruption**: Multiple transactions with same coupon code
- **System Load**: Concurrent requests may cause performance issues

## 🔍 Detection Methods

### Application Logs
```bash
# Look for multiple discount applications
grep "Applied.*discount.*with coupon" app.log

# Expected vulnerable output:
# [DEBUG] Applied 10.0% discount ($129.99) with coupon SAVE10
# [DEBUG] Applied 10.0% discount ($129.99) with coupon SAVE10  
# [DEBUG] Applied 10.0% discount ($129.99) with coupon SAVE10
```

### Database Analysis
```sql
-- Check for suspicious coupon usage patterns
SELECT coupon_code, COUNT(*) as usage_count, 
       MIN(created_at) as first_use, MAX(created_at) as last_use
FROM orders 
WHERE coupon_code = 'SAVE10' 
  AND DATE(created_at) = CURRENT_DATE
GROUP BY coupon_code, user_id
HAVING COUNT(*) > 1;

-- Check wallet transactions for multiple discounts
SELECT user_id, description, amount, created_at
FROM wallet_transactions 
WHERE description LIKE '%SAVE10%'
ORDER BY created_at DESC;
```

## 🛡️ Remediation

### Immediate Fix (Database Level)
```python
# Use database transactions with proper locking
def apply_coupon_safe(coupon_code, user_id, amount):
    conn = sqlite3.connect('vulnerable_shop.db')
    conn.execute('BEGIN EXCLUSIVE')  # Exclusive lock
    
    try:
        cursor = conn.cursor()
        
        # Atomic check and update
        cursor.execute("""
            UPDATE coupons 
            SET used_count = used_count + 1 
            WHERE code = ? AND active = 1 AND used_count < usage_limit
            AND NOT EXISTS (
                SELECT 1 FROM orders 
                WHERE user_id = ? AND coupon_code = ? 
                AND DATE(created_at) = DATE('now')
            )
        """, (coupon_code, user_id, coupon_code))
        
        if cursor.rowcount == 0:
            conn.rollback()
            return None, "Coupon invalid or already used"
            
        # Get coupon details after successful update
        cursor.execute("SELECT discount_percent FROM coupons WHERE code = ?", (coupon_code,))
        discount_percent = cursor.fetchone()[0]
        
        conn.commit()
        return discount_percent, None
        
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### Application-Level Fix
```python
import threading
coupon_lock = threading.Lock()

def purchase():
    # Use application-level locking
    with coupon_lock:
        # Coupon validation and application logic here
        pass
```

## 📋 Testing Checklist

- [ ] Verify race condition window exists (100ms delay)
- [ ] Confirm multiple concurrent requests succeed  
- [ ] Check debug logs show multiple discount applications
- [ ] Validate database shows excessive coupon usage
- [ ] Verify user receives unintended multiple discounts
- [ ] Test with different coupon codes (SAVE10, WELCOME20, MEGA50)
- [ ] Confirm exploit works across different user sessions

## 🎓 Educational Value

This vulnerability demonstrates:
- **Race Condition Attacks** in web applications
- **TOCTOU (Time-of-Check-Time-of-Use)** vulnerabilities
- **Business Logic Bypass** through timing attacks  
- **Concurrency Issues** in financial transactions
- **Database Transaction** importance in e-commerce

## 🚨 Disclaimer

This vulnerability is intentionally implemented for educational and testing purposes only. Never exploit race conditions in production systems without explicit authorization.

---
*Part of the Vulnerable E-commerce Security Lab*

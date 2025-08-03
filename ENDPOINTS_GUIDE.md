# 🔥 Vulnerable E-Commerce Lab - Complete Endpoint Guide

## 🚀 **Application Status: FULLY OPERATIONAL**
- ✅ Database: Properly initialized with wallet system
- ✅ Static Images: Fixed (SVG placeholders created)
- ✅ All Routes: Working with proper authentication
- ✅ Wallet System: Implemented with multiple vulnerabilities
- ✅ Role-Based Access: Admin/Moderator/Seller/User/Guest roles

---

## 🎯 **Main Application Endpoints**

### 🏠 **Public Pages**
- `/` - Homepage with product catalog
- `/login` - Login page (Vulnerable to SQL Injection)
- `/register` - User registration
- `/news` - News and announcements
- `/support` - Support center
- `/support/create` - Create support ticket

### 👤 **User Dashboard & Profile**
- `/dashboard` - User dashboard with orders and wallet balance
- `/profile` - User profile with account information
- `/update_profile` - Update user profile (POST)
- `/change_password` - Change password page

### 🛒 **E-Commerce Features**
- `/buy/<int:product_id>` - Purchase product
- `/receipt/<int:order_id>` - View order receipt
- `/comment/<int:product_id>` - Add product comments (XSS vulnerable)

---

## 💰 **Wallet System Endpoints**

### 🔒 **Legitimate Wallet Access**
- `/wallet` - View wallet balance and transaction history
- `/admin/wallet` - Admin wallet management (requires admin role)
- `/admin/add_money` - Admin add money to user accounts (POST)

### 🚨 **Vulnerable Wallet Endpoints (Educational)**

#### 1. **Secret Money Addition** - No Authentication
```
GET/POST /secret_add_money
```
- **Vulnerability**: Broken Access Control
- **Exploit**: Direct URL access without authentication
- **Form Fields**: `user_id`, `amount`, `description`

#### 2. **Quick Money via URL Parameters**
```
GET /quick_money?amount=X&user_id=Y
```
- **Vulnerability**: Parameter Tampering
- **Example**: `/quick_money?amount=100&user_id=4`
- **Exploit**: Modify URL parameters to add money

#### 3. **Weak API Token Authentication**
```
POST /api/wallet/add
Content-Type: application/json
{
    "user_id": 4,
    "amount": 50.00,
    "token": "admin123"
}
```
- **Vulnerability**: Hardcoded API Token
- **Token**: `admin123`
- **Exploit**: Use weak token to access API

---

## 👑 **Administrative Endpoints**

### 🛡️ **Admin Panel** (Requires Admin Role)
- `/admin` - Main admin dashboard with statistics
- `/admin/users` - User management
- `/admin/add_user` - Add new user (GET/POST)

### 👮 **Moderator Panel** (Requires Moderator Role)
- `/moderator` - Moderator dashboard for content moderation

### 🏪 **Seller Dashboard** (Requires Seller Role)
- `/seller_dashboard` - Seller dashboard for product management

---

## 🔐 **Default Login Credentials**

### Admin Access
```
Username: admin
Password: admin123
```

### Moderator Access
```
Username: moderator  
Password: mod123
```

### Seller Access
```
Username: seller
Password: sell123
```

### Regular Users
```
Username: john_doe     | Password: password123
Username: jane_smith   | Password: mypass
Username: guest_user   | Password: guest
Username: test_user    | Password: test
```

---

## 🎯 **Vulnerability Categories Implemented**

### 1. **Financial/Authentication Vulnerabilities**
- **Broken Access Control**: `/secret_add_money` accessible without auth
- **Parameter Tampering**: `/quick_money` with URL parameters
- **Weak API Security**: Hardcoded token `admin123`
- **Client-Side Data Exposure**: Session data in browser console

### 2. **Classic Web Vulnerabilities**
- **SQL Injection**: Login form bypass (`admin' OR '1'='1' --`)
- **Cross-Site Scripting (XSS)**: Product comments
- **Server-Side Template Injection (SSTI)**: Template rendering
- **Directory/Path Traversal**: File inclusion
- **Command Injection**: System command execution
- **Server-Side Request Forgery (SSRF)**: External URL requests

### 3. **Business Logic Flaws**
- **Coupon Abuse**: Multiple usage of single-use coupons
- **Insecure Direct Object References (IDOR)**: Access other users' data
- **Cross-Site Request Forgery (CSRF)**: No token protection

### 4. **Authentication & Authorization Issues**
- **Broken Authentication**: Weak password policies
- **Session Management**: Predictable session tokens
- **Role-Based Access Control Bypasses**: URL manipulation

---

## 🧪 **Testing Examples**

### SQL Injection (Login)
```sql
Username: admin' OR '1'='1' --
Password: anything
```

### XSS in Comments
```html
<script>alert('XSS vulnerability!')</script>
```

### Wallet Exploitation Examples
```bash
# Direct access to secret money page
curl http://127.0.0.1:5001/secret_add_money

# Parameter tampering
curl "http://127.0.0.1:5001/quick_money?amount=1000&user_id=4"

# API token exploitation
curl -X POST http://127.0.0.1:5001/api/wallet/add \
  -H "Content-Type: application/json" \
  -d '{"user_id": 4, "amount": 500, "token": "admin123"}'
```

---

## 📊 **Database Schema**

### Users Table
- `id`, `username`, `password` (MD5), `email`, `role`, `created_at`, `wallet_balance` (default: $200)

### Products Table
- `id`, `name`, `description`, `price`, `stock`, `image_url`, `is_featured`

### Wallet Transactions Table  
- `id`, `user_id`, `amount`, `transaction_type`, `description`, `admin_id`, `created_at`

### Orders Table
- `id`, `user_id`, `product_id`, `quantity`, `total_price`, `promo_code`, `discount`, `order_date`

### News Table
- `id`, `title`, `content`, `author_id`, `is_published`, `created_at`

### Coupons Table
- `id`, `code`, `discount_percent`, `usage_limit`, `used_count`, `active`, `created_at`

### API Keys Table
- `id`, `api_key`, `user_id`, `permissions`, `is_active`, `created_at`

### Comments, Support Tickets, File Uploads Tables
- Complete relational structure with foreign key constraints

---

## 🎨 **Static Assets Fixed**
- ✅ `laptop.jpg` - Gaming laptop SVG placeholder
- ✅ `phone.jpg` - Smartphone SVG placeholder  
- ✅ `mouse.jpg` - Gaming mouse SVG placeholder
- ✅ `headphones.jpg` - Headphones SVG placeholder
- ✅ `watch.jpg` - Smart watch SVG placeholder

---

## 🛠️ **Development Information**
- **Framework**: Flask 2.3.3
- **Database**: SQLite3 with vulnerable_shop.db
- **Authentication**: MD5 hashing (intentionally weak)
- **Session Management**: Flask sessions
- **Static Files**: SVG placeholders for product images
- **Security Level**: Intentionally vulnerable for education

---

## ⚠️ **Security Warnings**

> **🚨 CRITICAL NOTICE**: This application contains INTENTIONAL security vulnerabilities for educational purposes only. 

**DO NOT:**
- Deploy in production environments
- Use with real user data
- Connect to public networks without isolation
- Use any code patterns in real applications

**DO:**
- Use in isolated testing environments only
- Study vulnerabilities for educational purposes
- Practice ethical hacking techniques
- Learn secure coding practices by understanding what NOT to do

---

## 🎓 **Educational Value**
This lab demonstrates:
1. **Real-world vulnerability patterns**
2. **Financial application security risks**
3. **Authentication and authorization flaws**
4. **Business logic vulnerability exploitation**
5. **Secure coding best practices (by showing what to avoid)**

Perfect for:
- Security researchers
- Penetration testing practice
- Web application security training
- Vulnerability assessment learning

---

**🌐 Access the application**: http://127.0.0.1:5001

**📝 Happy Ethical Hacking!** 🔒

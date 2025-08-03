#!/usr/bin/env python3
"""
Vulnerable E-Commerce Platform - Educational Lab
WARNING: This application contains intentional security vulnerabilities.
DO NOT deploy this in production environments!
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_file, make_response, flash, Response
import sqlite3
import hashlib
import os
import uuid
import requests
from datetime import datetime
import pickle
from functools import wraps
import base64
from jinja2 import Template
import subprocess
import re

app = Flask(__name__)
app.secret_key = 'super-secret-key-123'  # Weak secret key
app.config['DEBUG'] = True  # Debug mode enabled for SQL injection output

# Deployment safety - Add basic authentication for hosted versions
@app.before_request
def require_lab_access():
    # Skip auth for static files and specific routes
    if request.endpoint in ['static', 'lab_login'] or request.path.startswith('/static/'):
        return
    
    # Check if this is a hosted environment (not local)
    if os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT') or request.host != '127.0.0.1:5002':
        auth = request.authorization
        # Use existing lab users for authentication
        valid_users = {
            'guest_user': 'guest123',
            'test_user': 'test123', 
            'lab_user': 'lab123',
            'demo_user': 'demo123'
        }
        
        if not auth or auth.username not in valid_users or valid_users[auth.username] != auth.password:
            return Response(
                '''🚨 CYBERSECURITY LAB ACCESS 🚨
                
This is an educational cybersecurity lab with intentional vulnerabilities.
Choose any of these access credentials:

Username: guest_user | Password: guest123
Username: test_user  | Password: test123  
Username: lab_user   | Password: lab123
Username: demo_user  | Password: demo123

⚠️ FOR EDUCATIONAL USE ONLY ⚠️''', 
                401, 
                {'WWW-Authenticate': 'Basic realm="Cybersecurity Education Lab"'}
            )

@app.route('/lab_login')
def lab_login():
    return """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; border: 2px solid #e74c3c; background: #f8f9fa;">
        <h1 style="color: #e74c3c;">🚨 Cybersecurity Education Lab</h1>
        <p><strong>⚠️ Warning:</strong> This is an educational cybersecurity lab containing <strong>intentional vulnerabilities</strong>.</p>
        
        <h3>🔑 Access Credentials (Choose Any):</h3>
        <div style="background: #f1f2f6; padding: 15px; border-radius: 5px; font-family: monospace;">
            <strong>guest_user</strong> / guest123<br>
            <strong>test_user</strong> / test123<br>
            <strong>lab_user</strong> / lab123<br>
            <strong>demo_user</strong> / demo123
        </div>
        
        <h3>🎯 Lab User Accounts:</h3>
        <div style="background: #f1f2f6; padding: 15px; border-radius: 5px; font-family: monospace;">
            <strong>Admin:</strong> admin / admin123<br>
            <strong>Moderator:</strong> moderator / mod123<br>
            <strong>Regular User:</strong> user1 / password123<br>
            <strong>Guest:</strong> guest_user / guest123
        </div>
        
        <h3>🛡️ Educational Purpose Only</h3>
        <p>This lab is designed for cybersecurity education and training. It contains real vulnerabilities for learning purposes.</p>
        
        <p style="text-align: center; margin-top: 30px;">
            <a href="/" style="background: #3742fa; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🚀 Enter Lab Environment</a>
        </p>
    </div>
    """

# Disable caching for all static files to prevent 304 responses
@app.after_request
def after_request(response):
    if request.endpoint == 'static' or '/static/' in request.path:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Initialize database
def init_db():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Users table with enhanced roles and wallet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_active INTEGER DEFAULT 1,
            profile_image TEXT DEFAULT 'default.png',
            phone TEXT,
            address TEXT,
            wallet_balance REAL DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            failed_login_attempts INTEGER DEFAULT 0
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            seller_id INTEGER,
            category TEXT DEFAULT 'Electronics',
            stock_quantity INTEGER DEFAULT 100,
            image_url TEXT,
            is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users (id)
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            coupon_code TEXT,
            discount REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            comment TEXT,
            rating INTEGER DEFAULT 5,
            is_approved INTEGER DEFAULT 1,
            custom_username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Coupons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount_percent REAL NOT NULL,
            usage_limit INTEGER DEFAULT 1,
            used_count INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1,
            expiry_date TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # News/Blog table for additional vulnerabilities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            category TEXT DEFAULT 'General',
            is_published INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Support tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            priority TEXT DEFAULT 'medium',
            assigned_to INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (assigned_to) REFERENCES users (id)
        )
    ''')
    
    # File uploads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            file_type TEXT,
            is_public INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # API keys table for API vulnerabilities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            api_key TEXT UNIQUE NOT NULL,
            permissions TEXT DEFAULT 'read',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Wallet transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallet_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            admin_user_id INTEGER,
            reference_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (admin_user_id) REFERENCES users (id)
        )
    ''')

    # Insert sample data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Insert sample users with different roles and wallet balances
        cursor.execute("INSERT INTO users (username, email, password, role, phone, address, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      ('admin', 'admin@shop.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin', '+1234567890', '123 Admin St', 10000.00))
        cursor.execute("INSERT INTO users (username, email, password, role, phone, address, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      ('moderator', 'mod@shop.com', hashlib.md5('hello'.encode()).hexdigest(), 'moderator', '+1234567891', '456 Mod Ave', 500.00))
        cursor.execute("INSERT INTO users (username, email, password, role, phone, address, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      ('seller1', 'seller@shop.com', hashlib.md5('hello'.encode()).hexdigest(), 'seller', '+1234567892', '789 Seller Rd', 1500.00))
        cursor.execute("INSERT INTO users (username, email, password, role, phone, address, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      ('john_doe', 'john@email.com', hashlib.md5('password123'.encode()).hexdigest(), 'user', '+1234567893', '321 User Blvd', 250.00))
        cursor.execute("INSERT INTO users (username, email, password, role, phone, address, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      ('jane_smith', 'jane@email.com', hashlib.md5('secret456'.encode()).hexdigest(), 'user', '+1234567894', '654 Test Lane', 100.00))
        cursor.execute("INSERT INTO users (username, email, password, role, phone, address, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      ('testuser', 'test@shop.com', hashlib.md5('test'.encode()).hexdigest(), 'user', '+1234567895', '987 Guest Way', 75.50))
        
        # Insert sample products with enhanced details and higher stock
        cursor.execute("INSERT INTO products (name, description, price, stock, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?)", 
                      ('Gaming Laptop Pro', 'High-performance gaming laptop with RTX graphics', 1299.99, 50, 'laptop.jpg', 1))
        cursor.execute("INSERT INTO products (name, description, price, stock, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?)", 
                      ('Smartphone X', 'Latest flagship smartphone with advanced camera', 899.99, 75, 'phone.jpg', 1))
        cursor.execute("INSERT INTO products (name, description, price, stock, image_url) VALUES (?, ?, ?, ?, ?)", 
                      ('Wireless Gaming Mouse', 'RGB gaming mouse with precision tracking', 59.99, 150, 'mouse.jpg'))
        cursor.execute("INSERT INTO products (name, description, price, stock, image_url) VALUES (?, ?, ?, ?, ?)", 
                      ('Premium Headphones', 'Noise-cancelling wireless headphones', 249.99, 100, 'headphones.jpg'))
        cursor.execute("INSERT INTO products (name, description, price, stock, image_url) VALUES (?, ?, ?, ?, ?)", 
                      ('Smart Watch Elite', 'Advanced fitness tracking smart watch', 199.99, 80, 'watch.jpg'))
        
        # Insert sample coupons with creator
        cursor.execute("INSERT INTO coupons (code, discount_percent, usage_limit, created_by) VALUES (?, ?, ?, ?)", 
                      ('SAVE10', 10.0, 100, 1))
        cursor.execute("INSERT INTO coupons (code, discount_percent, usage_limit, created_by) VALUES (?, ?, ?, ?)", 
                      ('WELCOME20', 20.0, 50, 1))
        cursor.execute("INSERT INTO coupons (code, discount_percent, usage_limit, created_by) VALUES (?, ?, ?, ?)", 
                      ('MEGA50', 50.0, 10, 1))
        
        # Insert sample news articles
        cursor.execute("INSERT INTO news (title, content, author_id, category) VALUES (?, ?, ?, ?)", 
                      ('Welcome to SecureShop!', 'We are excited to launch our new secure e-commerce platform with the latest security features.', 1, 'Announcement'))
        cursor.execute("INSERT INTO news (title, content, author_id, category) VALUES (?, ?, ?, ?)", 
                      ('New Products Added', 'Check out our latest collection of electronics and gadgets now available in the store.', 2, 'Products'))
        cursor.execute("INSERT INTO news (title, content, author_id, category) VALUES (?, ?, ?, ?)", 
                      ('Security Update', 'We have implemented additional security measures to protect your data and transactions.', 1, 'Security'))
        
        # Insert sample API keys
        cursor.execute("INSERT INTO api_keys (user_id, api_key, permissions) VALUES (?, ?, ?)", 
                      (1, 'sk_admin_' + hashlib.md5('admin_key'.encode()).hexdigest()[:16], 'admin'))
        cursor.execute("INSERT INTO api_keys (user_id, api_key, permissions) VALUES (?, ?, ?)", 
                      (4, 'sk_user_' + hashlib.md5('user_key'.encode()).hexdigest()[:16], 'read'))
        
        # Insert sample wallet transactions
        cursor.execute("INSERT INTO wallet_transactions (user_id, transaction_type, amount, description, admin_user_id, reference_id) VALUES (?, ?, ?, ?, ?, ?)", 
                      (1, 'credit', 10000.00, 'Initial admin balance', 1, 'INIT_001'))
        cursor.execute("INSERT INTO wallet_transactions (user_id, transaction_type, amount, description, admin_user_id, reference_id) VALUES (?, ?, ?, ?, ?, ?)", 
                      (4, 'credit', 250.00, 'Welcome bonus', 1, 'WELCOME_001'))
        cursor.execute("INSERT INTO wallet_transactions (user_id, transaction_type, amount, description, admin_user_id, reference_id) VALUES (?, ?, ?, ?, ?, ?)", 
                      (5, 'credit', 100.00, 'Registration reward', 1, 'REG_001'))
    
    
    conn.commit()
    conn.close()

# Helper functions
def update_session_balance(user_id):
    """Update wallet balance in session - helper function"""
    if 'user_id' in session and session['user_id'] == user_id:
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT wallet_balance FROM users WHERE id = ?", (user_id,))
        balance = cursor.fetchone()
        if balance:
            session['wallet_balance'] = balance[0]
        conn.close()

# Helper functions for role-based access control
def requires_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect('/login')
            
            conn = sqlite3.connect('vulnerable_shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                session.clear()
                return redirect('/login')
            
            user_role = user[0]
            
            # Role hierarchy: admin > moderator > seller > user > guest
            role_levels = {'guest': 0, 'user': 1, 'seller': 2, 'moderator': 3, 'admin': 4}
            
            if role_levels.get(user_role, 0) < role_levels.get(required_role, 0):
                return "Access Denied: Insufficient privileges", 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_user_role():
    if 'user_id' not in session:
        return 'guest'
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return user[0] if user else 'guest'

@app.route('/')
def home():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE is_featured = 1 OR 1=1 LIMIT 20")
    products = cursor.fetchall()
    
    # Get latest news for homepage
    cursor.execute("SELECT * FROM news WHERE is_published = 1 ORDER BY created_at DESC LIMIT 3")
    news = cursor.fetchall()
    
    conn.close()
    user_role = get_user_role()
    return render_template('home.html', products=products, news=news, user_role=user_role)

# VULNERABILITY 1: SQL Injection in login with debug output
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Vulnerable SQL query - direct string concatenation
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        # MD5 hash for password comparison
        password_hash = hashlib.md5(password.encode()).hexdigest() if password else ''
        
        # VULNERABLE: SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                # Update last login and reset failed attempts
                cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP, failed_login_attempts = 0 WHERE id = ?", (user[0],))
                conn.commit()
                
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['user_role'] = user[4]  # role is at index 4 in new schema
                session['role'] = user[4]  # Also set 'role' for template compatibility
                session['wallet_balance'] = user[6] if len(user) > 6 else 200.0  # wallet_balance is at index 6
                conn.close()
                
                # Role-based redirect
                if user[4] == 'admin':
                    return redirect('/admin')
                elif user[4] == 'moderator':
                    return redirect('/moderator')
                elif user[4] == 'seller':
                    return redirect('/seller_dashboard')
                else:
                    return redirect('/dashboard')
            else:
                # Increment failed login attempts
                cursor.execute(f"UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE username = '{username}'")
                conn.commit()
                conn.close()
                return render_template('login.html', error='Invalid credentials')
                
        except Exception as e:
            # VULNERABILITY: Expose SQL errors in debug mode
            conn.close()
            return render_template('login.html', error=f'Database Error (Debug Mode): {str(e)}', debug_query=query)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_seller = 1 if request.form.get('is_seller') else 0
        
        if not password:
            return render_template('register.html', error='Password is required')
            
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, email, password, role, wallet_balance, failed_login_attempts, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                          (username, email, password_hash, 'user', 200.0, 0, 1))
            conn.commit()
            
            # Create welcome transaction record
            user_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO wallet_transactions (user_id, amount, transaction_type, description)
                VALUES (?, ?, ?, ?)
            """, (user_id, 200.0, 'credit', 'Welcome bonus for new user'))
            
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='Username already exists')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get user's orders
    cursor.execute("SELECT o.*, p.name FROM orders o JOIN products p ON o.product_id = p.id WHERE o.user_id = ?", 
                   (session['user_id'],))
    orders = cursor.fetchall()
    
    conn.close()
    return render_template('dashboard.html', orders=orders)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    # VULNERABILITY 2: XSS in comments - no sanitization
    # VULNERABILITY: BAC - Display custom username if provided (allows impersonation)
    cursor.execute("""
        SELECT c.*, 
               CASE 
                   WHEN c.custom_username IS NOT NULL AND c.custom_username != '' 
                   THEN c.custom_username 
                   ELSE u.username 
               END as display_username,
               u.role
        FROM comments c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.product_id = ?
        ORDER BY c.created_at DESC
    """, (product_id,))
    comments = cursor.fetchall()
    
    conn.close()
    return render_template('product.html', product=product, comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    """
    VULNERABILITY: Broken Access Control (BAC) in comments
    - Users can impersonate other users including admin
    - No validation of username parameter
    - Trust client-side data for user identity
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product_id = request.form.get('product_id')
    comment = request.form.get('comment')  # VULNERABLE: No XSS filtering
    
    # VULNERABILITY: BAC - Accept username from client without validation
    # Users can manipulate this to post as any user including admin
    impersonated_username = request.form.get('username', '')
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    if impersonated_username:
        # VULNERABLE: Trust the username provided by client
        # Check if this username exists (but still allow impersonation)
        cursor.execute("SELECT id, role FROM users WHERE username = ?", (impersonated_username,))
        impersonated_user = cursor.fetchone()
        
        if impersonated_user:
            # Use the impersonated user's ID
            comment_user_id = impersonated_user[0]
            user_role = impersonated_user[1]
            
            # Log the impersonation attempt (but still allow it)
            print(f"[SECURITY ALERT] User {session['user_id']} attempting to post as {impersonated_username} (role: {user_role})")
        else:
            # If username doesn't exist, create a fake entry or use session user
            comment_user_id = session['user_id']
            print(f"[INFO] Username {impersonated_username} not found, using session user")
    else:
        # No impersonation attempt, use session user
        comment_user_id = session['user_id']
    
    # Insert comment with potentially impersonated user ID
    cursor.execute("INSERT INTO comments (product_id, user_id, comment) VALUES (?, ?, ?)", 
                   (product_id, comment_user_id, comment))
    conn.commit()
    
    # Additional vulnerability: Store the attempted username for display
    if impersonated_username:
        # Store custom username in a separate field for display purposes
        cursor.execute("UPDATE comments SET custom_username = ? WHERE id = ?", 
                      (impersonated_username, cursor.lastrowid))
        conn.commit()
    
    conn.close()
    
    return redirect(url_for('product_detail', product_id=product_id))

# Cart functionality - Amazon-like shopping experience
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add item to shopping cart"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add or update item in cart
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity
    
    flash(f'Added {quantity} item(s) to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
def view_cart():
    """View shopping cart"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', cart_items=[], total_price=0)
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    cart_items = []
    total_price = 0
    
    for product_id, quantity in session['cart'].items():
        cursor.execute("SELECT id, name, price, stock FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if product:
            item_total = product[2] * quantity
            cart_items.append({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'quantity': quantity,
                'item_total': item_total,
                'in_stock': product[3] >= quantity
            })
            total_price += item_total
    
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'cart' in session and str(product_id) in session['cart']:
        del session['cart'][str(product_id)]
        flash('Item removed from cart!', 'info')
    
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page with coupon application"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('view_cart'))
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get cart items with product details
    cart_items = []
    total_price = 0
    
    for product_id, quantity in session['cart'].items():
        cursor.execute("SELECT id, name, price, stock FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if product:
            if product[3] < quantity:
                flash(f'Insufficient stock for {product[1]}. Only {product[3]} available.', 'danger')
                conn.close()
                return redirect(url_for('view_cart'))
            
            item_total = product[2] * quantity
            cart_items.append({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'quantity': quantity,
                'item_total': item_total
            })
            total_price += item_total
    
    # Get user's wallet balance
    cursor.execute("SELECT wallet_balance FROM users WHERE id = ?", (session['user_id'],))
    user_balance = cursor.fetchone()[0]
    
    # Get available coupons
    cursor.execute("SELECT code, discount_percent, used_count, usage_limit FROM coupons WHERE active = 1")
    available_coupons = cursor.fetchall()
    
    conn.close()
    
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         total_price=total_price,
                         user_balance=user_balance,
                         available_coupons=available_coupons)

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    """Apply coupon and show discounted price"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('view_cart'))
    
    coupon_code = request.form.get('coupon_code', '').strip().upper()
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Calculate original total
    total_price = 0
    cart_items = []
    
    for product_id, quantity in session['cart'].items():
        cursor.execute("SELECT id, name, price, stock FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if product:
            item_total = product[2] * quantity
            cart_items.append({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'quantity': quantity,
                'item_total': item_total
            })
            total_price += item_total
    
    # Get user's wallet balance
    cursor.execute("SELECT wallet_balance FROM users WHERE id = ?", (session['user_id'],))
    user_balance = cursor.fetchone()[0]
    
    # Get available coupons
    cursor.execute("SELECT code, discount_percent, used_count, usage_limit FROM coupons WHERE active = 1")
    available_coupons = cursor.fetchall()
    
    # VULNERABLE: Business Logic Flaw + Race Condition in Coupon Application
    # Validate and apply coupon with FLAWED CALCULATION + RACE CONDITION
    discount = 0
    applied_coupon = None
    coupon_message = ""
    
    if coupon_code:
        # RACE CONDITION VULNERABILITY: Check coupon without proper locking
        cursor.execute("SELECT * FROM coupons WHERE code = ? AND active = 1", (coupon_code,))
        coupon = cursor.fetchone()
        
        if coupon:
            # RACE CONDITION: Time gap between check and discount application
            import time
            import threading
            thread_id = threading.current_thread().ident
            print(f"[APPLY-RACE-DEBUG] Thread {thread_id}: Starting coupon application for {coupon_code}")
            
            # VULNERABILITY: 300ms delay creates race condition window for apply_coupon
            time.sleep(0.3)  # Larger window for apply_coupon exploitation
            
            print(f"[APPLY-RACE-DEBUG] Thread {thread_id}: Coupon {coupon_code} usage: {coupon[4]}/{coupon[3]}")
            
            if coupon[3] > coupon[4]:  # usage_limit > used_count
                # Store original usage count before business logic calculation
                original_usage = coupon[4]
                
                # BUSINESS LOGIC FLAW 1: Incorrect discount calculation
                # Instead of applying discount to total, it applies discount incorrectly
                
                if coupon_code == 'SAVE10':
                    # FLAW: Instead of 10% off, calculate as 10% + bonus
                    base_discount = total_price * (coupon[2] / 100)  # Normal 10%
                    bonus_discount = total_price * 0.05  # Extra 5% due to "calculation error"
                    discount = base_discount + bonus_discount  # 15% total instead of 10%
                    
                elif coupon_code == 'MEGA50':
                    # FLAW: Instead of 50% off, calculate as 50% + item count bonus
                    base_discount = total_price * (coupon[2] / 100)  # Normal 50%
                    item_bonus = len(cart_items) * 10  # $10 bonus per item type
                    discount = base_discount + item_bonus
                    
                elif coupon_code == 'WELCOME5':
                    # FLAW: Treat 5% as $50 off each item type instead of 5% total
                    discount = len(cart_items) * 50  # $50 off per different item type
                    
                else:
                    # FLAW: For any other coupon, double the discount percentage
                    discount = total_price * (coupon[2] / 50)  # Double the discount rate
                
                # Additional FLAW: If discount exceeds total, make item free
                if discount > total_price:
                    discount = total_price  # Free items!
                
                applied_coupon = coupon
                
                # RACE CONDITION VULNERABILITY: Store applied discount in session for race condition exploitation
                # Multiple concurrent requests can stack discounts
                if 'applied_discounts' not in session:
                    session['applied_discounts'] = []
                
                # Add this discount to the session (vulnerable to race condition)
                session['applied_discounts'].append({
                    'coupon_code': coupon_code,
                    'discount': discount,
                    'thread_id': thread_id
                })
                
                # Calculate total discount from all concurrent applications
                total_stacked_discount = sum(d['discount'] for d in session['applied_discounts'])
                if total_stacked_discount > total_price:
                    total_stacked_discount = total_price  # Cap at total price
                
                coupon_message = f"✅ Coupon '{coupon_code}' applied! You save ${discount:.2f} ({(discount/total_price*100):.1f}% off)"
                
                # Show race condition exploitation if multiple discounts applied
                if len(session['applied_discounts']) > 1:
                    coupon_message += f" | 🚨 RACE CONDITION: {len(session['applied_discounts'])} applications = ${total_stacked_discount:.2f} total!"
                    discount = total_stacked_discount  # Use stacked discount
                
                print(f"[BUSINESS-LOGIC-FLAW] Applied flawed discount calculation:")
                print(f"[FLAW] Coupon: {coupon_code}")
                print(f"[FLAW] Expected discount: ${total_price * (coupon[2] / 100):.2f}")
                print(f"[FLAW] ACTUAL discount: ${discount:.2f}")
                print(f"[FLAW] Extra savings: ${discount - (total_price * (coupon[2] / 100)):.2f}")
                print(f"[APPLY-RACE-DEBUG] Thread {thread_id}: Applied discounts in session: {len(session['applied_discounts'])}")
                
                # VULNERABLE: Non-atomic increment allows multiple coupon counting
                cursor.execute("UPDATE coupons SET used_count = used_count + 1 WHERE code = ?", (coupon_code,))
                conn.commit()  # Commit the usage count increase
                
            else:
                coupon_message = f"❌ Coupon '{coupon_code}' has reached its usage limit"
        else:
            coupon_message = f"❌ Invalid coupon code: '{coupon_code}'"
    
    final_price = total_price - discount
    
    conn.close()
    
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         total_price=total_price,
                         discount=discount,
                         final_price=final_price,
                         applied_coupon=applied_coupon,
                         coupon_code=coupon_code,
                         coupon_message=coupon_message,
                         user_balance=user_balance,
                         available_coupons=available_coupons)

# VULNERABILITY 3: Business Logic Flaw - Coupon Mass Abuse
@app.route('/purchase', methods=['POST'])
def purchase():
    """Process cart checkout with coupon application"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if cart exists and has items
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('view_cart'))
    
    coupon_code = request.form.get('coupon_code', '')
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Calculate total price and validate stock
    cart_items = []
    total_price = 0
    
    for product_id, quantity in session['cart'].items():
        cursor.execute("SELECT id, name, price, stock FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            flash('Some items in your cart are no longer available', 'danger')
            return redirect(url_for('view_cart'))
        
        # Check stock availability
        if product[3] < quantity:
            conn.close()
            flash(f'Insufficient stock for {product[1]}! Only {product[3]} items available', 'danger')
            return redirect(url_for('view_cart'))
        
        item_total = product[2] * quantity
        cart_items.append({
            'id': product[0],
            'name': product[1], 
            'price': product[2],
            'quantity': quantity,
            'stock': product[3]
        })
        total_price += item_total
    
    # Get user's current wallet balance
    cursor.execute("SELECT wallet_balance FROM users WHERE id = ?", (session['user_id'],))
    user_balance = cursor.fetchone()
    
    if not user_balance:
        conn.close()
        flash('User account error', 'danger')
        return redirect(url_for('home'))
    
    current_balance = user_balance[0]
    original_total = total_price
    discount = 0
    
    # VULNERABLE: Business Logic Flaw - Use session-stored race condition discounts
    if coupon_code:
        # Check if there are stacked discounts from apply_coupon race condition
        if 'applied_discounts' in session and session['applied_discounts']:
            print(f"[PURCHASE-RACE] Found {len(session['applied_discounts'])} stacked discounts in session")
            
            # Use the total stacked discount from apply_coupon race condition
            discount = sum(d['discount'] for d in session['applied_discounts'])
            if discount > original_total:
                discount = original_total  # Cap at total price (free items!)
            
            total_price = original_total - discount
            
            print(f"[PURCHASE-RACE] Using stacked race condition discount: ${discount:.2f}")
            print(f"[PURCHASE-RACE] Original: ${original_total:.2f} → Final: ${total_price:.2f}")
            
            # Clear the session discounts after use
            session['applied_discounts'] = []
            
        else:
            # Fallback to normal coupon processing if no race condition discounts
            # VULNERABILITY 1: Check coupon without proper locking
            cursor.execute("SELECT discount_percent, used_count, usage_limit FROM coupons WHERE code = ? AND active = 1", 
                           (coupon_code,))
            coupon = cursor.fetchone()
            
            if coupon:
                discount_percent, current_usage, usage_limit = coupon
                
                # VULNERABILITY 2: Time gap between check and update creates race condition window
                import time
                import threading
                thread_id = threading.current_thread().ident
                print(f"[RACE-DEBUG] Thread {thread_id}: Starting coupon processing for {coupon_code}")
                
                time.sleep(0.2)  # 200ms delay - LARGER window for race condition
                
                print(f"[RACE-DEBUG] Thread {thread_id}: Coupon {coupon_code}: Current usage {current_usage}/{usage_limit}")
                
                # BUSINESS LOGIC FLAW: Apply same flawed discount calculation as in apply_coupon
                if coupon_code == 'SAVE10':
                    base_discount = total_price * (discount_percent / 100)  # Normal 10%
                    bonus_discount = total_price * 0.05  # Extra 5% due to "calculation error"
                    discount = base_discount + bonus_discount  # 15% total instead of 10%
                    
                elif coupon_code == 'MEGA50':
                    base_discount = total_price * (discount_percent / 100)  # Normal 50%
                    item_bonus = len(cart_items) * 10  # $10 bonus per item type
                    discount = base_discount + item_bonus
                    
                elif coupon_code == 'WELCOME5':
                    # Treat 5% as $50 off each item type instead of 5% total
                    discount = len(cart_items) * 50  # $50 off per different item type
                    
                else:
                    # For any other coupon, double the discount percentage
                    discount = total_price * (discount_percent / 50)  # Double the discount rate
                
                # If discount exceeds total, make item free
                if discount > total_price:
                    discount = total_price  # Free items!
                
                total_price -= discount
                
                print(f"[BUSINESS-LOGIC-FLAW] Applied flawed discount in purchase:")
                print(f"[FLAW] Expected discount: ${original_total * (discount_percent / 100):.2f}")
                print(f"[FLAW] ACTUAL discount: ${discount:.2f}")
                print(f"[RACE-DEBUG] Thread {thread_id}: DISCOUNT APPLIED! ${discount:.2f} (FLAWED CALCULATION)")
                
                # VULNERABILITY 4: Non-atomic increment allows multiple applications
                cursor.execute("UPDATE coupons SET used_count = used_count + 1 WHERE code = ?", (coupon_code,))
                
            else:
                print(f"[DEBUG] Coupon {coupon_code} not found or inactive")    # Check if user has sufficient balance
    if current_balance < total_price:
        conn.close()
        flash(f'Insufficient funds! You have ${current_balance:.2f} but need ${total_price:.2f}', 'danger')
        return redirect(url_for('checkout'))
    
    try:
        # Deduct money from user's wallet
        new_balance = current_balance - total_price
        cursor.execute("UPDATE users SET wallet_balance = ? WHERE id = ?", (new_balance, session['user_id']))
        
        # Update session balance
        session['wallet_balance'] = new_balance
        
        new_balance = current_balance - total_price
        cursor.execute("UPDATE users SET wallet_balance = ? WHERE id = ?", (new_balance, session['user_id']))
        
        # Update session balance
        session['wallet_balance'] = new_balance
        
        # Create wallet transaction record
        cart_description = f"Cart purchase ({len(cart_items)} items)"
        if coupon_code:
            cart_description += f" with {coupon_code} coupon"
            
        cursor.execute("""
            INSERT INTO wallet_transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, ?, ?)
        """, (session['user_id'], -total_price, 'debit', cart_description))
        
        # Process each item in cart - update stock and create orders
        order_ids = []
        for item in cart_items:
            # Update product stock
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", 
                          (item['quantity'], item['id']))
            
            # Create individual order for each product (maintaining original structure)
            item_total = item['price'] * item['quantity']
            # Apply proportional discount if coupon was used
            item_discount = (discount * item_total / original_total) if discount > 0 else 0
            item_final_price = item_total - item_discount
            
            cursor.execute("""
                INSERT INTO orders (user_id, product_id, quantity, total_price, promo_code, discount) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session['user_id'], item['id'], item['quantity'], item_final_price, coupon_code, item_discount))
            
            order_ids.append(cursor.lastrowid)
        
        # Clear the cart after successful purchase
        session['cart'] = {}
        
        conn.commit()
        conn.close()
        
        flash(f'Purchase successful! ${total_price:.2f} deducted from your wallet. New balance: ${new_balance:.2f}', 'success')
        
        # Redirect to receipt for first order (or could create a summary page)
        return redirect(url_for('receipt', order_id=order_ids[0]))
        
    except Exception as e:
        conn.rollback()
        conn.close()
        flash(f'Purchase failed: {str(e)}', 'danger')
        return redirect(url_for('checkout'))

# VULNERABILITY 4: IDOR in purchase receipt
@app.route('/receipt/<int:order_id>')
def receipt(order_id):
    # VULNERABLE: No access control - any user can access any receipt
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT o.*, p.name, u.username, u.email 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        JOIN users u ON o.user_id = u.id 
        WHERE o.id = ?
    """, (order_id,))
    
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        return "Receipt not found", 404
    
    return render_template('receipt.html', order=order)

# VULNERABILITY 5: CSRF in password change
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # VULNERABLE: No CSRF protection
        new_password = request.form.get('new_password')
        
        if not new_password:
            return render_template('change_password.html', error='New password is required')
            
        new_password_hash = hashlib.md5(new_password.encode()).hexdigest()
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", 
                       (new_password_hash, session['user_id']))
        conn.commit()
        conn.close()
        
        return render_template('change_password.html', success='Password changed successfully!')
    
    return render_template('change_password.html')

# VULNERABILITY 6: Directory Traversal
@app.route('/download/<path:filename>')
def download_file(filename):
    # VULNERABLE: No path sanitization - allows directory traversal
    try:
        # This allows ../../../etc/passwd type attacks
        file_path = os.path.join('uploads', filename)
        print(f"DEBUG: Attempting to access file: {file_path}")
        print(f"DEBUG: Absolute path: {os.path.abspath(file_path)}")
        return send_file(file_path)
    except Exception as e:
        print(f"DEBUG: Error accessing file: {str(e)}")
        return f"Error: {str(e)}", 404

# VULNERABILITY 6b: Alternative Directory Traversal Route
@app.route('/files')
@app.route('/files/')
def list_root_files():
    """VULNERABLE: Lists all files in the current directory"""
    try:
        files = os.listdir('.')
        html = "<h1>Root Directory Listing</h1><ul>"
        
        def should_hide_file(filename):
            """Hide .md, .txt, .py files except app.py, and testing scripts"""
            if filename == 'app.py':
                return False
            # Hide testing scripts and related files
            if 'test' in filename.lower():
                return True
            if filename.startswith(('pytest', 'SQLI_WORKING_PROOF')):
                return True
            return filename.endswith(('.md', '.txt', '.py'))
        
        for file in files:
            if should_hide_file(file):
                continue
                
            if os.path.isfile(file):
                html += f"<li><a href='/files/{file}'>{file}</a> (file)</li>"
            elif os.path.isdir(file):
                html += f"<li><a href='/files/{file}/'>{file}/</a> (directory)</li>"
        html += "</ul>"
        return html
    except Exception as e:
        return f"Error listing directory: {str(e)}", 404

@app.route('/files/<path:filename>')
def get_file(filename):
    # EXTREMELY VULNERABLE: Direct file access without any restrictions
    try:
        print(f"DEBUG: Accessing file directly: {filename}")
        
        def should_hide_file(filename):
            """Hide .md, .txt, .py files except app.py, and testing scripts"""
            if filename == 'app.py':
                return False
            # Hide testing scripts and related files
            if 'test' in filename.lower():
                return True
            if filename.startswith(('pytest', 'SQLI_WORKING_PROOF')):
                return True
            return filename.endswith(('.md', '.txt', '.py'))
        
        # If it's a directory, list its contents
        if os.path.isdir(filename):
            files = os.listdir(filename)
            html = f"<h1>Directory Listing: /{filename}</h1><ul>"
            for file in files:
                if should_hide_file(file):
                    continue
                    
                file_path = os.path.join(filename, file)
                if os.path.isfile(file_path):
                    html += f"<li><a href='/files/{file_path}'>{file}</a> (file)</li>"
                elif os.path.isdir(file_path):
                    html += f"<li><a href='/files/{file_path}/'>{file}/</a> (directory)</li>"
            html += "</ul>"
            return html
        else:
            # If it's a file, serve it
            return send_file(filename)
    except Exception as e:
        print(f"DEBUG: Error: {str(e)}")
        return f"File not found: {str(e)}", 404

# VULNERABILITY 6c: Directory Listing Vulnerability
@app.route('/static/images')
@app.route('/static/images/')
def list_static_images():
    """VULNERABLE: Lists all files in the static/images directory"""
    try:
        files = os.listdir('static/images')
        html = "<h1>Static Images Directory Listing</h1><ul>"
        for file in files:
            html += f"<li><a href='/static/images/{file}'>{file}</a></li>"
        html += "</ul>"
        return html
    except Exception as e:
        return f"Error listing directory: {str(e)}", 404

@app.route('/static/images/<path:subpath>')
def serve_static_or_list(subpath):
    """VULNERABLE: Serves files or lists directories with directory traversal"""
    try:
        full_path = os.path.join('static/images', subpath)
        
        # If it's a directory, list contents
        if os.path.isdir(full_path):
            files = os.listdir(full_path)
            html = f"<h1>Directory Listing: /static/images/{subpath}</h1><ul>"
            for file in files:
                file_path = os.path.join(subpath, file)
                html += f"<li><a href='/static/images/{file_path}'>{file}</a></li>"
            html += "</ul>"
            return html
        else:
            # If it's a file, serve it with no-cache headers
            response = make_response(send_file(full_path))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
    except Exception as e:
        return f"Error: {str(e)}", 404

@app.route('/images')
def list_images():
    """VULNERABLE: Lists all files in the images directory"""
    try:
        files = os.listdir('static/images')
        html = "<h1>Image Directory Listing</h1><ul>"
        for file in files:
            html += f"<li><a href='/static/images/{file}'>{file}</a></li>"
        html += "</ul>"
        return html
    except Exception as e:
        return f"Error listing directory: {str(e)}", 404

@app.route('/images/<path:subdir>')
def list_directory(subdir):
    """VULNERABLE: Lists any directory contents"""
    try:
        dir_path = os.path.join('static/images', subdir)
        files = os.listdir(dir_path)
        html = f"<h1>Directory Listing: {subdir}</h1><ul>"
        for file in files:
            file_path = os.path.join(subdir, file)
            html += f"<li><a href='/static/images/{file_path}'>{file}</a></li>"
        html += "</ul>"
        return html
    except Exception as e:
        return f"Error listing directory: {str(e)}", 404

# VULNERABILITY: Simple Directory Traversal Test  
@app.route('/read/<path:filepath>')
def read_any_file(filepath):
    """EXTREMELY VULNERABLE: Read any file on the system"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"Error reading file: {str(e)}", 404

# VULNERABILITY 7: SSRF (Server-Side Request Forgery)
@app.route('/check_url', methods=['POST'])
def check_url():
    url = request.form.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'})

# VULNERABILITY 7b: SSRF via Stock Check API
@app.route('/check_stock_api', methods=['POST'])
def check_stock_api():
    """
    VULNERABLE: SSRF via external stock checking API
    This endpoint allows checking stock from external inventory systems
    but doesn't validate the URL, allowing SSRF attacks
    """
    api_url = request.form.get('stock_api_url', '').strip()
    product_id = request.form.get('product_id')
    
    if not api_url:
        return jsonify({'error': 'Stock API URL required', 'stock': 0})
    
    if not product_id:
        return jsonify({'error': 'Product ID required', 'stock': 0})
    
    try:
        # VULNERABLE: No URL validation allows SSRF
        # Attacker can redirect to internal services, webhooks, etc.
        print(f"[SSRF] Attempting to fetch stock from: {api_url}")
        
        # Construct the API request - vulnerable to manipulation
        if '?' in api_url:
            full_url = f"{api_url}&product_id={product_id}"
        else:
            full_url = f"{api_url}?product_id={product_id}"
        
        print(f"[SSRF] Full URL: {full_url}")
        
        # Make the SSRF request - no restrictions
        import requests
        response = requests.get(full_url, timeout=10, allow_redirects=True)
        
        print(f"[SSRF] Response Status: {response.status_code}")
        print(f"[SSRF] Response Headers: {dict(response.headers)}")
        
        # Try to parse JSON response for stock count
        try:
            data = response.json()
            stock_count = data.get('stock', data.get('quantity', data.get('available', 0)))
            
            return jsonify({
                'success': True,
                'stock': stock_count,
                'api_response': data,
                'status_code': response.status_code
            })
        except:
            # If not JSON, try to extract numbers from response
            import re
            numbers = re.findall(r'\d+', response.text)
            stock_count = int(numbers[0]) if numbers else 0
            
            return jsonify({
                'success': True, 
                'stock': stock_count,
                'api_response': response.text[:500],  # First 500 chars
                'status_code': response.status_code
            })
            
    except requests.exceptions.RequestException as e:
        print(f"[SSRF] Request failed: {str(e)}")
        return jsonify({
            'error': f'Stock API request failed: {str(e)}',
            'stock': 0
        })
    except Exception as e:
        print(f"[SSRF] Unexpected error: {str(e)}")
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'stock': 0
        })

@app.route('/stock_checker')
def stock_checker():
    """Admin page for configuring external stock API endpoints"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    return render_template('stock_checker.html')
    
    try:
        # VULNERABLE: No URL validation - allows SSRF attacks
        response = requests.get(url, timeout=10)
        return jsonify({
            'status_code': response.status_code,
            'content': response.text[:1000],  # Limit response size
            'headers': dict(response.headers)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# VULNERABILITY 8: SSTI (Server-Side Template Injection)
@app.route('/render_template', methods=['GET', 'POST'])
def render_custom_template():
    if request.method == 'POST':
        template_content = request.form.get('template')
        user_name = request.form.get('name', 'Guest')
        
        # VULNERABLE: Direct template rendering without sanitization
        try:
            if not template_content:
                return render_template('ssti_result.html', error='Template content is required')
                
            template = Template(template_content)
            rendered = template.render(name=user_name, session=session)
            return render_template('ssti_result.html', result=rendered)
        except Exception as e:
            return render_template('ssti_result.html', error=str(e))
    
    return render_template('ssti_form.html')

# VULNERABILITY 9: Insecure Deserialization
@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    preferences = {
        'theme': request.form.get('theme', 'light'),
        'notifications': request.form.get('notifications') == 'on',
        'user_id': session['user_id']
    }
    
    # VULNERABLE: Insecure serialization
    serialized = base64.b64encode(pickle.dumps(preferences)).decode()
    
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('preferences', serialized)
    return response

@app.route('/load_preferences')
def load_preferences():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    prefs_cookie = request.cookies.get('preferences')
    if prefs_cookie:
        try:
            # VULNERABLE: Insecure deserialization
            preferences = pickle.loads(base64.b64decode(prefs_cookie))
            return jsonify(preferences)
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return jsonify({'error': 'No preferences found'})

# VULNERABILITY: Search with SQL Injection, XSS, and SSTI
@app.route('/search')
def search():
    """
    VULNERABILITY: Redirect search to autocomplete API for easier SQL injection
    """
    query = request.args.get('q', '')
    
    if not query:
        return render_template('search_results.html', products=[], query='', message="Please enter a search term")
    
    # Redirect to autocomplete API for SQL injection
    from flask import redirect, url_for
    return redirect(url_for('search_autocomplete') + f'?term={query}')

@app.route('/api/search_autocomplete')
def search_autocomplete():
    """
    VULNERABILITY: XSS and SQL Injection in autocomplete
    """
    term = request.args.get('term', '')
    
    if len(term) < 2:
        return jsonify([])
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: SQL Injection in autocomplete
    query = f"SELECT DISTINCT name FROM products WHERE name LIKE '%{term}%' LIMIT 10"
    
    try:
        cursor.execute(query)
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # VULNERABILITY: XSS in JSON response
        return jsonify(results)  # No XSS protection
    except:
        conn.close()
        return jsonify([])

# VULNERABILITY 10: Command Injection
@app.route('/ping', methods=['POST'])
def ping_host():
    host = request.form.get('host')
    
    if not host:
        return jsonify({'error': 'No host provided'})
    
    # VULNERABLE: Command injection
    try:
        result = subprocess.run(f"ping -c 4 {host}", shell=True, capture_output=True, text=True)
        return jsonify({
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# VULNERABILITY 11: Local File Inclusion (LFI)
@app.route('/view_file')
def view_file():
    file_param = request.args.get('file', 'default.txt')
    
    # VULNERABLE: No input validation for file parameter
    try:
        with open(file_param, 'r') as f:
            content = f.read()
        return render_template('file_viewer.html', filename=file_param, content=content)
    except Exception as e:
        return render_template('file_viewer.html', filename=file_param, error=str(e))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    """User profile page - VULNERABLE: Missing authentication check"""
    if 'username' not in session:
        flash('Please log in to access your profile.', 'danger')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (session['username'],))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return render_template('profile.html', user=user)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Update user profile - VULNERABLE: Weak validation"""
    if 'username' not in session:
        flash('Please log in to update your profile.', 'danger')
        return redirect(url_for('login'))
    
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Verify current password
    cursor.execute("SELECT password FROM users WHERE username = ?", (session['username'],))
    stored_password = cursor.fetchone()
    
    if not stored_password or not current_password or hashlib.md5(current_password.encode()).hexdigest() != stored_password[0]:
        flash('Current password is incorrect.', 'danger')
        conn.close()
        return redirect(url_for('profile'))
    
    # Update email
    if email:
        cursor.execute("UPDATE users SET email = ? WHERE username = ?", (email, session['username']))
    
    # Update password if provided
    if new_password:
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            conn.close()
            return redirect(url_for('profile'))
        
        hashed_password = hashlib.md5(new_password.encode()).hexdigest()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, session['username']))
    
    conn.commit()
    conn.close()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

# Additional vulnerable endpoints for comprehensive testing
@app.route('/admin')
@requires_role('admin')
def admin_panel():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get user statistics
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total_price) FROM orders")
    total_revenue_result = cursor.fetchone()[0]
    total_revenue = total_revenue_result if total_revenue_result else 0
    
    # Get all users for management
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    # Get all orders
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin.html', 
                         users=users, 
                         orders=orders,
                         total_users=total_users,
                         total_products=total_products, 
                         total_orders=total_orders,
                         total_revenue=total_revenue)

# VULNERABILITY 12: Admin User Management with IDOR
@app.route('/admin/users')
@requires_role('admin')
def admin_users():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, is_active, created_at, last_login, failed_login_attempts FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    
    return render_template('admin_users.html', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@requires_role('admin')
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        
        if not all([username, email, password]):
            return render_template('add_user.html', error='All fields are required')
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            return render_template('add_user.html', error='User already exists')
        
        # VULNERABLE: No password strength validation
        password_hash = hashlib.md5(password.encode()).hexdigest() if password else ''
        
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password, role, phone, address) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, role, phone, address))
            conn.commit()
            conn.close()
            return redirect('/admin/users')
        except Exception as e:
            conn.close()
            return render_template('add_user.html', error=f'Error creating user: {str(e)}')
    
    return render_template('add_user.html')

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@requires_role('admin')
def edit_user(user_id):
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        is_active = 1 if request.form.get('is_active') == 'on' else 0
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        
        # VULNERABLE: IDOR - Direct object reference without proper authorization check
        cursor.execute("""
            UPDATE users SET username=?, email=?, role=?, is_active=?, phone=?, address=? 
            WHERE id=?
        """, (username, email, role, is_active, phone, address, user_id))
        
        conn.commit()
        conn.close()
        return redirect('/admin/users')
    
    # Get user details
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return "User not found", 404
    
    return render_template('edit_user.html', user=user)

@app.route('/moderator')
@requires_role('moderator')
def moderator():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get pending content for moderation
    cursor.execute("SELECT * FROM comments WHERE is_approved = 0 ORDER BY created_at DESC")
    pending_comments = cursor.fetchall()
    
    cursor.execute("SELECT * FROM support_tickets WHERE status = 'open' ORDER BY created_at DESC")
    open_tickets = cursor.fetchall()
    
    conn.close()
    
    return render_template('moderator.html', 
                         pending_comments=pending_comments,
                         open_tickets=open_tickets)

@app.route('/seller_dashboard')
@requires_role('seller')
def seller_dashboard():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get seller's products and orders
    cursor.execute("SELECT * FROM products WHERE seller_id = ?", (session['user_id'],))
    products = cursor.fetchall()
    
    cursor.execute("""
        SELECT o.*, p.name as product_name 
        FROM orders o 
        JOIN products p ON o.product_id = p.id 
        WHERE p.seller_id = ? 
        ORDER BY o.order_date DESC
    """, (session['user_id'],))
    orders = cursor.fetchall()
    
    conn.close()
    
    return render_template('seller_dashboard.html', products=products, orders=orders)

# News/Blog section with XSS vulnerabilities
@app.route('/news')
def news():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE is_published = 1 ORDER BY created_at DESC")
    articles = cursor.fetchall()
    conn.close()
    
    return render_template('news.html', articles=articles)

# VULNERABILITY: Weak authentication for wallet management
@app.route('/wallet')
def wallet():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get user wallet info
    cursor.execute("SELECT username, wallet_balance, role FROM users WHERE id = ?", (session['user_id'],))
    user_info = cursor.fetchone()
    
    # Get recent transactions
    cursor.execute("""
        SELECT wt.*, u.username as admin_username 
        FROM wallet_transactions wt
        LEFT JOIN users u ON wt.admin_user_id = u.id
        WHERE wt.user_id = ? 
        ORDER BY wt.created_at DESC 
        LIMIT 20
    """, (session['user_id'],))
    transactions = cursor.fetchall()
    
    conn.close()
    
    return render_template('wallet.html', user_info=user_info, transactions=transactions)

# VULNERABILITY: Hidden admin wallet management with weak authentication
@app.route('/admin/wallet')
@requires_role('admin')
def admin_wallet():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Get all users with wallet info
    cursor.execute("SELECT id, username, role, wallet_balance, created_at FROM users ORDER BY wallet_balance DESC")
    users = cursor.fetchall()
    
    # Get recent transactions
    cursor.execute("""
        SELECT wt.*, u1.username as user_name, u2.username as admin_name
        FROM wallet_transactions wt
        LEFT JOIN users u1 ON wt.user_id = u1.id
        LEFT JOIN users u2 ON wt.admin_user_id = u2.id
        ORDER BY wt.created_at DESC 
        LIMIT 50
    """)
    all_transactions = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin_wallet.html', users=users, transactions=all_transactions)

@app.route('/admin/add_money', methods=['POST'])
@requires_role('admin')
def admin_add_money():
    """Admin function to add money to user wallets"""
    user_id = request.form.get('user_id')
    amount = request.form.get('amount')
    
    if not user_id or not amount:
        flash('User ID and amount are required', 'danger')
        return redirect(url_for('admin_wallet'))
    
    try:
        user_id = int(user_id)
        amount = float(amount)
        
        if amount <= 0:
            flash('Amount must be positive', 'danger')
            return redirect(url_for('admin_wallet'))
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        # Update user balance
        cursor.execute("UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?", (amount, user_id))
        
        # Record transaction
        cursor.execute("""
            INSERT INTO wallet_transactions (user_id, amount, transaction_type, description, admin_id)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, amount, 'credit', f'Admin credit by {session.get("username")}', session.get('user_id')))
        
        conn.commit()
        conn.close()
        
        # Update session balance if it's the current user
        update_session_balance(user_id)
        
        flash(f'Successfully added ${amount:.2f} to user account', 'success')
        
    except ValueError:
        flash('Invalid user ID or amount', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('admin_wallet'))

# VULNERABILITY: Weak authentication - accessible via URL manipulation
@app.route('/secret_add_money', methods=['GET', 'POST'])
def secret_add_money():
    # VULNERABLE: Only checks if user exists, not if they're admin
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        target_user_id = request.form.get('user_id')
        amount = request.form.get('amount')
        description = request.form.get('description', 'Manual credit adjustment')
        
        # VULNERABLE: No proper authorization check
        try:
            if not amount or not target_user_id:
                return render_template('secret_add_money.html', error='Amount and User ID are required')
            
            amount = float(amount)
            target_user_id = int(target_user_id)
            
            if amount <= 0:
                return render_template('secret_add_money.html', error='Amount must be positive')
            
            conn = sqlite3.connect('vulnerable_shop.db')
            cursor = conn.cursor()
            
            # Check if target user exists
            cursor.execute("SELECT username, wallet_balance FROM users WHERE id = ?", (target_user_id,))
            target_user = cursor.fetchone()
            
            if not target_user:
                conn.close()
                return render_template('secret_add_money.html', error='User not found')
            
            # Add money to user's wallet
            new_balance = target_user[1] + amount
            cursor.execute("UPDATE users SET wallet_balance = ? WHERE id = ?", (new_balance, target_user_id))
            
            # Log transaction
            cursor.execute("""
                INSERT INTO wallet_transactions (user_id, transaction_type, amount, description, admin_user_id)
                VALUES (?, ?, ?, ?, ?)
            """, (target_user_id, 'credit', amount, f'{description} - ADMIN_{uuid.uuid4().hex[:8].upper()}', session['user_id']))
            
            conn.commit()
            conn.close()
            
            success_msg = f'Successfully added ${amount:.2f} to {target_user[0]}\'s wallet. New balance: ${new_balance:.2f}'
            return render_template('secret_add_money.html', success=success_msg)
            
        except ValueError:
            return render_template('secret_add_money.html', error='Invalid amount or user ID')
        except Exception as e:
            return render_template('secret_add_money.html', error=f'Error: {str(e)}')
    
    return render_template('secret_add_money.html')

# VULNERABILITY: Even weaker authentication - URL parameter based
@app.route('/quick_money')
def quick_money():
    # VULNERABLE: Anyone can access if they know the URL and parameters
    user_id = request.args.get('user_id')
    amount = request.args.get('amount')
    admin_key = request.args.get('key')
    
    # VULNERABLE: Weak admin key check
    if admin_key != 'admin123':
        return jsonify({'error': 'Invalid admin key'})
    
    if not user_id or not amount:
        return jsonify({'error': 'Missing user_id or amount parameters'})
    
    try:
        user_id = int(user_id)
        amount = float(amount)
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, wallet_balance FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'error': 'User not found'})
        
        new_balance = user[1] + amount
        cursor.execute("UPDATE users SET wallet_balance = ? WHERE id = ?", (new_balance, user_id))
        
        # Log transaction without proper admin tracking
        cursor.execute("""
            INSERT INTO wallet_transactions (user_id, transaction_type, amount, description)
            VALUES (?, ?, ?, ?)
        """, (user_id, 'credit', amount, f'Quick admin credit - QUICK_{uuid.uuid4().hex[:8].upper()}'))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Added ${amount:.2f} to {user[0]}\'s wallet',
            'new_balance': new_balance
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

# VULNERABILITY: API endpoint with weak authentication
@app.route('/api/wallet/add', methods=['POST'])
def api_add_money():
    # VULNERABLE: Basic auth bypass
    auth_token = request.headers.get('Authorization') or request.form.get('token')
    
    if not auth_token or auth_token != 'Bearer admin_token_123':
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json() or request.form
    user_id = data.get('user_id')
    amount = data.get('amount')
    
    try:
        if not amount or not user_id:
            return jsonify({'error': 'User ID and amount are required'}), 400
            
        amount = float(amount)
        user_id = int(user_id)
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?", (amount, user_id))
        
        cursor.execute("""
            INSERT INTO wallet_transactions (user_id, transaction_type, amount, description)
            VALUES (?, ?, ?, ?)
        """, (user_id, 'credit', amount, f'API credit via token - API_{uuid.uuid4().hex[:8].upper()}'))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Added ${amount:.2f} to user {user_id}'})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/news/<int:article_id>')
def news_article(article_id):
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # VULNERABLE: IDOR
    cursor.execute("SELECT * FROM news WHERE id = ?", (article_id,))
    article = cursor.fetchone()
    conn.close()
    
    if not article:
        return "Article not found", 404
    
    return render_template('news_article.html', article=article)

# Support system with vulnerabilities
@app.route('/support')
def support():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM support_tickets WHERE user_id = ? ORDER BY created_at DESC", (session['user_id'],))
    tickets = cursor.fetchall()
    conn.close()
    
    return render_template('support.html', tickets=tickets)

@app.route('/support/create', methods=['GET', 'POST'])
def create_ticket():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        priority = request.form.get('priority', 'medium')
        
        if not all([subject, message]):
            return render_template('create_ticket.html', error='Subject and message are required')
        
        conn = sqlite3.connect('vulnerable_shop.db')
        cursor = conn.cursor()
        
        # VULNERABLE: XSS in message content
        cursor.execute("""
            INSERT INTO support_tickets (user_id, subject, message, priority) 
            VALUES (?, ?, ?, ?)
        """, (session['user_id'], subject, message, priority))
        
        conn.commit()
        conn.close()
        return redirect('/support')
    
    return render_template('create_ticket.html')

# API endpoints with authentication vulnerabilities
@app.route('/api/users')
def api_users():
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key required'}), 401
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Weak API key validation
    cursor.execute("SELECT user_id, permissions FROM api_keys WHERE api_key = ? AND is_active = 1", (api_key,))
    key_info = cursor.fetchone()
    
    if not key_info:
        conn.close()
        return jsonify({'error': 'Invalid API key'}), 401
    
    # VULNERABLE: Excessive data exposure
    cursor.execute("SELECT id, username, email, role, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'role': user[3],
        'created_at': user[4]
    } for user in users])

@app.route('/api/products')
def api_products():
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': p[0],
        'name': p[1],
        'description': p[2],
        'price': p[3],
        'seller_id': p[4],
        'category': p[5],
        'stock_quantity': p[6]
    } for p in products])

# XML processing endpoint for XXE vulnerability
@app.route('/xml_import', methods=['GET', 'POST'])
@requires_role('admin')
def xml_import():
    if request.method == 'POST':
        xml_file = request.files.get('xml_file')
        
        if not xml_file:
            return render_template('xml_import.html', error='No XML file provided')
        
        try:
            import xml.etree.ElementTree as ET
            
            # VULNERABLE: XXE - External Entity Processing enabled
            xml_content = xml_file.read().decode('utf-8')
            
            # Parse XML without disabling external entities
            root = ET.fromstring(xml_content)
            
            # Process the XML (simulate importing data)
            result = f"XML processed successfully. Root element: {root.tag}"
            return render_template('xml_import.html', success=result)
            
        except Exception as e:
            return render_template('xml_import.html', error=f'XML processing error: {str(e)}')
    
    return render_template('xml_import.html')

# Additional API routes
@app.route('/admin/toggle_user/<int:user_id>', methods=['POST'])
@requires_role('admin')
def toggle_user(user_id):
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT is_active FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'success': False, 'error': 'User not found'})
    
    new_status = 0 if user[0] == 1 else 1
    cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/admin/reset_password/<int:user_id>', methods=['POST'])
@requires_role('admin')
def reset_password(user_id):
    data = request.get_json()
    new_password = data.get('password') if data else request.args.get('password')
    
    if not new_password:
        return jsonify({'success': False, 'error': 'No password provided'})
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # VULNERABLE: No password strength validation
    password_hash = hashlib.md5(new_password.encode()).hexdigest() if new_password else ''
    
    cursor.execute("UPDATE users SET password = ?, failed_login_attempts = 0 WHERE id = ?", 
                  (password_hash, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/ticket/<int:ticket_id>')
def api_ticket(ticket_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # VULNERABLE: IDOR - No authorization check
    cursor.execute("SELECT * FROM support_tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    
    return jsonify({
        'id': ticket[0],
        'subject': ticket[2],
        'message': ticket[3],
        'status': ticket[4],
        'priority': ticket[5],
        'created_at': ticket[7]
    })

@app.route('/news/<int:article_id>/comment', methods=['POST'])
def add_news_comment(article_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    comment = request.form.get('comment')
    
    if not comment:
        return redirect(f'/news/{article_id}')
    
    # This would normally add to comments table
    # For now, just redirect back
    return redirect(f'/news/{article_id}')

if __name__ == '__main__':
    # Create uploads directory for file operations
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Create a sample file for directory traversal testing
    with open('uploads/sample.txt', 'w') as f:
        f.write('This is a sample file for download testing.')
    
    # Initialize database
    init_db()
    
    print("\n" + "="*60)
    print("🔥 VULNERABLE E-COMMERCE LAB STARTED 🔥")
    print("="*60)
    print("⚠️  WARNING: This application contains intentional vulnerabilities!")
    print("⚠️  DO NOT use this in production environments!")
    print("="*60)
    print("\n🎯 VULNERABILITIES INCLUDED:")
    print("1. SQL Injection (Login page)")
    print("2. Cross-Site Scripting (XSS) in comments")
    print("3. Business Logic Flaw - Coupon abuse")
    print("4. Insecure Direct Object References (IDOR)")
    print("5. Cross-Site Request Forgery (CSRF)")
    print("6. Directory/Path Traversal")
    print("7. Server-Side Request Forgery (SSRF)")
    print("8. Server-Side Template Injection (SSTI)")
    print("9. Insecure Deserialization")
    print("10. Command Injection")
    print("11. Local File Inclusion (LFI)")
    print("12. Broken Authentication & Authorization")
    print("="*60)
    print("\n🔑 ACCESS CREDENTIALS:")
    print("guest_user / guest123")  
    print("test_user / test123")
    print("lab_user / lab123")
    print("demo_user / demo123")
    print("="*60)
    print("\n👥 LAB USER ACCOUNTS:")
    print("Admin: admin / admin123")
    print("Moderator: moderator / mod123") 
    print("User: user1 / password123")
    print("Guest: guest_user / guest123")
    print("="*60)
    
    # Determine host and port based on environment
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5002))
    
    if os.environ.get('CODESPACES'):
        print(f"🌐 Codespaces URL: https://{os.environ.get('CODESPACE_NAME')}-{port}.{os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')}")
    elif os.environ.get('RENDER'):
        print("🌐 Render.com deployment detected")
        print("🌐 Use any of the access credentials above to enter the lab")
    elif os.environ.get('RAILWAY_ENVIRONMENT'):
        print("🌐 Railway deployment detected")
        print("🌐 Use any of the access credentials above to enter the lab") 
    else:
        print(f"🌐 Local access: http://127.0.0.1:{port}")
        print("🌐 No authentication required for local access")
    
    print("="*60)
    
    app.run(debug=True, host=host, port=port)

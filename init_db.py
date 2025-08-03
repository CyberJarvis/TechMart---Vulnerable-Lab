#!/usr/bin/env python3
"""
Database initialization script for Vulnerable E-commerce Lab
This script creates the database with proper schema including wallet functionality
"""

import sqlite3
import os
import hashlib
from datetime import datetime

def hash_password(password):
    """Simple MD5 hash for passwords (intentionally weak for educational purposes)"""
    return hashlib.md5(password.encode()).hexdigest()

def init_database():
    """Initialize the vulnerable_shop.db database with proper schema"""
    
    # Remove existing database if it exists
    if os.path.exists('vulnerable_shop.db'):
        os.remove('vulnerable_shop.db')
        print("✅ Removed existing database")
    
    # Connect to database (will create if not exists)
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    
    # Create users table with wallet_balance
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            wallet_balance REAL DEFAULT 200.0,
            last_login TIMESTAMP,
            failed_login_attempts INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            is_featured INTEGER DEFAULT 0
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            promo_code TEXT,
            discount REAL DEFAULT 0,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Create wallet_transactions table
    cursor.execute('''
        CREATE TABLE wallet_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            description TEXT,
            admin_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (admin_id) REFERENCES users (id)
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create support_tickets table
    cursor.execute('''
        CREATE TABLE support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create news table
    cursor.execute('''
        CREATE TABLE news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            is_published INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    # Create coupons table
    cursor.execute('''
        CREATE TABLE coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount_percent REAL NOT NULL,
            usage_limit INTEGER DEFAULT 1,
            used_count INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create api_keys table
    cursor.execute('''
        CREATE TABLE api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            permissions TEXT DEFAULT 'read',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create file_uploads table
    cursor.execute('''
        CREATE TABLE file_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            user_id INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    print("✅ Created all tables successfully")
    
    # Insert sample users with different roles and wallet balances
    users_data = [
        ('admin', hash_password('admin123'), 'admin@techmart.com', 'admin', 1000.0, None, 0, 1),
        ('moderator', hash_password('mod123'), 'moderator@techmart.com', 'moderator', 500.0, None, 0, 1),
        ('seller', hash_password('sell123'), 'seller@techmart.com', 'seller', 750.0, None, 0, 1),
        ('john_doe', hash_password('password123'), 'john@example.com', 'user', 200.0, None, 0, 1),
        ('jane_smith', hash_password('mypass'), 'jane@example.com', 'user', 200.0, None, 0, 1),
        ('guest_user', hash_password('guest'), 'guest@example.com', 'guest', 200.0, None, 0, 1),
        ('test_user', hash_password('test'), 'test@test.com', 'user', 200.0, None, 0, 1)
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password, email, role, wallet_balance, last_login, failed_login_attempts, is_active) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)
    
    print("✅ Inserted sample users")
    
    # Insert sample products
    products_data = [
        ('Gaming Laptop Pro', 'High-performance gaming laptop with RTX graphics', 1299.99, 15, 'laptop.jpg', 1),
        ('Smartphone X', 'Latest flagship smartphone with advanced camera', 899.99, 25, 'phone.jpg', 1),
        ('Wireless Gaming Mouse', 'Precision wireless mouse for gaming', 79.99, 50, 'mouse.jpg', 1),
        ('Premium Headphones', 'Noise-cancelling over-ear headphones', 199.99, 30, 'headphones.jpg', 0),
        ('Smart Watch Elite', 'Advanced fitness and smartwatch', 299.99, 20, 'watch.jpg', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO products (name, description, price, stock, image_url, is_featured) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', products_data)
    
    print("✅ Inserted sample products")
    
    # Insert sample orders
    orders_data = [
        (4, 1, 1, 1299.99, 'SAVE10', 129.99, '2024-12-15 10:30:00'),
        (5, 2, 2, 1799.98, None, 0, '2024-12-16 14:20:00'),
        (6, 3, 1, 79.99, 'WELCOME5', 4.00, '2024-12-17 09:15:00'),
        (4, 4, 1, 199.99, None, 0, '2024-12-18 16:45:00'),
        (7, 5, 1, 299.99, 'SAVE10', 29.99, '2024-12-19 11:30:00')
    ]
    
    cursor.executemany('''
        INSERT INTO orders (user_id, product_id, quantity, total_price, promo_code, discount, order_date) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', orders_data)
    
    print("✅ Inserted sample orders")
    
    # Insert sample wallet transactions
    transactions_data = [
        (1, 1000.0, 'credit', 'Initial admin balance', None),
        (2, 500.0, 'credit', 'Initial moderator balance', 1),
        (3, 750.0, 'credit', 'Initial seller balance', 1),
        (4, 250.0, 'credit', 'Welcome bonus', 1),
        (5, 150.0, 'credit', 'Account setup bonus', 1),
        (6, 50.0, 'credit', 'Guest account credit', 1),
        (7, 100.0, 'credit', 'Test account setup', 1),
        (4, -50.0, 'debit', 'Purchase payment', None),
        (5, 25.0, 'credit', 'Referral bonus', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO wallet_transactions (user_id, amount, transaction_type, description, admin_id) 
        VALUES (?, ?, ?, ?, ?)
    ''', transactions_data)
    
    print("✅ Inserted sample wallet transactions")
    
    # Insert sample comments
    comments_data = [
        (1, 4, 'Amazing laptop! Great for gaming and work.'),  # john_doe (user_id=4)
        (2, 5, 'Best phone I\'ve ever owned. Camera is incredible!'),  # jane_smith (user_id=5)
        (3, 7, 'Perfect mouse for competitive gaming.'),  # test_user (user_id=7)
        (1, 6, '<script>alert("XSS vulnerability")</script>Great laptop!'),  # guest_user (user_id=6)
        (4, 4, 'Sound quality is outstanding!')  # john_doe (user_id=4)
    ]
    
    cursor.executemany('''
        INSERT INTO comments (product_id, user_id, comment) 
        VALUES (?, ?, ?)
    ''', comments_data)
    
    print("✅ Inserted sample comments")
    
    # Insert sample support tickets
    tickets_data = [
        (4, 'Login Issue', 'I cannot log into my account', 'open', 'high'),
        (5, 'Order Problem', 'My order was cancelled unexpectedly', 'pending', 'medium'),
        (6, 'Payment Question', 'Question about payment methods', 'closed', 'low'),
        (7, 'Product Inquiry', 'Need more info about gaming laptop', 'open', 'medium')
    ]
    
    cursor.executemany('''
        INSERT INTO support_tickets (user_id, subject, message, status, priority) 
        VALUES (?, ?, ?, ?, ?)
    ''', tickets_data)
    
    print("✅ Inserted sample support tickets")
    
    # Insert sample news articles
    news_data = [
        ('New Gaming Laptop Launch', 'We are excited to announce our latest gaming laptop with RTX 4080 graphics!', 1, 1),
        ('Holiday Sale Coming Soon', 'Get ready for our biggest sale of the year. Up to 50% off on selected items.', 1, 1),
        ('Security Update Notice', 'We have updated our security systems to better protect your data.', 2, 1),
        ('Customer Service Hours', 'Our customer service hours have been extended for better support.', 2, 0)
    ]
    
    cursor.executemany('''
        INSERT INTO news (title, content, author_id, is_published) 
        VALUES (?, ?, ?, ?)
    ''', news_data)
    
    print("✅ Inserted sample news articles")
    
    # Insert sample coupons
    coupons_data = [
        ('SAVE10', 10.0, 100, 5, 1),
        ('WELCOME5', 5.0, 50, 12, 1),
        ('NEWUSER', 15.0, 20, 3, 1),
        ('EXPIRED', 20.0, 10, 15, 0)
    ]
    
    cursor.executemany('''
        INSERT INTO coupons (code, discount_percent, usage_limit, used_count, active) 
        VALUES (?, ?, ?, ?, ?)
    ''', coupons_data)
    
    print("✅ Inserted sample coupons")
    
    # Insert sample API keys
    api_keys_data = [
        ('admin123', 1, 'admin', 1),
        ('user456', 4, 'read', 1),
        ('test789', 7, 'read', 0)
    ]
    
    cursor.executemany('''
        INSERT INTO api_keys (api_key, user_id, permissions, is_active) 
        VALUES (?, ?, ?, ?)
    ''', api_keys_data)
    
    print("✅ Inserted sample API keys")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("\n🎉 Database initialized successfully!")
    print("📊 Database contains:")
    print("   - 7 users with different roles (admin, moderator, seller, users, guest)")
    print("   - 5 products with stock and featured flags")
    print("   - 5 sample orders")
    print("   - 9 wallet transactions")
    print("   - 5 comments (including XSS example)")
    print("   - 4 support tickets")
    print("   - 4 news articles")
    print("   - 4 discount coupons")
    print("   - 3 API keys")
    print("\n🔐 Default login credentials:")
    print("   Admin: admin / admin123")
    print("   Moderator: moderator / mod123")
    print("   Seller: seller / sell123")
    print("   User: john_doe / password123")
    print("   Guest: guest_user / guest")

if __name__ == '__main__':
    init_database()

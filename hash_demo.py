#!/usr/bin/env python3
"""
MD5 Hash Vulnerability Demonstration
Shows how weak MD5 hashing can be cracked
"""

import hashlib
import requests
import sqlite3

def demonstrate_md5_weakness():
    """Demonstrate MD5 hash cracking"""
    print("🔐 MD5 Hash Vulnerability Demonstration")
    print("=" * 50)
    
    # Get hashes from database
    conn = sqlite3.connect('vulnerable_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users")
    users = cursor.fetchall()
    conn.close()
    
    # Common passwords to test
    common_passwords = [
        "admin123", "password123", "secret456", "mod123", 
        "sell123", "guest", "test", "admin", "password", 
        "123456", "qwerty", "letmein"
    ]
    
    print("\n🎯 Attempting to crack MD5 hashes...")
    print("-" * 50)
    
    cracked = 0
    for username, hash_value in users:
        print(f"\n👤 User: {username}")
        print(f"🔑 Hash: {hash_value}")
        
        # Try to crack the hash
        for password in common_passwords:
            test_hash = hashlib.md5(password.encode()).hexdigest()
            if test_hash == hash_value:
                print(f"✅ CRACKED! Password: '{password}'")
                cracked += 1
                break
        else:
            print("❌ Password not in common list")
    
    print(f"\n📊 Results: {cracked}/{len(users)} passwords cracked!")
    print("\n⚠️  This demonstrates why MD5 should NEVER be used for passwords!")
    print("💡 Use bcrypt, Argon2, or scrypt instead.")

if __name__ == "__main__":
    demonstrate_md5_weakness()

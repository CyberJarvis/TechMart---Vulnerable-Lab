# 🚀 Deployment Guide - Vulnerable E-Commerce Lab

## ⚠️ SECURITY WARNING
This application contains **INTENTIONAL VULNERABILITIES** for educational purposes. **NEVER** deploy without proper access controls!

## 🛡️ Built-in Safety Features
- Basic HTTP authentication for hosted environments
- Environment detection (Codespaces, Render, Railway)
- Private port forwarding by default
- Clear warning messages

## 📋 Deployment Options

### 1. GitHub Codespaces (Recommended - FREE)

**Steps:**
1. Push this repo to GitHub
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for setup to complete
4. Run: `python app.py`
5. Access via the forwarded port URL

**Access:**
- Username: `labuser`
- Password: `vulnerable123`

### 2. Render.com (FREE Tier)

**Steps:**
1. Connect GitHub repo to Render
2. Select "Web Service"
3. Use these settings:
   - Build Command: `pip install -r requirements.txt && python init_db.py`
   - Start Command: `python app.py`
4. Deploy

### 3. Railway.app ($5 Free Credit)

**Steps:**
1. Connect GitHub repo
2. Railway auto-detects Python
3. Deploy automatically

### 4. Replit (FREE)

**Steps:**
1. Import from GitHub
2. Run the project
3. Access via Replit's URL

## 🔐 Access Credentials (for hosted versions)

```
Username: labuser
Password: vulnerable123
```

## 🎯 Test Vulnerabilities

Once deployed, test these vulnerabilities:

### SQL Injection:
- Login: `admin' OR '1'='1' --`
- Search: `' UNION SELECT username,password FROM users --`

### XSS:
- Comments: `<script>alert('XSS')</script>`

### Directory Traversal:
- `/files/app.py`
- `/read/etc/passwd`
- `/download/../app.py`

### IDOR:
- `/receipt/1` (try different IDs)
- `/profile/2` (access other users)

## 📊 Built-in Test Accounts

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| user1 | password123 | User |
| moderator | mod123 | Moderator |

## 🚨 Important Notes

1. **Private Access Only**: Never make this publicly accessible
2. **Educational Use**: Only for cybersecurity education
3. **Monitor Access**: Keep track of who has access
4. **Limited Time**: Deploy only when needed
5. **Takedown Plan**: Have a plan to remove quickly

## 🔧 Local Development

```bash
# Setup
pip install -r requirements.txt
python init_db.py
python app.py

# Access
http://127.0.0.1:5002
```

## 📝 Vulnerability Categories

- **OWASP Top 10 2021** coverage
- **18+ vulnerability types**
- **Real-world examples**
- **Educational exploits**

## 🛠️ Troubleshooting

### Port Issues:
- Codespaces: Check port forwarding settings
- Render: Uses PORT environment variable
- Railway: Auto-assigns ports

### Database Issues:
- Run `python init_db.py` manually if needed
- Check if SQLite file is created

### Authentication Issues:
- Use: `labuser` / `vulnerable123`
- Clear browser cache if needed

---

**Remember**: This is for **EDUCATION ONLY**! Always deploy responsibly! 🎓

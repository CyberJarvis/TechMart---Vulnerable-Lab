# 🚀 Deploy to Render.com - Step by Step Guide

## 📋 Prerequisites
- GitHub account
- Render.com account (free)

## 🔧 Deployment Steps

### 1. Prepare GitHub Repository
```bash
# Create a new public repository on GitHub
# Name: vulnerable-ecommerce-lab (or your preferred name)

# Clone and push this code
git init
git add .
git commit -m "Initial commit - Cybersecurity Education Lab"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vulnerable-ecommerce-lab.git
git push -u origin main
```

### 2. Deploy to Render.com

1. **Go to Render.com** and sign up/login
2. **Connect GitHub** account if not already connected
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository** → Select your repository
5. **Configure Service:**
   - **Name**: `cybersecurity-education-lab`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python init_db.py`
   - **Start Command**: `python app.py`
   - **Plan**: `Free`

6. **Click "Create Web Service"**

### 3. Automatic Configuration
The `render.yaml` file will automatically configure:
- ✅ Python environment
- ✅ Dependencies installation
- ✅ Database initialization
- ✅ Security authentication
- ✅ Environment variables

### 4. Access Your Lab

Once deployed, you'll get a URL like:
`https://cybersecurity-education-lab.onrender.com`

**🔑 Access Credentials** (choose any):
```
guest_user / guest123
test_user  / test123
lab_user   / lab123
demo_user  / demo123
```

### 5. Lab User Accounts
Once inside the lab:
```
Admin:     admin / admin123
Moderator: moderator / mod123
User:      user1 / password123
Guest:     guest_user / guest123
```

## 🔒 Security Features

### Automatic Protection
- **HTTP Basic Auth** enabled for hosted versions
- **Environment detection** (Render.com)
- **Access control** prevents unauthorized use
- **Educational warnings** displayed

### Safe for Public Repos
- ✅ No hardcoded secrets exposed
- ✅ Authentication required for access
- ✅ Clear educational purpose
- ✅ Vulnerability warnings

## 🧪 Testing the Deployment

### 1. Verify Access
- Visit your Render.com URL
- Enter lab credentials when prompted
- Should see the e-commerce homepage

### 2. Test Vulnerabilities
```bash
# SQL Injection (Login)
Username: admin' OR '1'='1' --
Password: anything

# Directory Traversal
https://your-app.onrender.com/files/app.py
https://your-app.onrender.com/read/etc/passwd

# XSS (Comments)
<script>alert('XSS Test')</script>
```

## 🔧 Troubleshooting

### Common Issues

**Build Fails:**
- Check `requirements.txt` for typos
- Verify Python version compatibility

**Database Issues:**
- Render automatically runs `python init_db.py`
- Check build logs for SQLite errors

**Authentication Problems:**
- Use exact credentials (case-sensitive)
- Clear browser cache/cookies

**App Won't Start:**
- Check Render logs for Python errors
- Verify Flask app starts correctly

### Render.com Logs
- **Dashboard** → **Your Service** → **Logs**
- Check for startup errors or crashes

## 📊 Monitoring

### Render.com Dashboard
- **Service Status** - Running/Stopped
- **Build Logs** - Deployment process
- **Runtime Logs** - Application output
- **Metrics** - Performance data

### Usage Limits (Free Tier)
- **750 hours/month** runtime
- **Sleeps after 15 minutes** of inactivity
- **500 MB RAM** limit
- **100 GB bandwidth** per month

## 🔄 Updates and Maintenance

### Updating the Lab
```bash
# Make changes locally
git add .
git commit -m "Update vulnerabilities"
git push

# Render automatically redeploys
```

### Manual Redeploy
- Render Dashboard → Your Service → Manual Deploy

## 🎓 Educational Use

### For Instructors
- Share the Render.com URL with students
- Provide access credentials
- Monitor usage via Render logs
- Easy to redeploy updates

### For Students
- No local setup required
- Immediate access via browser
- Practice on real vulnerabilities
- Safe, controlled environment

## 💰 Cost Considerations

### Free Tier Limits
- **$0/month** for basic usage
- **15-minute sleep** after inactivity
- **Cold start** (~30 seconds) when waking

### Upgrade Options
- **$7/month** for always-on
- **No sleep** time
- **Faster** performance

## ⚖️ Legal Compliance

### Public Repository Safety
- ✅ **Educational purpose** clearly stated
- ✅ **Authentication required** for access
- ✅ **Vulnerability warnings** prominent
- ✅ **No production secrets** exposed

### Terms of Service
- ✅ **Render.com ToS** compliant
- ✅ **GitHub ToS** compliant
- ✅ **Educational use** permitted
- ✅ **No malicious content**

---

## 🎉 Success!

Your cybersecurity education lab is now publicly accessible via Render.com with proper security controls! Share the URL and credentials with your students or use it for your own learning.

**Remember**: This is for **educational purposes only**! 🎓🔒

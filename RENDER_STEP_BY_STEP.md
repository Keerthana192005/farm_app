# Render Deployment - Step by Step Guide

## 📋 Prerequisites

Before you start, you'll need:
- A GitHub account (free)
- Your code pushed to a GitHub repository
- A Render account (free signup at render.com)

---

## 🚀 Step 1: Create a GitHub Repository

### 1.1 Initialize Git (if not already done)
```bash
cd "c:\Users\Keerthana\Downloads\farm_app (2)\farm_app (3)\farm_app"
git init
git add .
git commit -m "Initial farm app commit"
```

### 1.2 Create Repository on GitHub
1. Go to [github.com](https://github.com)
2. Sign in (or create account)
3. Click **"New"** to create a new repository
4. Name it: `farm-app`
5. Add description: "Farm management e-commerce platform"
6. Choose **Public** (for Render free tier)
7. Click **Create Repository**

### 1.3 Push Code to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/farm-app.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Create Render Account & Database

### 2.1 Sign Up for Render
1. Go to [render.com](https://render.com)
2. Click **"Sign Up"**
3. Choose **"Sign up with GitHub"** (easiest)
4. Authorize Render to access your GitHub account
5. Complete signup

### 2.2 Create PostgreSQL Database
1. In Render dashboard, click **New +** (top right)
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `farm-app-db`
   - **Database**: `farm_app`
   - **User**: `farm_user`
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 15
   - **Plan**: Free
4. Click **Create Database**
5. Wait for creation (2-3 minutes)
6. **Copy the Internal Database URL** (you'll need this!)

**Example URL format:**
```
postgresql://farm_user:password@localhost:5432/farm_app
```

---

## 🔧 Step 3: Create Web Service on Render

### 3.1 Create New Web Service
1. Click **New +** in Render dashboard
2. Select **"Web Service"**
3. Choose **"Build and deploy from a Git repository"**

### 3.2 Connect GitHub Repository
1. Click **"Connect account"** next to GitHub
2. Authorize if asked
3. Select your repository: `farm-app`
4. Click **"Connect"**

### 3.3 Configure Service Settings
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `farm-app` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT wsgi:app` |
| **Plan** | `Free` |
| **Region** | Same as database |

### 3.4 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | *Paste the PostgreSQL URL from Step 2.6* |
| `SECRET_KEY` | *Render will auto-generate this* |

**How to add**:
1. Click **"Add Environment Variable"**
2. Enter Key: `FLASK_ENV`
3. Enter Value: `production`
4. Click **"Add Environment Variable"** again
5. Repeat for other variables

### 3.5 Create Web Service
Click **"Create Web Service"** button

**This will start the deployment!** ⏳

---

## ⏳ Step 4: Wait for Deployment

Monitor the deployment process:
1. **Build Phase** (2-3 minutes)
   - Render installs Python packages
   - Watch the logs for any errors
   
2. **Deployment Phase** (1-2 minutes)
   - Application starts
   - Database gets initialized
   - Seed data loads

### What to Look For
- ✅ "Deployment successful" message
- ✅ Green status indicator
- ✅ Your app URL appears (like: `https://farm-app.onrender.com`)

### If Deployment Fails
- Check the **"Logs"** section
- Common issues:
  - Missing environment variables
  - Wrong database URL
  - Syntax errors in code
  - Missing requirements

---

## 🌍 Step 5: Access Your Deployed App

### Your App URL
Once deployment succeeds, your app will be live at:
```
https://farm-app.onrender.com
```

**Note**: Render's free tier has a delay on first access (app may "wake up")

### Test the App
1. Visit: `https://farm-app.onrender.com/`
   - Should see your home page
   
2. Visit: `https://farm-app.onrender.com/admin`
   - Should see admin login page
   
3. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`
   - Should see admin dashboard

---

## 🔐 Step 6: Secure Your Application (IMPORTANT!)

### Change Admin Password Immediately

1. Go to: `https://farm-app.onrender.com/admin`
2. Login with: `admin` / `admin123`
3. Click **"Settings"** in sidebar
4. Click **"Change Password"**
5. Enter:
   - **Current Password**: `admin123`
   - **New Password**: Something strong (12+ characters)
   - **Confirm Password**: Same as above
6. Click **"Update Password"**
7. Log out and log back in with new password

---

## 📊 Step 7: Test Core Features

### Test Customer Features
- [ ] Browse products on home page
- [ ] Search for products using search bar
- [ ] Filter by price
- [ ] Add items to cart
- [ ] Go to checkout
- [ ] Verify only "Cash on Delivery" shows
- [ ] Verify payment details show: "Pay to this number: 7349784480"

### Test Admin Features
- [ ] Login to admin dashboard
- [ ] View orders in "Orders" section
- [ ] View customers in "Customers"
- [ ] View analytics in "Analytics"
- [ ] View inventory in "Inventory"
- [ ] Add a new product
- [ ] Edit a product
- [ ] Change admin password

---

## 🛠️ Step 8: Monitor Your App

### Check Render Dashboard
1. Click on your service in Render
2. **Logs** tab: View real-time application logs
3. **Metrics** tab: Monitor CPU, Memory, Network
4. **Events** tab: See deployment history

### Set Up Alerts (Optional)
In Render dashboard:
1. Click **"Notifications"**
2. Set email alerts for:
   - Deployment failures
   - High CPU usage
   - High memory usage

---

## 🔄 Continuous Deployment

### Automatic Deployments
Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update farm app"
git push
```

Render will automatically:
1. Pull latest code
2. Run build command
3. Restart the app
4. Keep it live (no downtime)

---

## 📸 Updating App After Deployment

### To Update Your App:
1. Make changes locally
2. Run and test: `python app.py`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Your change description"
   git push
   ```
4. Watch deployment in Render dashboard
5. Changes live in 5-10 minutes

### Common Updates:
- **Add new product**: No deployment needed (in-app)
- **Change template**: Commit and push
- **Update prices**: No deployment needed (in-app)
- **Fix bugs**: Commit and push
- **Add features**: Commit and push

---

## 📈 File Storage (Important for Uploads)

### Current Limitation
Free tier Render has **ephemeral storage** - files disappear on app restart.

### For Product Images
Since you removed the image upload feature, you're good! But if you need images:

**Option 1**: Use external URLs (no uploads needed)
```html
<img src="https://external-site.com/image.jpg">
```

**Option 2**: Use a free file service
- **Cloudinary** (free tier available)
- **Imgur** (upload images, get URL)
- **AWS S3** (small free tier)

---

## 🐛 Troubleshooting

### App Won't Start
**Problem**: Deployment shows error
**Solution**:
1. Check **Logs** in Render dashboard
2. Look for error messages
3. Common fixes:
   - Verify DATABASE_URL is correct
   - Check SECRET_KEY is set
   - Ensure requirements.txt has no errors

### Can't Log In
**Problem**: Admin login not working
**Solution**:
1. Database might not be initialized
2. Check logs: `db.create_all()` ran?
3. Try clearing browser cookies
4. Open app in incognito/private window

### Slow Performance
**Problem**: App is slow or timing out
**Solution**:
1. Free tier might be overloaded
2. Check **Metrics** in Render
3. Consider upgrading to paid plan
4. Optimize database queries

### Static Files Not Loading
**Problem**: CSS/Images not showing
**Solution**:
1. Check static folder exists locally
2. Verify in github repo contains static/
3. Restart deployment:
   - Make a change to code
   - Push to GitHub
   - Render will redeploy

---

## 💡 Performance Tips

### Optimize Your App
1. **Minimize database queries** - use eager loading
2. **Cache static files** - use CDN (optional)
3. **Optimize images** - compress before upload
4. **Enable GZIP** - Render does this automatically
5. **Monitor logs** - find slow endpoints

### Upgrade to Paid Plan
For production use:
- **Advantage**: No sleep-on-idle
- **Cost**: $7/month+ (PostgreSQL + Web service)
- **Benefits**: Better performance, guaranteed uptime

---

## 📚 Useful Resources

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Gunicorn**: https://gunicorn.org/

---

## ✅ Deployment Checklist (Final)

Before considering your app fully deployed:

- [ ] App loads on Render URL (https://farm-app.onrender.com)
- [ ] Admin login works
- [ ] Admin password changed from default
- [ ] Home page shows products
- [ ] Search/filter works
- [ ] Cart and checkout functional
- [ ] Admin dashboard accessible
- [ ] Analytics page working
- [ ] Inventory page working
- [ ] No errors in Render logs
- [ ] Database initialized with data
- [ ] Static files (CSS, JS) loading correctly
- [ ] Mobile-responsive layout working

---

## 🎉 You're Live!

Congratulations! Your Farm App is now live on Render! 

Your deployment URL:
```
https://farm-app.onrender.com
```

Share this URL with customers to access your farm's e-commerce platform!

---

## 📞 Getting Help

If something goes wrong:
1. **Check Render Logs** - Most detailed information
2. **Read error messages** - They're usually helpful
3. **Review changes** - What did you change recently?
4. **Check commit history** - Last successful deploy
5. **Rollback** - Go to deployment history, redeploy previous version

---

**Happy deploying! 🚀**

*Last updated: March 31, 2026*

# Campus Krishi - Quick Start Checklist

## 🚀 Getting Started

### **Step 1: Setup Environment** (5 minutes)
- [ ] Clone or download the farm_app folder
- [ ] Install Python 3.8+ on your system
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`

### **Step 2: Initialize Database** (5 minutes)
- [ ] Run Python interactive shell: `python`
- [ ] Execute these commands:
  ```python
  from app import app, db
  with app.app_context():
      db.create_all()
  exit()
  ```
- [ ] Verify `instance/database.db` is created

### **Step 3: Start Application** (2 minutes)
- [ ] Run: `python app.py`
- [ ] Open browser: `http://localhost:5000`
- [ ] Verify home page loads
- [ ] Admin login page accessible

### **Step 4: Test New Features** (10 minutes)

#### **Test Order Tracking**
- [ ] Click "Track Order" in navigation
- [ ] Create a test order (checkout with COD)
- [ ] Use Order ID from confirmation page
- [ ] Track order with phone number
- [ ] Verify order details display

#### **Test Analytics**
- [ ] Log in as Admin (username: admin, password: admin123)
- [ ] Click "Analytics" in sidebar
- [ ] Verify metrics display (revenue, orders, etc.)
- [ ] Check charts load and render correctly
- [ ] Check inventory alerts

#### **Test Inventory**
- [ ] Click "Inventory" in sidebar
- [ ] Verify stock classification (In Stock, Low, Out)
- [ ] Check color coding (Green, Yellow, Red)
- [ ] Click edit button on a product
- [ ] Change stock level and save
- [ ] Verify change reflects immediately

#### **Test Search & Filter**
- [ ] Go to home page
- [ ] Type product name in search (e.g., "tomato")
- [ ] Products filter instantly
- [ ] Use sort dropdown (price, name, etc.)
- [ ] Verify sorting works correctly

---

## 📋 Admin First-Time Setup

### **Step 1: Change Admin Password** (Required!)
1. Log in with default credentials:
   - Username: `admin`
   - Password: `admin123`
2. Click "Change Password" in sidebar
3. Enter new secure password
4. Confirm password
5. Click "Update Password"
6. Log out and log back in with new password

### **Step 2: Add Products** (Important)
1. Click "Products" → "Add Product"
2. Fill in details:
   - Name: e.g., "Tomatoes"
   - Price: e.g., 40
   - Stock: e.g., 50
   - Description: e.g., "Fresh red tomatoes"
   - Image: (optional) upload image
3. Click "Add Product"
4. Repeat for 5-10 products

### **Step 3: Monitor Dashboard**
1. Check "Dashboard" for overview
2. Review "Analytics" for metrics
3. Monitor "Inventory" for stock levels
4. Process "Orders" as they come in

---

## 👥 Creating Test Orders

### **Step 1: Add to Cart**
1. Go to home page
2. Click "Add to Cart" on products
3. Repeat for 2-3 products
4. Click cart icon (top right)

### **Step 2: Checkout**
1. Click "Proceed to Checkout"
2. Fill in delivery info:
   - Name
   - Phone (10 digits)
   - Address
   - Email (optional)
   - Delivery time
3. Click "Place Order"
4. **Save Order ID** for tracking

### **Step 3: Track Order**
1. Click "Track Order" in navigation
2. Enter saved Order ID
3. Enter same phone number
4. Click "Track Order"
5. View order status and details

---

## 🎯 Daily Admin Tasks

### **Morning** (5 minutes)
- [ ] Check Dashboard for overnight orders
- [ ] Review pending orders
- [ ] Mark completed orders as done
- [ ] Check Inventory alerts

### **Mid-Day** (10 minutes)
- [ ] View Analytics for trends
- [ ] Check low stock items
- [ ] Process received shipments
- [ ] Update inventory levels

### **Evening** (5 minutes)
- [ ] Review daily sales in Analytics
- [ ] Check inventory summary
- [ ] Note any issues for next day
- [ ] Backup database (manual or scheduled)

---

## 📞 Troubleshooting

### **Q: Database file not created**
```
A: Make sure you:
   1. Activated virtual environment
   2. Installed all dependencies
   3. Used correct Python commands
   4. Checked folder permissions
```

### **Q: "Module not found" error**
```
A: Reinstall dependencies:
   pip install -r requirements.txt --force-reinstall
```

### **Q: Analytics shows no data**
```
A: This is normal if no orders exist yet
   Solution: Create test orders first
```

### **Q: Charts not displaying**
```
A: Check browser console for errors
   Solution: Clear cache and refresh page
```

### **Q: Login not working**
```
A: Use default credentials:
   Username: admin
   Password: admin123
```

### **Q: Port 5000 already in use**
```
A: Change port by editing app.py last line:
   app.run(debug=True, port=5001)
```

---

## 🔒 Security Reminders

- [x] Change default admin password immediately
- [ ] Never commit sensitive data to version control
- [ ] Use HTTPS in production
- [ ] Keep dependencies updated
- [ ] Regular database backups
- [ ] Monitor for suspicious activity
- [ ] Use strong passwords

---

## 📊 Feature Access Guide

| Feature | User | Admin | URL |
|---------|------|-------|-----|
| Home | ✅ | ✅ | `/` |
| Products | ✅ | ✅ | Browsable |
| Cart | ✅ | ✅ | `/cart` |
| Checkout | ✅ | N/A | `/checkout` |
| Track Order | ✅ | ✅ | `/track_order` |
| Dashboard | N/A | ✅ | `/admin/dashboard` |
| Analytics | N/A | ✅ | `/admin/analytics` |
| Inventory | N/A | ✅ | `/admin/inventory-management` |
| Products Mgmt | N/A | ✅ | `/admin/products` |
| Customers | N/A | ✅ | `/admin/customers` |
| Reports | N/A | ✅ | `/admin/reports` |

---

## 📱 Testing on Mobile

1. Get your computer's IP address:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`
2. Start app on computer
3. On phone/tablet, visit: `http://<IP_ADDRESS>:5000`
4. Test all features on mobile

---

## 🎓 Learning Resources

- **User Guide**: See `USER_ADMIN_GUIDE.md`
- **Admin Guide**: See `USER_ADMIN_GUIDE.md`
- **Developer Guide**: See `DEVELOPER_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Improvement Analysis**: See `IMPROVEMENT_ANALYSIS.md`

---

## ✅ Verification Checklist

After setup, verify these work:

### **Customer Features**
- [ ] Can add products to cart
- [ ] Can place order
- [ ] Can track order by ID + phone
- [ ] Can search products
- [ ] Can filter by price
- [ ] Can sort products

### **Admin Features**
- [ ] Can log in
- [ ] Can view dashboard
- [ ] Can view analytics
- [ ] Can see inventory status
- [ ] Can add/edit products
- [ ] Can manage orders
- [ ] Can view customer list
- [ ] Can change password

### **Data Features**
- [ ] Orders appear in database
- [ ] Charts show data
- [ ] Inventory updates properly
- [ ] Analytics calculate correctly

---

## 🚀 Production Deployment

When ready to deploy to production:

1. **Environment Setup**
   - [ ] Set `DEBUG = False`
   - [ ] Use strong `SECRET_KEY`
   - [ ] Use PostgreSQL (not SQLite)
   - [ ] Configure environment variables

2. **Security**
   - [ ] Enable HTTPS
   - [ ] Set secure cookies
   - [ ] Add rate limiting
   - [ ] Regular security audits

3. **Performance**
   - [ ] Enable caching
   - [ ] Optimize database
   - [ ] Use CDN for static files
   - [ ] Setup monitoring

4. **Backup & Recovery**
   - [ ] Daily database backups
   - [ ] Off-site backup storage
   - [ ] Recovery procedure testing
   - [ ] Disaster recovery plan

---

## 📞 Support Contact

For questions or issues:
- Email: sumaraj.r@nmit.ac.in
- Phone: 7349784480
- Campus: NMIT, Bengaluru

---

## 🎉 Ready to Use!

Your Campus Krishi application is now ready with:
- ✅ Order tracking
- ✅ Advanced search
- ✅ Admin analytics
- ✅ Inventory management
- ✅ Professional documentation

**Start serving customers better today!** 🌱

---

**Quick Start Version**: 1.0  
**Last Updated**: March 31, 2026  
**Status**: Production Ready

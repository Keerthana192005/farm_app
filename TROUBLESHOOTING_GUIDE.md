# 🔧 TROUBLESHOOTING GUIDE - Farm App

## Quick Problem Solver

---

## ⚠️ Common Issues & Solutions

### Issue: Admin options visible to regular users

**Problem:** Non-admin users can see "Admin Panel" in navbar

**Solution:**
```
Check Jinja2 template: templates/layout.html
Look for: {% if current_user.is_authenticated %}
Should be present to hide admin options
If missing, copy from working version

Line 49: {% if current_user.is_authenticated %}
Line 65: {% endif %}

If still showing:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Check if user is properly logged out
3. Restart Flask server
```

**Verification:**
- [ ] Non-logged user sees: Home, About, Vision, Process, Contact, Cart only
- [ ] Non-logged user sees "Admin Login" button where Admin Panel would be
- [ ] Logged-in admin sees: All menu items + Admin Panel dropdown

---

### Issue: Images not appearing on About Us page

**Problem:** Team member photos showing as broken images on About Us page

**Causes & Solutions:**

#### Solution 1: Image files missing
```
Check if files exist:
static/
└── uploads/
    ├── bhooswarga_garden.png
    ├── dr_sumaraj.png
    ├── byre_gowda.png
    ├── vishwadeep_k.jpg
    └── abhishek_r.jpg

If missing:
1. Go to Admin Dashboard → Manage Images
2. Upload images for each person
3. Check that upload was successful
```

#### Solution 2: Incorrect file paths
```
Check about.html line with image:
<img src="{{ url_for('static', filename='uploads/dr_sumaraj.png') }}">

Should be exactly:
{{ url_for('static', filename='uploads/FILENAME') }}

Not:
{{ url_for('static', filename='UPLOAD_FOLDER/FILENAME') }}
{{ url_for('static', filename='/uploads/FILENAME') }}
```

#### Solution 3: Missing uploads folder
```
Create if not exists:
static/
└── uploads/

On Linux/Mac:
mkdir -p static/uploads
chmod 755 static/uploads

On Windows:
Manually create "uploads" folder inside static/
```

#### Solution 4: Cache issue
```
1. Clear browser cache
2. Hard refresh: Ctrl+F5 (Windows) / Cmd+Shift+R (Mac)
3. Try in incognito mode
4. Check page source to verify image URL
```

**Verification:**
- [ ] All 5 team member images display
- [ ] Images are not broken/error images
- [ ] Images persist after page refresh
- [ ] Images visible in different browsers

---

### Issue: Star rating not working on contact form

**Problem:** Stars appear but clicking doesn't change rating

**Causes & Solutions:**

#### Solution 1: JavaScript error
```
Check browser console:
1. Open DevTools (F12)
2. Go to Console tab
3. Look for JavaScript errors
4. If errors appear, check templates/contact.html

Ensure JavaScript code exists at lines 195-220
Must include event listeners for star icons
```

#### Solution 2: Missing star icons HTML
```
Check contact.html around line 54:
<i class="fas fa-star star-icon" data-rating="1"></i>
<i class="fas fa-star star-icon" data-rating="2"></i>
<i class="fas fa-star star-icon" data-rating="3"></i>
<i class="fas fa-star star-icon" data-rating="4"></i>
<i class="fas fa-star star-icon" data-rating="5"></i>

Must have:
- class="star-icon"
- data-rating="1" through data-rating="5"
- All 5 stars
```

#### Solution 3: CSS issue
```
Check if stars are styled correctly in contact.html
Should have inline style:
style="cursor: pointer; font-size: 1.5rem; color: #ffc107;"

If not visible:
1. Add CSS class to style.css
2. Or add inline styles
3. Check font-awesome is loaded in layout.html
```

#### Solution 4: Hidden input not updated
```
Check HTML:
<input type="hidden" id="rating" name="rating" value="5">

JavaScript must update this:
document.getElementById('rating').value = rating;

If missing, form won't send rating
```

**Verification:**
- [ ] Stars are visible
- [ ] Click changes star color
- [ ] Hover shows orange color
- [ ] Rating text updates
- [ ] Form submits with rating value
- [ ] Rating appears in database

---

### Issue: No notifications appearing when order placed

**Problem:** Admin doesn't see notifications in dashboard or notifications page

**Causes & Solutions:**

#### Solution 1: Notification model not in database
```
Verify Notification table exists:
1. Go to database console/admin
2. Check tables list
3. Should see "notification" table

If missing:
1. Run: python shell
2. Execute: from app import db; db.create_all()
3. Restart Flask server

Or check models.py has:
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
```

#### Solution 2: Notification not created on checkout
```
Check app.py around line 302-308:
After db.session.commit() for order, should have:

notification = Notification(
    title=f'New Order #{order.id}',
    message=f'New order from {customer_name}: ₹{total} - {len(order_items_data)} items',
    type='order',
    order_id=order.id
)
db.session.add(notification)
db.session.commit()

If missing, add this code after order creation
```

#### Solution 3: Admin not viewing notifications
```
To see notifications, admin must:
1. Login with admin credentials
2. Visit /admin/ (dashboard)
3. Look for "New Notifications" alert
   OR
   Click "Notifications" in sidebar → /admin/notifications

If dashboard doesn't load:
- Check admin is logged in
- Visit /admin/notifications directly
```

#### Solution 4: Notifications exist but not showing
```
Check admin_dashboard.html:
Should have code around line 136-152:
{% if notifications %}
    <div class="alert alert-info">
        ...notifications display...
    </div>
{% endif %}

If missing:
1. Add notification display section
2. Pass notifications from route
3. Verify notifications variable in render_template
```

**Verification:**
- [ ] Place test order
- [ ] Check notifications table in database (should have new entry)
- [ ] Admin dashboard shows notification alert
- [ ] /admin/notifications page shows order
- [ ] Notification has correct order details

---

### Issue: Images not saving permanently

**Problem:** Uploaded images disappear after admin logs out or server restarts

**Causes & Solutions:**

#### Solution 1: Wrong upload location
```
Verify upload folder in config.py:
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

Should save to: static/uploads/
NOT to: /tmp/ (temporary)
NOT to: memory (RAM)
NOT to: session (request-scoped)

Check app.py upload_image():
save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_name)
file.save(save_path)  ← Should save to disk, not memory
```

#### Solution 2: Database-only storage
```
Images must be saved to FILE SYSTEM, not database

Check upload code doesn't do:
- Store as blob in database
- Save to memory
- Save to temp folder

Verify:
file.save(save_path)
↑ This saves to disk

Not:
db.session.add(file_content)
↑ This would be in-memory
```

#### Solution 3: Wrong filename
```
Check upload_image() uses correct mapping:
allowed_targets = {
    'bhooswarga': 'bhooswarga_garden.png',
    'dr_sumaraj': 'dr_sumaraj.png',
    'byre_gowda': 'byre_gowda.png',
    'vishwadeep_k': 'vishwadeep_k.jpg',
    'abhishek_r': 'abhishek_r.jpg'
}

NOT random filenames
NOT uploading with original name
NOT using timestamp/UUID
```

#### Solution 4: File permissions issue
```
On Linux/Mac - Check permissions:
ls -l static/uploads/

Should be readable/writable:
drwxr-xr-x (755)

Fix with:
chmod 755 static/uploads/
chmod 644 static/uploads/*

On Windows - Check folder properties:
Right-click uploads folder → Properties
→ Security tab → Permissions
→ Should have Write access
```

**Verification:**
- [ ] Upload image via admin panel
- [ ] Check file exists on disk (admin verify)
- [ ] Admin logs out and logs back in
- [ ] Image still visible on About Us page
- [ ] Restart Flask server (python app.py)
- [ ] Image still visible
- [ ] Image file still exists on disk

---

### Issue: Process page still shows "Current Crops & Practices"

**Problem:** Old section visible on process page

**Solution:**
```
Check templates/process.html:
1. Search file for "Current Crops"
2. Should find ZERO matches

If found:
1. Open process.html
2. Delete the entire section
3. Save file
4. Refresh browser (Ctrl+F5)

If still visible:
1. Clear browser cache
2. Check you edited correct file
3. Verify changes saved (file modified time)
4. Restart Flask server
```

**Verification:**
- [ ] Process page loads
- [ ] NO "Current Crops & Practices" section
- [ ] Only these sections visible:
  - What We Do
  - Community sections
  - Continuous Improvement
- [ ] Checked by searching file (not found)

---

## 🔍 Debug Checklist

### For Any Issue:

1. **Clear Cache**
   ```
   Browser: Ctrl+Shift+Delete → Clear all
   Hard Refresh: Ctrl+F5
   Try Incognito Mode: Ctrl+Shift+N
   ```

2. **Check Flask Console**
   ```
   Look for errors when accessing page
   Example: 404 Not Found, 500 Server Error
   Note the error message
   ```

3. **Check Browser Console**
   ```
   F12 → Console tab
   Look for JavaScript errors
   Look for network errors (red items)
   ```

4. **Verify File Exists**
   ```
   For images: Check static/uploads/ folder
   For templates: Check templates/ folder
   For code: Check app.py has correct route
   ```

5. **Restart Server**
   ```
   Stop Flask running (Ctrl+C)
   python app.py
   Try again
   ```

6. **Check Database**
   ```
   Error might be in database connection
   Verify SQLite/database file exists
   Try creating fresh database
   ```

---

## 📋 Testing Checklist

### After Any Change:

- [ ] Test in main browser (Chrome/Firefox)
- [ ] Test in incognito mode
- [ ] Test on mobile (responsive)
- [ ] Clear cache and test again
- [ ] Check browser console for errors
- [ ] Check Flask console for errors
- [ ] Verify database changes were saved
- [ ] Verify file changes on disk

---

## 🆘 Getting Help

### If Problem Persists:

1. **Gather Information**
   - What page/feature has issue?
   - What's the exact error message?
   - When did it start?
   - What did you change?

2. **Check Documentation**
   - FIXES_VERIFICATION.md
   - IMPLEMENTATION_CHECKLIST.md
   - CONFIGURATION_GUIDE.md
   - VISUAL_DIAGRAMS.md

3. **Review Code Comments**
   - app.py has inline comments
   - routes clearly labeled
   - error handling noted

4. **Test Individually**
   - Test admin login alone
   - Test image upload alone
   - Test feedback form alone
   - Test orders/notifications alone

---

## ✅ Health Check Commands

### Quick Status Check:

```bash
# Check if Flask runs
python app.py

# Check template syntax
python -m jinja2.ext -p templates/contact.html

# Check Python syntax
python -m py_compile app.py models.py

# Check database
sqlite3 instance/farm_app.db ".tables"

# Check uploads folder exists
ls -la static/uploads/  # Linux/Mac
dir static/uploads/     # Windows
```

---

## 💡 Pro Tips

1. **Use browser DevTools**
   - F12 to open
   - Check Elements tab for HTML
   - Check Network tab for failed requests
   - Check Console tab for errors

2. **Check File Paths**
   - Always use absolute paths for debugging
   - Use url_for() for URLs
   - Use os.path.join() for file paths

3. **Test in Stages**
   - Test one feature at a time
   - Isolate problems
   - Test again after any change

4. **Keep Backups**
   - Before major changes
   - Of working code
   - Of database

5. **Use Logging**
   - Add print() statements
   - Check Flask debug output
   - Review logs regularly

---

## 📞 When to Restart

You need to **restart Flask server** after:
- [ ] Changing app.py
- [ ] Changing models.py  
- [ ] Changing config.py
- [ ] Installing new packages
- [ ] Modifying database in code

You DON'T need to restart after:
- [ ] Changing templates (HTML)
- [ ] Changing static assets (CSS/JS)
- [ ] Uploading images
- [ ] Database data changes

---

Generated: April 1, 2026
Status: ✅ Ready to Use


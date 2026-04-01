# Farm App - Quick Feature Guide

## 👤 User Features

### 1. Browse & Order Vegetables
- Homepage shows all available products
- Add items to cart and checkout
- Multiple payment methods: UPI, QR Code, Cash on Delivery

### 2. Feedback with Star Rating
- Visit Contact page
- Fill feedback form with message
- **Select 1-5 stars** to rate your experience
- Ratings are stored and help improve service

### 3. View About Us Page
- See team member photos
- Learn about Bhooswarga initiative
- All images are permanent and persist across sessions

---

## 🔐 Admin Features

### 1. Login to Admin Panel
- Go to navbar and click "Admin Login" (only visible when not logged in)
- Default admin credentials:
  - **Username:** admin
  - **Password:** admin123

### 2. Manage Team Images
- Navigate: Admin Dashboard → Manage Images
- Upload new photos for:
  - Bhooswarga Garden
  - Dr. Sumaraj
  - Byre Gowda
  - Vishwadeep K
  - Abhishek R
- Images are automatically saved to `static/uploads/`
- These images appear on the About Us page

### 3. View Order Notifications
- **Quick View:** Admin Dashboard shows latest unread notifications
- **Full View:** Click "View All Notifications" 
  - See complete list of all orders
  - Mark notifications as read
  - Each notification links to order details

### 4. Manage Products
- Add new vegetables
- Edit product details
- Set prices and stock quantities
- Upload product images

### 5. View Analytics & Reports
- Dashboard displays:
  - Total orders count
  - Pending orders count
  - Recent feedback with ratings
  - Total products in system

---

## 💾 Data Persistence

### Images
- **Location:** `static/uploads/` folder
- **Persistence:** Permanent (survives website restarts)
- **Types:** PNG, JPG, GIF supported

### Feedback & Ratings
- **Storage:** Database (SQLite/PostgreSQL)
- **Data Retained:** User name, email, message, star rating, timestamp

### Orders & Notifications
- **Storage:** Database
- **Auto-Created:** When user completes checkout
- **Contents:** Order ID, customer name, total amount, items count

---

## 🚀 Key Routes

| Page | URL | Accessible To |
|------|-----|---|
| Home | `/` | Everyone |
| About Us | `/about` | Everyone |
| Our Process | `/process` | Everyone |
| Contact & Feedback | `/contact` | Everyone |
| Cart | `/cart` | Everyone |
| Checkout | `/checkout` | Customers |
| Admin Login | `/admin/login` | Not Logged In |
| Admin Dashboard | `/admin/` | Admin Only |
| Manage Images | `/admin/images` | Admin Only |
| Notifications | `/admin/notifications` | Admin Only |
| Products Management | `/admin/products` | Admin Only |

---

## ⚙️ Important Notes

### Security
- Admin panel is **protected** - only accessible after login
- Regular users **cannot see** admin options in navbar
- Admin options only appear after successful authentication

### Image Management
- Images uploaded through admin panel are **permanent**
- They display on About Us page for all users
- No need to re-upload after website restarts

### Notifications
- Created **automatically** when orders are placed
- Appear in Admin Dashboard immediately
- Admin can mark them as read
- Linked to specific order details

### Feedback Ratings
- Default rating: 5 stars
- User can select 1-5 stars interactively
- Visual feedback with color changes
- Stored in database with feedback message

---

## 📱 Mobile Responsive
- All pages are mobile-friendly
- Works on phones, tablets, and desktops
- Bootstrap 5 framework for responsive design

---

## 🔄 Workflow Example: Placing an Order

1. User browses vegetables on homepage
2. Adds items to cart
3. Clicks checkout
4. Fills delivery details and selects payment method
5. **Notification automatically created for admin** ✅
6. **Admin sees notification in dashboard** ✅
7. Admin can view order details via notification
8. Customer receives order confirmation

---

## 🔄 Workflow Example: Uploading Team Photo

1. Admin logs in → Admin Dashboard
2. Clicks "Manage Images" in sidebar
3. Selects the person to replace photo for
4. Clicks "Choose File" and selects new image
5. Clicks "Upload"
6. Photo saved permanently to `static/uploads/`
7. **Photo appears immediately on About Us page** ✅
8. Photo persists even after admin logs out ✅

---

## ✅ All Features Working

- [x] Admin visibility properly restricted
- [x] Image uploads permanent and persistent
- [x] 5-star rating selector active in feedback form
- [x] Order notifications created automatically
- [x] Admin dashboard shows notifications
- [x] Current Crops section removed from process page

**No additional fixes needed!**


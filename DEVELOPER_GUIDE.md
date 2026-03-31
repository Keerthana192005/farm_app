# Campus Krishi - Developer Guide

## 🏗️ Project Architecture

### **Technology Stack**
- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS + Chart.js
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug

---

## 📁 Project Structure

```
farm_app/
├── app.py                 # Main Flask application (700+ lines)
├── models.py              # Database models (Admin, Vegetable, Order, etc.)
├── config.py              # Configuration (Dev, Prod, Test)
├── utils.py               # Utility functions (QR code generation)
├── requirements.txt       # Python dependencies
├── wsgi.py                # WSGI entry point for deployment
│
├── templates/             # HTML templates
│   ├── layout.html        # Base template with navigation
│   ├── home.html          # Home page
│   ├── track_order.html   # Order tracking (NEW)
│   ├── checkout.html      # Checkout form
│   ├── cart.html          # Shopping cart
│   ├── admin_dashboard.html       # Admin home
│   ├── admin_analytics.html       # Analytics (NEW)
│   ├── admin_inventory.html       # Inventory (NEW)
│   ├── admin_products.html        # Product management
│   └── ... (other templates)
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   └── main.js        # Client-side scripts
│   ├── uploads/           # User uploaded images
│   └── images/            # Static images
│
└── instance/              # Instance-specific files (database, etc.)
```

---

## 🔌 API Endpoints Reference

### **Customer APIs**

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/` | Home page | No |
| GET | `/api/vegetables` | All vegetables JSON | No |
| GET | `/api/search` | Search/filter vegetables | No |
| GET | `/api/cart-count` | Cart item count | No |
| GET | `/cart` | Cart page | No |
| POST | `/update_cart` | Update cart items | No |
| GET | `/add_to_cart/<id>` | Add to cart | No |
| GET | `/remove_from_cart/<id>` | Remove from cart | No |
| GET | `/checkout` | Checkout form | No |
| POST | `/checkout` | Place order | No |
| GET | `/track_order` | Order tracking page | No |
| POST | `/track_order` | Search order | No |

### **Admin APIs**

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET/POST | `/admin/login` | Admin login | No |
| GET | `/admin/dashboard` | Dashboard | Yes |
| GET | `/admin/analytics` | Analytics | Yes |
| GET | `/admin/api/sales-chart` | Sales data JSON | Yes |
| GET | `/admin/api/product-chart` | Product data JSON | Yes |
| GET | `/admin/inventory-management` | Inventory page | Yes |
| GET | `/admin/products` | Product list | Yes |
| GET/POST | `/admin/add_product` | Add product | Yes |
| GET/POST | `/admin/edit_product/<id>` | Edit product | Yes |
| GET | `/admin/delete_product/<id>` | Delete product | Yes |
| GET | `/admin/customers` | Customer list | Yes |
| GET | `/admin/reports` | Reports | Yes |
| GET | `/admin/images` | Image manager | Yes |
| GET | `/admin/change_password` | Change password | Yes |
| GET | `/admin/logout` | Logout | Yes |

---

## 📊 Database Models

### **Admin**
```python
id (Integer, Primary Key)
username (String, Unique)
password_hash (String)
```

### **Vegetable**
```python
id (Integer, Primary Key)
name (String)
price (Float)
stock (Integer)
image (String, Optional)
description (Text, Optional)
created_at (DateTime)
```

### **Order**
```python
id (Integer, Primary Key)
customer_name (String)
phone (String)
address (Text)
email (String, Optional)
total (Float)
status (String) # pending, confirmed, completed
payment_method (String) # cod, upi, razorpay, etc.
payment_status (String) # pending, completed
payment_id (String, Optional)
delivery_time (String, Optional)
order_notes (Text, Optional)
date (DateTime)
order_items (Relationship)
```

### **OrderItem**
```python
id (Integer, Primary Key)
order_id (Integer, ForeignKey)
vegetable_id (Integer, ForeignKey)
quantity (Integer)
price (Float)
vegetable (Relationship)
```

### **Feedback**
```python
id (Integer, Primary Key)
name (String)
email (String, Optional)
message (Text)
date (DateTime)
```

---

## 🔑 Key Functions & Implementation Details

### **Cart Management** (Client-side)
- Session-based cart storage `session['cart'] = {}`
- Real-time updates every 5 seconds
- Cart item count badge in navbar

### **Search & Filter** (`/api/search`)
```python
@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    sort_by = request.args.get('sort', 'name')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    
    # Filters vegetables by search term, price range
    # Returns JSON array of matching vegetables
```

### **Analytics** (`/admin/analytics`)
- Aggregates orders data
- Calculates metrics (revenue, orders, customers, etc.)
- Prepares data for Chart.js visualization
- Identifies low/out-of-stock items

### **Order Tracking** (`/track_order`)
- Searches by Order ID + Phone number
- Shows 4-step status flow
- Displays complete order details

---

## 🔧 Development Workflow

### **Setting Up Development Environment**

1. **Clone Repository**
   ```bash
   git clone <repo_url>
   cd farm_app
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   source venv/bin/activate       # Mac/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

5. **Run Development Server**
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

---

## 📝 Adding New Features

### **Example: Adding Product Reviews**

1. **Update Model** (`models.py`)
```python
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vegetable_id = db.Column(db.Integer, db.ForeignKey('vegetable.id'))
    customer_name = db.Column(db.String(100))
    rating = db.Column(db.Integer)  # 1-5
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
```

2. **Add Route** (`app.py`)
```python
@app.route('/add_review/<int:veg_id>', methods=['POST'])
def add_review(veg_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    customer_name = request.form.get('name')
    
    review = Review(
        vegetable_id=veg_id,
        customer_name=customer_name,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('home'))
```

3. **Create Template** (`templates/review_form.html`)
4. **Test Thoroughly**

---

## 🧪 Testing Guide

### **Manual Testing Checklist**

- [ ] Create admin account
- [ ] Add/Edit/Delete products
- [ ] Search products by name
- [ ] Filter by price
- [ ] Add products to cart
- [ ] Place order with COD
- [ ] Check order in pending status
- [ ] Update order to completed
- [ ] Track order with correct ID
- [ ] View analytics dashboard
- [ ] Check inventory management
- [ ] Verify charts load correctly

### **Automated Testing** (Future)
```python
# Example: test_models.py
import unittest
from app import app, db
from models import Order, Vegetable

class TestModels(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
    def test_vegetable_creation(self):
        veg = Vegetable(name='Test', price=100, stock=50)
        db.session.add(veg)
        db.session.commit()
        self.assertEqual(veg.name, 'Test')
```

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Set strong `SECRET_KEY`
- [ ] Use PostgreSQL instead of SQLite for production
- [ ] Set `SESSION_COOKIE_SECURE = True` for HTTPS
- [ ] Add error logging
- [ ] Set up backup strategy
- [ ] Configure email notifications
- [ ] Test on staging environment
- [ ] Monitor application performance
- [ ] Set up monitoring/alerting

---

## 📦 Dependencies Explanation

| Package | Purpose | Version |
|---------|---------|---------|
| Flask | Web framework | 2.3.3 |
| Flask-SQLAlchemy | ORM | 3.0.5 |
| Flask-Login | Authentication | 0.6.3 |
| Werkzeug | Security utilities | 2.3.7 |
| SQLAlchemy | Database toolkit | 2.0.36 |
| Pillow | Image processing | 9.5.0 |
| gunicorn | Production server | 21.2.0 |
| razorpay | Payment gateway | 1.2.0 |
| qrcode | QR code generation | 7.4.2 |

### **Future: Add for Analytics**
```
matplotlib==3.6.0    # Charts
pandas==1.5.0        # Data analysis
python-dateutil==2.8.2
PyPDF2==3.0.1        # PDF export
```

---

## 🐛 Common Issues & Solutions

### **Issue: Database locked**
```python
# Solution: Reset database
rm instance/database.db
python app.py  # Will recreate with seed data
```

### **Issue: Images not uploading**
```python
# Check: 
# 1. static/uploads folder exists
# 2. UPLOAD_FOLDER configured correctly
# 3. File permissions allow writes
```

### **Issue: Chart.js not loading**
```python
# Check browser console for:
# 1. CDN is accessible
# 2. JSON API returning correct data
# 3. Chart.js library loaded before chart code
```

### **Issue: Slow analytics page**
```python
# Solutions:
# 1. Add query limits: Order.query.limit(1000)
# 2. Cache results: @cache.cached(timeout=300)
# 3. Paginate large datasets
```

---

## 🔐 Security Best Practices

1. **Never commit secrets** to version control
2. **Validate all inputs** on backend (not just frontend)
3. **Use HTTPS** in production
4. **Store passwords** with proper hashing (werkzeug.security)
5. **Add CSRF protection** with `csrf_token` in forms
6. **Rate limit** login attempts
7. **Regular security audits** of dependencies

---

## 📚 Code Style Guide

- **Python**: Follow PEP 8
- **Naming**: snake_case for functions, CamelCase for classes
- **Comments**: Use meaningful comments, not obvious ones
- **Docstrings**: Add for complex functions
- **Line Length**: Max 100 characters
- **Indentation**: 4 spaces (no tabs)

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Update documentation
5. Create pull request
6. Wait for code review

---

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Chart.js Docs](https://www.chartjs.org/docs/latest/)
- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

**Last Updated**: March 31, 2026  
**Version**: 1.0  
**Maintainer**: Campus Krishi Team

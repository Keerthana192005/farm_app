# Farm Fresh Vegetables - Online Store

A complete production-ready full-stack web application for selling fresh vegetables online. Built with Python Flask, featuring real-time updates, shopping cart functionality, and admin panel.

## Features

### Customer Features
- **Browse Vegetables**: View today's fresh vegetables with real-time price and stock updates
- **Shopping Cart**: Add items to cart, update quantities, remove items
- **Price Comparison**: Compare our prices with market prices
- **Order Placement**: Complete checkout process with delivery information
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Prices and stock update automatically every 5 seconds

### Admin Features
- **Dashboard**: View orders, statistics, and recent feedback
- **Product Management**: Add, edit, delete vegetables
- **Stock Management**: Update stock levels and prices
- **Order Management**: View and manage customer orders
- **Image Upload**: Upload product images
- **Authentication**: Secure admin login system

### Technical Features
- **REST API**: `/api/vegetables` endpoint for real-time data
- **Session-based Cart**: Cart data stored in Flask sessions
- **Database**: SQLite with SQLAlchemy ORM
- **Responsive UI**: Bootstrap 5 with custom CSS
- **AJAX Updates**: Real-time price and stock updates
- **File Uploads**: Image upload functionality

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS with Fetch API
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug

## Project Structure

```
farm_app/
│
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── layout.html      # Base template
│   ├── home.html        # Home page
│   ├── vegetables.html  # Products listing
│   ├── cart.html        # Shopping cart
│   ├── checkout.html    # Checkout page
│   ├── about.html       # About us
│   ├── vision.html      # Vision & Mission
│   ├── process.html     # Our process
│   ├── gallery.html     # Photo gallery
│   ├── contact.html     # Contact page
│   ├── admin_login.html # Admin login
│   ├── admin_dashboard.html # Admin dashboard
│   ├── admin_products.html # Product management
│   ├── add_product.html # Add product form
│   └── edit_product.html # Edit product form
│
├── static/
│   ├── css/
│   │   └── style.css    # Custom CSS styles
│   ├── js/
│   │   └── main.js      # JavaScript functionality
│   └── uploads/         # Product images
│
└── database.db          # SQLite database (created automatically)
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone/Download the Project
```bash
# If you have the project files, navigate to the farm_app directory
cd farm_app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
- **Customer Site**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

### Default Admin Credentials
- **Username**: admin
- **Password**: admin123

## Database Setup

The application uses SQLite database which is created automatically when you first run the application. The database is seeded with 10 sample vegetables:

1. Tomatoes - ₹40/kg
2. Potatoes - ₹30/kg
3. Onions - ₹35/kg
4. Carrots - ₹45/kg
5. Spinach - ₹25/kg
6. Broccoli - ₹60/kg
7. Bell Peppers - ₹55/kg
8. Cucumbers - ₹35/kg
9. Cabbage - ₹28/kg
10. Cauliflower - ₹50/kg

## Usage Guide

### For Customers
1. Browse vegetables on the home page or vegetables page
2. Add items to cart using "Add to Cart" or "Quick Add" buttons
3. View cart and update quantities
4. Proceed to checkout and fill delivery details
5. Place order and receive confirmation

### For Admins
1. Login to admin panel using credentials
2. View dashboard for statistics and recent orders
3. Manage products (add, edit, delete)
4. Update stock levels and prices
5. View and manage customer orders
6. Upload product images

## API Endpoints

### GET /api/vegetables
Returns all vegetables with current prices and stock in JSON format.

**Response Format:**
```json
[
  {
    "id": 1,
    "name": "Tomatoes",
    "price": 40.0,
    "stock": 50,
    "image": "tomatoes.jpg",
    "description": "Fresh red tomatoes"
  }
]
```

## Configuration

### Environment Variables
You can configure the application using environment variables:

```bash
export SECRET_KEY='your-secret-key'
export FLASK_ENV='development'  # or 'production'
```

### Customization
- **Database**: Change `SQLALCHEMY_DATABASE_URI` in `app.py` for different databases
- **Upload Folder**: Modify `UPLOAD_FOLDER` configuration for image storage
- **Admin Credentials**: Update authentication logic in admin routes

## Deployment

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. Configure reverse proxy (Nginx) if needed
4. Set up SSL certificate for HTTPS

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t farm-fresh .
docker run -p 5000:5000 farm-fresh
```

## Features in Detail

### Real-time Updates
- Prices and stock levels update every 5 seconds automatically
- Visual indicators show when data is refreshed
- Cart updates in real-time without page refresh

### Shopping Cart
- Session-based cart persistence
- Quantity validation against stock
- Real-time price calculation
- Visual feedback for all actions

### Admin Panel
- Secure authentication system
- CRUD operations for products
- Order management dashboard
- Image upload with validation
- Statistics and analytics

### Responsive Design
- Mobile-first approach
- Bootstrap 5 components
- Custom CSS animations
- Accessibility features

## Security Features

- CSRF protection
- Session management
- Input validation
- File upload security
- SQL injection prevention
- XSS protection

## Performance Optimization

- Database indexing
- Efficient queries
- Image optimization
- CSS/JS minification ready
- Caching headers

## Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the documentation
- Review the code comments
- Test with sample data
- Contact development team

## License

This project is proprietary commercial software. All rights reserved.

© 2026 Campus Krishi. This software and its contents are protected by copyright law and international treaties. Unauthorized reproduction, distribution, or modification is strictly prohibited.

For licensing inquiries, please contact the development team.

---

**Happy Farming!** 🌱🥕🥦

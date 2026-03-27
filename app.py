from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, Vegetable, Order, OrderItem, Feedback, Admin
from config import config
from utils import generate_payment_qr_code

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    # Now define all routes using the created app
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Admin.query.get(int(user_id))
        except:
            return None

    @app.route('/')
    def home():
        try:
            vegetables = Vegetable.query.filter(Vegetable.stock > 0).all()
            return render_template('home.html', vegetables=vegetables)
        except Exception as e:
            # Database tables don't exist yet, show setup message
            return '''
            <div style="text-align: center; padding: 50px; font-family: Arial;">
                <h1>🌱 Campus Krishi Farm Store</h1>
                <p>Database needs to be set up first!</p>
                <a href="/setup" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Setup Database
                </a>
            </div>
            '''

    @app.route('/setup')
    def setup_database():
        """Simple database setup route"""
        try:
            # Create tables
            db.create_all()
            
            # Create admin if not exists
            if Admin.query.count() == 0:
                admin = Admin(username='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
            
            # Add vegetables if empty
            if Vegetable.query.count() == 0:
                vegetables = [
                    Vegetable(name='Tomatoes', price=40.0, stock=50, description='Fresh red tomatoes'),
                    Vegetable(name='Potatoes', price=30.0, stock=100, description='High quality potatoes'),
                    Vegetable(name='Onions', price=35.0, stock=75, description='Fresh onions'),
                    Vegetable(name='Carrots', price=45.0, stock=60, description='Sweet carrots'),
                    Vegetable(name='Spinach', price=25.0, stock=40, description='Fresh spinach'),
                ]
                for veg in vegetables:
                    db.session.add(veg)
                db.session.commit()
            
            return "Database setup complete! Admin: admin/admin123"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/vision')
    def vision():
        return render_template('vision.html')

    @app.route('/process')
    def process():
        return render_template('process.html')

    @app.route('/api/vegetables')
    def api_vegetables():
        try:
            vegetables = Vegetable.query.all()
            result = []
            for veg in vegetables:
                result.append({
                    'id': veg.id,
                    'name': veg.name,
                    'price': veg.price,
                    'stock': veg.stock,
                    'image': veg.image,
                    'description': veg.description
                })
            return jsonify(result)
        except Exception as e:
            return jsonify([])

    @app.route('/api/cart-count')
    def api_cart_count():
        cart = session.get('cart', {})
        return jsonify({'count': len(cart)})

    @app.route('/cart')
    def cart():
        try:
            cart_items = session.get('cart', {})
            cart_total = 0
            cart_details = []
            
            for veg_id, item in cart_items.items():
                vegetable = Vegetable.query.get(int(veg_id))
                if vegetable:
                    subtotal = vegetable.price * item['quantity']
                    cart_total += subtotal
                    cart_details.append({
                        'vegetable': vegetable,
                        'quantity': item['quantity'],
                        'subtotal': subtotal
                    })
            
            return render_template('cart.html', cart_items=cart_details, cart_total=cart_total)
        except:
            return render_template('cart.html', cart_items=[], cart_total=0)

    @app.route('/add_to_cart/<int:veg_id>')
    def add_to_cart(veg_id):
        try:
            vegetable = Vegetable.query.get_or_404(veg_id)
            
            if 'cart' not in session:
                session['cart'] = {}
            
            cart = session['cart']
            if str(veg_id) in cart:
                cart[str(veg_id)]['quantity'] += 1
            else:
                cart[str(veg_id)] = {'quantity': 1}
            
            session.modified = True
            flash(f'{vegetable.name} added to cart!', 'success')
            return redirect(url_for('home'))
        except:
            flash('Item not available', 'error')
            return redirect(url_for('home'))

    @app.route('/checkout')
    def checkout():
        try:
            cart_items = session.get('cart', {})
            if not cart_items:
                flash('Your cart is empty!', 'warning')
                return redirect(url_for('cart'))
            
            cart_total = 0
            cart_details = []
            
            for veg_id, item in cart_items.items():
                vegetable = Vegetable.query.get(int(veg_id))
                if vegetable:
                    subtotal = vegetable.price * item['quantity']
                    cart_total += subtotal
                    cart_details.append({
                        'vegetable': vegetable,
                        'quantity': item['quantity'],
                        'subtotal': subtotal
                    })
            
            return render_template('checkout.html', cart_items=cart_details, cart_total=cart_total)
        except:
            flash('Error loading checkout', 'error')
            return redirect(url_for('cart'))

    @app.route('/place_order', methods=['POST'])
    def place_order():
        try:
            cart_items = session.get('cart', {})
            if not cart_items:
                flash('Your cart is empty!', 'warning')
                return redirect(url_for('cart'))
            
            # Create order
            order = Order(
                customer_name=request.form.get('customer_name'),
                phone=request.form.get('phone'),
                address=request.form.get('address'),
                email=request.form.get('email'),
                total=0
            )
            
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Add order items
            total = 0
            for veg_id, item in cart_items.items():
                vegetable = Vegetable.query.get(int(veg_id))
                if vegetable:
                    order_item = OrderItem(
                        order_id=order.id,
                        vegetable_id=veg_id,
                        quantity=item['quantity'],
                        price=vegetable.price
                    )
                    db.session.add(order_item)
                    total += vegetable.price * item['quantity']
            
            order.total = total
            db.session.commit()
            
            # Clear cart
            session['cart'] = {}
            session.modified = True
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('payment', order_id=order.id))
        except Exception as e:
            flash('Error placing order', 'error')
            return redirect(url_for('checkout'))

    @app.route('/payment/<int:order_id>')
    def payment(order_id):
        try:
            order = Order.query.get_or_404(order_id)
            return render_template('payment.html', order=order)
        except:
            flash('Order not found', 'error')
            return redirect(url_for('home'))

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            try:
                admin = Admin.query.filter_by(username=username).first()
                if admin and admin.check_password(password):
                    login_user(admin)
                    flash('Login successful!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid credentials!', 'error')
            except:
                flash('Database error!', 'error')
        
        return render_template('admin_login.html')

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        try:
            # Get statistics
            total_orders = Order.query.count()
            pending_orders = Order.query.filter_by(status='pending').count()
            completed_orders = Order.query.filter_by(status='completed').count()
            total_revenue = db.session.query(db.func.sum(Order.total)).filter_by(status='completed').scalar() or 0
            
            # Get recent orders
            recent_orders = Order.query.order_by(Order.date.desc()).limit(5).all()
            
            return render_template('admin_dashboard.html', 
                                 total_orders=total_orders,
                                 pending_orders=pending_orders,
                                 completed_orders=completed_orders,
                                 total_revenue=total_revenue,
                                 recent_orders=recent_orders)
        except:
            return render_template('admin_dashboard.html', 
                                 total_orders=0,
                                 pending_orders=0,
                                 completed_orders=0,
                                 total_revenue=0,
                                 recent_orders=[])

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        flash('Logged out successfully!', 'success')
        return redirect(url_for('admin_login'))

    return app

# Create app instance for local development
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)

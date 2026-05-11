from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, Vegetable, Order, OrderItem, Feedback
from config import config

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'

    class Admin(UserMixin):
        def __init__(self, id):
            self.id = id

    @login_manager.user_loader
    def load_user(user_id):
        return Admin(user_id)

    @app.route('/')
    def home():
        vegetables = Vegetable.query.filter(Vegetable.stock > 0).all()
        return render_template('home.html', vegetables=vegetables)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/vision')
    def vision():
        return render_template('vision.html')

    @app.route('/process')
    def process():
        return render_template('process.html')

    @app.route('/vegetables')
    def vegetables():
        vegetables = Vegetable.query.all()
        return render_template('vegetables.html', vegetables=vegetables)

    @app.route('/api/vegetables')
    def api_vegetables():
        vegetables = Vegetable.query.all()
        return jsonify([veg.to_dict() for veg in vegetables])

    @app.route('/cart')
    def cart():
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

    @app.route('/add_to_cart/<int:veg_id>')
    def add_to_cart(veg_id):
        vegetable = Vegetable.query.get_or_404(veg_id)
        
        if vegetable.stock <= 0:
            flash('This vegetable is out of stock!', 'error')
            return redirect(url_for('vegetables'))
        
        cart = session.get('cart', {})
        
        if str(veg_id) in cart:
            if cart[str(veg_id)]['quantity'] < vegetable.stock:
                cart[str(veg_id)]['quantity'] += 1
                flash(f'{vegetable.name} added to cart!', 'success')
            else:
                flash(f'Only {vegetable.stock} {vegetable.name}(s) available in stock!', 'error')
        else:
            cart[str(veg_id)] = {'quantity': 1}
            flash(f'{vegetable.name} added to cart!', 'success')
        
        session['cart'] = cart
        return redirect(url_for('vegetables'))

    @app.route('/update_cart', methods=['POST'])
    def update_cart():
        veg_id = request.form.get('veg_id')
        quantity = request.form.get('quantity', type=int)
        
        if quantity <= 0:
            cart = session.get('cart', {})
            if str(veg_id) in cart:
                del cart[str(veg_id)]
            session['cart'] = cart
            return jsonify({'success': True, 'message': 'Item removed from cart'})
        
        vegetable = Vegetable.query.get(veg_id)
        if not vegetable or quantity > vegetable.stock:
            return jsonify({'success': False, 'message': 'Invalid quantity or insufficient stock'})
        
        cart = session.get('cart', {})
        cart[str(veg_id)] = {'quantity': quantity}
        session['cart'] = cart
        
        # Calculate new totals
        cart_total = 0
        for item_veg_id, item in cart.items():
            veg = Vegetable.query.get(int(item_veg_id))
            if veg:
                cart_total += veg.price * item['quantity']
        
        return jsonify({
            'success': True, 
            'message': 'Cart updated',
            'subtotal': vegetable.price * quantity,
            'cart_total': cart_total
        })

    @app.route('/remove_from_cart/<int:veg_id>')
    def remove_from_cart(veg_id):
        cart = session.get('cart', {})
        if str(veg_id) in cart:
            del cart[str(veg_id)]
            session['cart'] = cart
            flash('Item removed from cart!', 'success')
        return redirect(url_for('cart'))

    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        cart_items = session.get('cart', {})
        
        if not cart_items:
            flash('Your cart is empty!', 'error')
            return redirect(url_for('cart'))
        
        if request.method == 'POST':
            customer_name = request.form.get('customer_name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            
            if not all([customer_name, phone, address]):
                flash('Please fill in all fields!', 'error')
                return redirect(url_for('checkout'))
            
            # Calculate total and create order
            total = 0
            order_items_data = []
            
            for veg_id, item in cart_items.items():
                vegetable = Vegetable.query.get(int(veg_id))
                if vegetable:
                    subtotal = vegetable.price * item['quantity']
                    total += subtotal
                    order_items_data.append({
                        'vegetable': vegetable,
                        'quantity': item['quantity'],
                        'price': vegetable.price
                    })
                    
                    # Update stock
                    vegetable.stock -= item['quantity']
            
            # Create order
            order = Order(
                customer_name=customer_name,
                phone=phone,
                address=address,
                total=total
            )
            db.session.add(order)
            db.session.commit()
            
            # Create order items
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    vegetable_id=item_data['vegetable'].id,
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Clear cart
            session['cart'] = {}
            
            flash(f'Order placed successfully! Order ID: {order.id}', 'success')
            return redirect(url_for('home'))
        
        # Calculate total for display
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

    @app.route('/gallery')
    def gallery():
        vegetables = Vegetable.query.all()
        return render_template('gallery.html', vegetables=vegetables)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            if not all([name, message]):
                flash('Please fill in required fields!', 'error')
                return redirect(url_for('contact'))
            
            feedback = Feedback(name=name, email=email, message=message)
            db.session.add(feedback)
            db.session.commit()
            
            flash('Thank you for your feedback! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        
        return render_template('contact.html')

    # Admin routes
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        admin_user = os.environ.get('ADMIN_USERNAME')
        admin_pass = os.environ.get('ADMIN_PASSWORD')

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if admin_user and admin_pass and username == admin_user and password == admin_pass:
                admin = Admin(1)
                login_user(admin)
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            elif not admin_user or not admin_pass:
                flash('Admin login is not configured. Please set ADMIN_USERNAME and ADMIN_PASSWORD.', 'error')
            else:
                flash('Invalid credentials!', 'error')

        return render_template('admin_login.html')

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        flash('Logged out successfully!', 'success')
        return redirect(url_for('admin_login'))

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        try:
            orders = Order.query.order_by(Order.date.desc()).all()
            total_orders = Order.query.count()
            pending_orders = Order.query.filter_by(status='pending').count()
            feedbacks = Feedback.query.order_by(Feedback.date.desc()).limit(5).all()
            total_vegetables = Vegetable.query.count()
        except Exception as e:
            # Handle case where tables don't exist yet
            print(f"Database error: {e}")
            orders = []
            total_orders = 0
            pending_orders = 0
            feedbacks = []
            total_vegetables = 0
        
        return render_template('admin_dashboard.html', 
                             orders=orders, 
                             total_orders=total_orders,
                             pending_orders=pending_orders,
                             feedbacks=feedbacks,
                             total_vegetables=total_vegetables)

    @app.route('/admin/products')
    @login_required
    def admin_products():
        try:
            vegetables = Vegetable.query.all()
        except Exception as e:
            print(f"Database error: {e}")
            vegetables = []
        return render_template('admin_products.html', vegetables=vegetables)

    @app.route('/admin/add_product', methods=['GET', 'POST'])
    @login_required
    def add_product():
        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price', type=float)
            stock = request.form.get('stock', type=int)
            description = request.form.get('description')
            
            if not all([name, price, stock]):
                flash('Please fill in all required fields!', 'error')
                return redirect(url_for('add_product'))
            
            # Handle image upload
            image = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image = filename
            
            vegetable = Vegetable(
                name=name,
                price=price,
                stock=stock,
                image=image,
                description=description
            )
            db.session.add(vegetable)
            db.session.commit()
            
            flash(f'{name} added successfully!', 'success')
            return redirect(url_for('admin_products'))
        
        return render_template('add_product.html')

    @app.route('/admin/edit_product/<int:veg_id>', methods=['GET', 'POST'])
    @login_required
    def edit_product(veg_id):
        vegetable = Vegetable.query.get_or_404(veg_id)
        
        if request.method == 'POST':
            vegetable.name = request.form.get('name')
            vegetable.price = request.form.get('price', type=float)
            vegetable.stock = request.form.get('stock', type=int)
            vegetable.description = request.form.get('description')
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    vegetable.image = filename
            
            db.session.commit()
            flash(f'{vegetable.name} updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        
        return render_template('edit_product.html', vegetable=vegetable)

    @app.route('/admin/delete_product/<int:veg_id>')
    @login_required
    def delete_product(veg_id):
        vegetable = Vegetable.query.get_or_404(veg_id)
        db.session.delete(vegetable)
        db.session.commit()
        flash(f'{vegetable.name} deleted successfully!', 'success')
        return redirect(url_for('admin_products'))

    @app.route('/admin/update_order_status/<int:order_id>')
    @login_required
    def update_order_status(order_id):
        order = Order.query.get_or_404(order_id)
        order.status = 'completed'
        db.session.commit()
        flash(f'Order {order_id} marked as completed!', 'success')
        return redirect(url_for('admin_dashboard'))

    # Initialize database and seed data
    def create_tables_and_seed():
        with app.app_context():
            db.create_all()
            
            # Seed data if database is empty
            if Vegetable.query.count() == 0:
                seed_data = [
                    {'name': 'Tomatoes', 'price': 40.0, 'stock': 50, 'description': 'Fresh red tomatoes from our farm'},
                    {'name': 'Potatoes', 'price': 30.0, 'stock': 100, 'description': 'High quality potatoes'},
                    {'name': 'Onions', 'price': 35.0, 'stock': 75, 'description': 'Fresh onions'},
                    {'name': 'Carrots', 'price': 45.0, 'stock': 60, 'description': 'Sweet and crunchy carrots'},
                    {'name': 'Spinach', 'price': 25.0, 'stock': 40, 'description': 'Fresh green spinach'},
                    {'name': 'Broccoli', 'price': 60.0, 'stock': 30, 'description': 'Organic broccoli'},
                    {'name': 'Bell Peppers', 'price': 55.0, 'stock': 45, 'description': 'Colorful bell peppers'},
                    {'name': 'Cucumbers', 'price': 35.0, 'stock': 55, 'description': 'Fresh cucumbers'},
                    {'name': 'Cabbage', 'price': 28.0, 'stock': 35, 'description': 'Green cabbage'},
                    {'name': 'Cauliflower', 'price': 50.0, 'stock': 25, 'description': 'Fresh cauliflower'}
                ]
                
                for data in seed_data:
                    vegetable = Vegetable(**data)
                    db.session.add(vegetable)
                
                db.session.commit()
                print("Database seeded with sample vegetables!")

    return app

# Create app instance for deployment
app = create_app()

# Make the function available at module level
def create_tables_and_seed():
    with app.app_context():
        db.create_all()
        
        # Seed data if database is empty
        if Vegetable.query.count() == 0:
            seed_data = [
                {'name': 'Tomatoes', 'price': 40.0, 'stock': 50, 'description': 'Fresh red tomatoes from our farm'},
                {'name': 'Potatoes', 'price': 30.0, 'stock': 100, 'description': 'High quality potatoes'},
                {'name': 'Onions', 'price': 35.0, 'stock': 75, 'description': 'Fresh onions'},
                {'name': 'Carrots', 'price': 45.0, 'stock': 60, 'description': 'Sweet and crunchy carrots'},
                {'name': 'Spinach', 'price': 25.0, 'stock': 40, 'description': 'Fresh green spinach'},
                {'name': 'Broccoli', 'price': 60.0, 'stock': 30, 'description': 'Organic broccoli'},
                {'name': 'Bell Peppers', 'price': 55.0, 'stock': 45, 'description': 'Colorful bell peppers'},
                {'name': 'Cucumbers', 'price': 35.0, 'stock': 55, 'description': 'Fresh cucumbers'},
                {'name': 'Cabbage', 'price': 28.0, 'stock': 35, 'description': 'Green cabbage'},
                {'name': 'Cauliflower', 'price': 50.0, 'stock': 25, 'description': 'Fresh cauliflower'}
            ]
            
            for data in seed_data:
                vegetable = Vegetable(**data)
                db.session.add(vegetable)
            
            db.session.commit()
            print("Database seeded with sample vegetables!")

if __name__ == '__main__':
    create_tables_and_seed()
    app.run(debug=True, host='127.0.0.1', port=8080)

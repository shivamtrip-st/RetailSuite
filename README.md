# E-Commerce Platform
A full-featured e-commerce platform built with Django, featuring Stripe payment integration, comprehensive inventory management, and a powerful admin panel.

## 📋 Features

### 🛒 Shopping Experience
- User-friendly product browsing and searching
- Product categories and filtering
- Shopping cart functionality
- User reviews and ratings

### 💳 Payment Processing
- Secure checkout with Stripe integration
- Order tracking system

### 📦 Inventory Management
- Real-time stock tracking
- Low stock analyzing

### 👑 Admin Panel
- Comprehensive dashboard with sales analytics
- Comprehensive dashboard with Category analytics
- Customer Order management
- Review and sentiment analysis
- Low stock product analysis

## 📸 Screenshots

### Homepage
![Screenshot 2025-05-03 234742](https://github.com/user-attachments/assets/51c49bfb-d5f0-4f36-b9fe-45461967abdd)
*Clean, modern interface showcasing featured products and categories.*

### Product Page
![Screenshot 2025-05-04 121054](https://github.com/user-attachments/assets/6bdfa5de-f861-4dab-90bd-4210cc1bcf33)
*Detailed product information with high-quality images and customer reviews.*

### Shopping Cart
![Screenshot 2025-05-03 235552](https://github.com/user-attachments/assets/a4ef97c3-870e-4c0c-8b23-b20b2950d247)
*Intuitive cart interface with quantity adjustments and price calculations.*

### Admin Dashboard
![Screenshot 2025-05-04 000038](https://github.com/user-attachments/assets/b8f132b2-b4c4-4d3c-ac14-a9b18c8b5dce)
*Powerful admin interface with sales metrics and inventory insights.*

### Inventory Management
![Screenshot 2025-05-04 000011](https://github.com/user-attachments/assets/34d3fa7d-4c58-4991-a9a5-c51f4b1ba2c4)
*Comprehensive inventory control system with filtering and bulk actions.*

## 🔧 Tech Stack

- **Backend**: Django
- **Database**: SQLite (Development)
- **Payment Processing**: Stripe API
- **Frontend**: HTML, CSS, JavaScript
- **Media Storage**: Django Media Framework
- **Authentication**: Django Authentication System

## 📥 Installation

1. Clone the repository:
   ```
   git clone https://github.com/shivamtrip-st/RetailSuite.git
   cd RetailSuite
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv virtual
   source virtual/bin/activate  # On Windows: virtual\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit .env with your configuration, including Stripe keys:
   ```
   STRIPE_PUBLIC_KEY=your_public_key
   STRIPE_SECRET_KEY=your_secret_key
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Load sample product data:
   ```
   python manage.py product_seed
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

9. Access the website at `http://localhost:8000/` and admin panel at `http://localhost:8000/admin/`

## 💾 Data Management

### Product Data
There are two ways to manage products in the system:

1. **Seed Command**: Load sample product data using the custom management command:
   ```
   python manage.py product_seed
   ```

2. **Admin Panel**: Use the Django admin interface at `/admin/` to manually add products, categories, and inventory items.

## 👥 User Roles and Access

### Admin Users
Administrators have access to:
- Complete inventory management system
- Order tracking and fulfillment (shipped/unshipped orders)
- Analytics dashboard with sales and category metrics
- Customer management tools
- Product and category management
- Review moderation

### Regular Users
Regular customers can:
- Browse and search products
- Add items to cart and complete checkout
- View their own order history and status
- Submit product reviews
- Manage their account information

## 📬 Contact

Project Link: [https://github.com/shivamtrip-st/RetailSuite](https://github.com/shivamtrip-st/RetailSuite)

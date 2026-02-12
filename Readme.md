# SS Bags E-commerce Platform

A complete e-commerce solution for bags and accessories with FastAPI backend and vanilla JavaScript frontend.

## Project Structure

```
project-root/
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # Pydantic models
│   │   ├── auth.py              # Authentication logic
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   └── routers/
│   │       ├── users.py         # User endpoints
│   │       ├── products.py      # Product endpoints
│   │       ├── orders.py        # Order endpoints
│   │       └── admin.py         # Admin endpoints
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   ├── combined_database.sql    # Database schema
│   └── README.md                # Backend documentation
│
├── frontend/                     # Static frontend files
│   ├── public/
│   │   ├── index.html           # User panel
│   │   └── admin.html           # Admin panel
│   ├── css/
│   │   ├── UserPannel.css       # User styles
│   │   └── AdminPannel.css      # Admin styles
│   ├── js/
│   │   ├── UserPannel.js        # User functionality
│   │   └── AdminPannel.js       # Admin functionality
│   ├── assets/
│   │   ├── images/              # Product images
│   │   └── videos/              # Video assets
│   └── README.md                # Frontend documentation
│
└── README.md                     # This file
```

## ✨ Features
- **User Management**: Registration, login, and profile management
- **Admin Panel**: Complete product and order management dashboard
- **Shopping Cart**: Add, remove, and update cart items
- **Order System**: Order placement, tracking, and status updates
- **Product Catalog**: Categorization, filtering, and search functionality
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Secure Authentication**: JWT-based security system

## 🛠️ Tech Stack
- **Backend**: FastAPI, Python 3.8+
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: JWT tokens
- **API Documentation**: Swagger/OpenAPI

## Security Improvements Made

### 1. JWT Secret Key Security
- Replaced default secret key with a strong, randomly generated key
- Changed from `your-super-secret-key-change-this-to-a-very-long-random-string-please` to a production-ready key

### 2. Database Security
- Updated default database credentials from root/root to more secure defaults
- Added proper foreign key constraints for data integrity
- Increased image URL field lengths to prevent truncation

### 3. Schema Normalization
- Created a unified database schema with proper foreign key relationships
- Both `category` (name) and `category_id` (foreign key) are maintained for backward compatibility
- Proper indexes added for performance optimization

### 4. Connection Management
- Improved database connection handling with proper try/finally blocks
- Fixed cursor dictionary mode issues in product creation/updating endpoints

### 5. CORS Configuration
- Enhanced CORS middleware to support development mode with wildcard origins
- Added proper OPTIONS method handlers for authentication endpoints
- Configured to allow all necessary HTTP methods

### 6. Frontend Security
- Implemented conditional API_BASE to handle mixed protocol issues
- Added proper error handling with user feedback
- Token storage and validation improvements

## 📋 System Requirements

### Required Software
- **Python**: Version 3.8 or higher
- **MySQL**: Version 8.0 or higher (or MariaDB 10.4+)
- **Git**: For cloning the repository
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### Recommended Development Tools
- **Code Editor**: VS Code, PyCharm, or similar
- **Database Tool**: MySQL Workbench
- **API Testing**: Postman or similar REST client

### Hardware Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: Minimum 2GB free space
- **Processor**: Any modern CPU

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=ss_bags
DB_PORT=3306
SECRET_KEY=your-super-secret-key
FRONTEND_URL=http://localhost:3000
DEV_MODE=true
```

4. Set up database:
```bash
mysql -u root -p ss_bags < combined_database.sql
```

5. Run the backend:
```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

The frontend consists of static HTML, CSS, and JavaScript files. Simply open the HTML files in a browser or serve them with a web server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000

# Or using Node.js serve
npx serve -s public -l 3000
```

The frontend will be available at `http://localhost:3000`

## 🔧 Default Login Credentials
```
Admin Login:
Username: admin
Password: admin123

User Registration:
Use the registration form to create new user accounts
```

## Environment Variables
Create a `.env` file with the following variables:
- `SECRET_KEY`: Your JWT secret key
- `DB_HOST`: Database host (default: localhost)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name (default: ss_bags)
- `DB_PORT`: Database port (default: 33006)
- `DEV_MODE`: Development mode flag (default: true)
- `FRONTEND_URL`: Frontend URL for CORS (default: http://localhost:3000)

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/admin/login` - Admin login

### Products
- `GET /api/products` - Get all products
- `POST /api/products` - Create product (admin only)
- `PUT /api/products/{id}` - Update product (admin only)
- `DELETE /api/products/{id}` - Delete product (admin only)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders/user/{id}` - Get user orders
- `GET /api/admin/orders` - Get all orders (admin only)
- `PUT /api/admin/orders/{id}` - Update order status (admin only)

### Categories
- `GET /api/categories` - Get all categories

## Admin Panel
Access the admin panel at `AdminPannel.html` using admin credentials.

## Production Deployment Notes
1. Change `DEV_MODE` to `false` in production
2. Update `FRONTEND_URL` to your production domain
3. Use strong, unique values for all security-related environment variables
4. Implement SSL/TLS for secure connections
5. Regularly update dependencies

## License
This project is licensed under the MIT License.

## 📁 Project Structure
pk-shop-ecommerce/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── combined_database.sql   # Database schema and sample data
├── .env                   # Environment variables (create this)
├── index.html             # Main website frontend
├── AdminPannel.html       # Admin dashboard frontend
├── css/
│   └── style.css          # Stylesheets
├── js/
│   └── script.js          # Frontend JavaScript
├── images/                # Product images and assets
└── README.md              # This documentation file

## 🎯 How to Use the Application

### For Customers
1. **Browse Products**: Visit the main website to view available bags and accessories
2. **Register Account**: Click "Sign Up" to create a new account
3. **Login**: Use your credentials to access your account
4. **Add to Cart**: Select products and add them to your shopping cart
5. **Checkout**: Proceed to checkout and place your order
6. **Track Orders**: View your order history and status in your account

### For Administrators
1. **Access Admin Panel**: Open `AdminPannel.html` in your browser
2. **Login**: Use admin credentials (admin/admin123 by default)
3. **Manage Products**: Add, edit, or delete products
4. **Manage Categories**: Organize products by categories
5. **View Orders**: Monitor and manage customer orders
6. **Update Order Status**: Change order status (pending, processing, shipped, delivered)

## 🔍 API Documentation
Once the server is running, visit `http://localhost:8000/docs` to explore the interactive API documentation using Swagger UI.
## UserPannel Running
http://127.0.0.1:3000/UserPannel.html
## AdminPannel Running
http://127.0.0.1:3000/AdminPannel.html
## ❌ Troubleshooting

### Common Issues and Solutions

**Problem: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
# Solution: Install missing dependencies
pip install fastapi uvicorn python-multipart mysql-connector-python python-jose[cryptography] passlib[bcrypt] python-dotenv
```

**Problem: "Access denied for user 'root'@'localhost'"**
```bash
# Solution: Check MySQL credentials and service status
# 1. Ensure MySQL is running
# 2. Verify username and password in .env file
# 3. Grant necessary permissions:
mysql -u root -p
GRANT ALL PRIVILEGES ON ss_bags.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

**Problem: "Can't connect to MySQL server"**
```bash
# Solution: Check MySQL service and port
# Windows: Check Services > MySQL
# Linux/Mac: sudo systemctl status mysql
# Verify port number in .env file (usually 3306)
```

**Problem: "CORS error in browser"**
```bash
# Solution: Check DEV_MODE setting in .env
DEV_MODE=true  # For development
# Or ensure FRONTEND_URL matches your frontend URL
```

**Problem: "JWT token invalid/expired"**
```bash
# Solution: Check SECRET_KEY in .env file
# Ensure it's the same on server restart
```

### Port Conflicts
If port 8000 is already in use:
```bash
# Use a different port
uvicorn main:app --reload --port 8001
# Update FRONTEND_URL in .env accordingly
```

## 🌐 Production Deployment

### Deployment Checklist
1. **Environment Setup**:
   - Set `DEV_MODE=false` in `.env`
   - Update `FRONTEND_URL` to your production domain
   - Use strong, unique values for all security variables

2. **Security Measures**:
   - Change default admin credentials
   - Implement SSL/TLS certificates
   - Use environment-specific database credentials
   - Enable firewall rules

3. **Performance Optimization**:
   - Use production-grade web server (Gunicorn/Nginx)
   - Enable database connection pooling
   - Implement caching strategies
   - Optimize images and static assets

4. **Monitoring & Maintenance**:
   - Set up logging and monitoring
   - Regular database backups
   - Update dependencies regularly
   - Monitor error logs

### Docker Deployment (Optional)
```dockerfile
# Create a Dockerfile for containerized deployment
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Check server logs for error messages
4. Verify all environment variables are correctly set

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
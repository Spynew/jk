# Frontend - SS Bags E-commerce

Frontend for the SS Bags e-commerce platform built with HTML, CSS, and JavaScript.

## Structure

```
frontend/
├── public/
│   ├── index.html           # User panel
│   └── admin.html           # Admin panel
├── css/
│   ├── UserPannel.css       # User panel styles
│   └── AdminPannel.css      # Admin panel styles
├── js/
│   ├── UserPannel.js        # User panel functionality
│   └── AdminPannel.js       # Admin panel functionality
└── assets/
    ├── images/              # Product and UI images
    └── videos/              # Video assets
```

## Features

### User Panel (index.html)
- Product browsing and filtering
- Shopping cart functionality
- Order placement
- User authentication
- Order history

### Admin Panel (admin.html)
- Product management (CRUD)
- Order management
- Customer management
- Sales reports and analytics
- Inventory management

## Configuration

Update the API base URL in JavaScript files to point to your backend:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Static Files

The frontend serves static files directly. Ensure your backend is configured to serve static files from the appropriate directories.

## Images

Product images are stored in `assets/images/` and should be optimized for web performance. Supported formats: JPG, PNG, GIF.

## Videos

Background videos and other video content are stored in `assets/videos/`.

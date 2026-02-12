-- ============ STEP 1: DROP & CREATE DATABASE ============
DROP DATABASE IF EXISTS ss_bags;
CREATE DATABASE ss_bags CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ss_bags;

-- ============ STEP 2: CREATE ALL TABLES WITH PROPER SCHEMA ============

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    status ENUM('active', 'inactive', 'blocked') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Categories Table (Only Bag Types)
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Products Table (Only Bags) - With normalized category_id from the start
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,           -- Kept for backward compatibility
    category_id INT NOT NULL,                 -- Proper foreign key reference
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    image_url VARCHAR(500),                   -- Increased length for longer URLs
    color VARCHAR(100),
    material VARCHAR(100),
    size VARCHAR(100),
    image_count INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_category_id (category_id),
    INDEX idx_status (status),
    INDEX idx_name (name),
    INDEX idx_color (color),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Product Images Table
CREATE TABLE IF NOT EXISTS product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url VARCHAR(1000) NOT NULL,         -- Increased length for longer URLs
    is_primary BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    delivery_address TEXT NOT NULL,
    payment_method VARCHAR(50) DEFAULT 'cash_on_delivery',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    color VARCHAR(100),
    size VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inventory Logs Table
CREATE TABLE IF NOT EXISTS inventory_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    old_stock INT NOT NULL,
    new_stock INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    admin_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE SET NULL,
    INDEX idx_product_id (product_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Activity Logs Table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(255) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Addresses Table
CREATE TABLE IF NOT EXISTS user_addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(10),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============ STEP 3: INSERT DEFAULT ADMIN ============
INSERT INTO admins (name, email, password, role, status) 
VALUES ('S.S BAGS Admin', 'admin@ssbags.com', '$2b$12$OIXl0uCQTOwvkVx0/zCqHOj6Yg3FQIAJrXXQvp7VH.nXYoG0dEzAm', 'admin', 'active');

-- ============ STEP 4: INSERT BAG CATEGORIES ============
INSERT INTO categories (name, description, status) 
VALUES
('Backpacks', 'School, travel, and daily use backpacks', 'active'),
('Handbags', 'Stylish handbags for women', 'active'),
('Crossbody Bags', 'Comfortable crossbody and sling bags', 'active'),
('Luggage & Travel', 'Trolley bags and travel luggage', 'active'),
('Wallets & Pouches', 'Wallets, pouches, and small bags', 'active');

-- ============ STEP 5: INSERT SAMPLE BAGS (PKR PRICES) ============
INSERT INTO products (name, description, category, category_id, price, stock, color, material, size, status) 
VALUES
('Premium Leather Backpack', 'High-quality leather backpack with laptop compartment', 'Backpacks', 1, 8500.00, 25, 'Black', 'Genuine Leather', 'Large', 'active'),
('School Backpack Pro', 'Durable backpack perfect for students', 'Backpacks', 1, 3500.00, 50, 'Blue', 'Polyester', 'Medium', 'active'),
('Designer Handbag Classic', 'Elegant designer handbag for daily use', 'Handbags', 2, 6500.00, 15, 'Brown', 'Leather', 'Medium', 'active'),
('Crossbody Messenger Bag', 'Comfortable crossbody bag for work and travel', 'Crossbody Bags', 3, 4500.00, 30, 'Black', 'Canvas', 'Large', 'active'),
('Compact Travel Pouch', 'Small pouch for travel essentials', 'Wallets & Pouches', 5, 1200.00, 100, 'Grey', 'Nylon', 'Small', 'active'),
('Trolley Luggage 24"', 'Lightweight luggage for air travel', 'Luggage & Travel', 4, 12000.00, 20, 'Black', 'Polycarbonate', '24 inch', 'active'),
('Office Briefcase', 'Professional briefcase for office and business', 'Handbags', 2, 5500.00, 18, 'Black', 'Leather', 'Large', 'active'),
('Sports Duffel Bag', 'Large duffel bag for gym and sports', 'Luggage & Travel', 4, 3800.00, 35, 'Red', 'Polyester', 'Large', 'active'),
('Ladies Shoulder Bag', 'Fashionable shoulder bag for women', 'Handbags', 2, 4200.00, 40, 'Pink', 'Synthetic Leather', 'Medium', 'active'),
('Kid Backpack Cartoon', 'Colorful backpack for kids', 'Backpacks', 1, 2500.00, 60, 'Multi-color', 'Polyester', 'Small', 'active');

-- ============ STEP 6: CREATE VIEWS ============

DROP VIEW IF EXISTS top_selling_bags;
DROP VIEW IF EXISTS customer_order_summary;

CREATE VIEW top_selling_bags AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.color,
    COUNT(oi.id) as sales_count,
    COALESCE(SUM(oi.quantity), 0) as total_quantity_sold,
    COALESCE(SUM(oi.quantity * oi.price), 0) as total_revenue
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status IN ('confirmed', 'shipped', 'delivered')
GROUP BY p.id, p.name, p.category, p.color
ORDER BY total_revenue DESC;

CREATE VIEW customer_order_summary AS
SELECT 
    u.id as user_id,
    u.name,
    u.email,
    COUNT(o.id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email;

-- ============ STEP 7: CREATE STORED PROCEDURE ============

DROP PROCEDURE IF EXISTS GetSalesReport;

DELIMITER $$

CREATE PROCEDURE GetSalesReport(IN report_period VARCHAR(20))
BEGIN
    IF report_period = 'daily' THEN
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as total_orders,
            SUM(total_amount) as revenue
        FROM orders
        WHERE status IN ('confirmed', 'shipped', 'delivered')
        AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(created_at)
        ORDER BY date DESC;
    ELSEIF report_period = 'monthly' THEN
        SELECT 
            DATE_FORMAT(created_at, '%Y-%m-01') as date,
            COUNT(*) as total_orders,
            SUM(total_amount) as revenue
        FROM orders
        WHERE status IN ('confirmed', 'shipped', 'delivered')
        AND created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
        GROUP BY DATE_FORMAT(created_at, '%Y-%m')
        ORDER BY date DESC;
    END IF;
END$$

DELIMITER ;

-- ============ VERIFICATION ============

SELECT 'S.S BAGS Database Created' as Status;
SELECT 'Admin Account Ready' as Status;
SELECT id, name, email, role FROM admins;
SELECT 'Sample Bags Inserted' as Status;
SELECT id, name, category, category_id, color, price, stock FROM products LIMIT 5;
SELECT 'Bag Categories' as Status;
SELECT id, name, description FROM categories;
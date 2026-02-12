// Enhanced JavaScript for S.S BAGS Template

// Sample Product Data (for demo purposes)
const sampleProducts = [
    {
        id: 1,
        name: "Premium Leather Backpack",
        category: "Backpacks",
        price: 8500,
        originalPrice: 12000,
        image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=500",
        badge: "sale",
        rating: 4.5,
        reviews: 128,
        description: "Handcrafted genuine leather backpack with multiple compartments"
    },
    {
        id: 2,
        name: "Designer Handbag Collection",
        category: "Handbags",
        price: 6500,
        originalPrice: null,
        image: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=500",
        badge: "new",
        rating: 4.8,
        reviews: 89,
        description: "Elegant designer handbag perfect for any occasion"
    },
    {
        id: 3,
        name: "Professional Laptop Bag",
        category: "Backpacks",
        price: 4500,
        originalPrice: 5500,
        image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?q=80&w=500",
        badge: "sale",
        rating: 4.3,
        reviews: 67,
        description: "Durable laptop bag with padded compartment and organization"
    },
    {
        id: 4,
        name: "Travel Duffel Bag",
        category: "Travel Bags",
        price: 7200,
        originalPrice: null,
        image: "https://images.unsplash.com/photo-1553877522-43269d4ea984?q=80&w=500",
        badge: "new",
        rating: 4.6,
        reviews: 94,
        description: "Spacious travel duffel bag with wheels and retractable handle"
    },
    {
        id: 5,
        name: "Classic Wallet Set",
        category: "Wallets",
        price: 2500,
        originalPrice: null,
        image: "https://images.unsplash.com/photo-1627123424574-724758594e93?q=80&w=500",
        badge: null,
        rating: 4.4,
        reviews: 156,
        description: "Premium leather wallet with card slots and coin pocket"
    },
    {
        id: 6,
        name: "Crossbody Messenger Bag",
        category: "Crossbody Bags",
        price: 3800,
        originalPrice: 4500,
        image: "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?q=80&w=500",
        badge: "sale",
        rating: 4.2,
        reviews: 73,
        description: "Stylish crossbody bag perfect for daily commute"
    }
];

// API base URL - configured for production/development
const API_BASE = 'http://localhost:8000/api';
let currentUser = JSON.parse(localStorage.getItem('user')) || null;
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products = [];
let useSampleData = false;

// Load categories for filtering
async function loadCategoriesForFilter() {
    // Don't clear HTML categories - they are already complete
    console.log('Categories filter loaded - keeping HTML categories intact');
}

// Load categories for home page display
async function loadCategoriesForHome() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        const data = await response.json();
        
        const categoryGrid = document.querySelector('.category-grid');
        
        if (data.categories && data.categories.length > 0) {
            categoryGrid.innerHTML = '';
            
            data.categories.forEach(category => {
                const categoryCard = document.createElement('div');
                categoryCard.className = 'cat-card';
                categoryCard.onclick = () => setCategory(category.name);
                
                // Use category image if available, otherwise use placeholder
                const imageUrl = category.image_url || `https://images.unsplash.com/photo-${getRandomImageId()}?auto=format&fit=crop&w=500&q=80`;
                
                categoryCard.innerHTML = `
                    <img src="${imageUrl}" alt="${category.name}">
                    <div class="cat-info"><h3>${category.name}</h3></div>
                `;
                
                categoryGrid.appendChild(categoryCard);
            });
        } else {
            // Fallback to default categories if API fails
            loadDefaultCategories();
        }
    } catch (error) {
        console.error('Error loading categories for home:', error);
        // Fallback to default categories
        loadDefaultCategories();
    }
}

// Fallback function to load default categories
function loadDefaultCategories() {
    console.log('Loading default categories...');
    const categoryGrid = document.querySelector('.category-grid');
    console.log('Category grid found:', categoryGrid);
    
    const defaultCategories = [
        { name: 'Handbags', image: 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=500&q=80' },
        { name: 'Backpacks', image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=500&q=80' },
        { name: 'Wallets', image: 'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=500&q=80' },
        { name: 'Travel Bags', image: '../assets/images/traveler.jpg' },
        { name: 'Crossbody Bags', image: '../assets/images/crossbody.jpg' },
        { name: 'Laptop Bags', image: '../assets/images/laptop.jpg' },
        { name: 'Duffel Bags', image: '../assets/images/Duffel.jpg' },
        { name: 'Clutch Bags', image: '../assets/images/clutch.jpg' },
        { name: 'Tote Bags', image: '../assets/images/tote.jpg' },
        { name: 'Messenger Bags', image: '../assets/images/Messenger.jpg' },
        { name: 'Sling Bags', image: '../assets/images/Sling.jpg' },
        { name: 'Briefcases', image: '../assets/images/Briefcases.jpg' },
        { name: 'School Bags', image: '../assets/images/School.jpg' },
        { name: 'Sports Bags', image: '../assets/images/Sports.jpg' },
        { name: 'Fashion Bags', image: '../assets/images/Fashion.jpg' },
        { name: 'Business Bags', image: '../assets/images/Business.jpg' },
        { name: 'Casual Bags', image: '../assets/images/Casual.jpg' },
        { name: 'Luxury Bags', image: '../assets/images/Luxury.jpg' }
    ];
    
    console.log('Default categories array:', defaultCategories);
    categoryGrid.innerHTML = '';
    
    defaultCategories.forEach((category, index) => {
        console.log(`Creating category ${index + 1}: ${category.name}`);
        const categoryCard = document.createElement('div');
        categoryCard.className = 'cat-card';
        categoryCard.onclick = () => setCategory(category.name);
        
        categoryCard.innerHTML = `
            <img src="${category.image}" alt="${category.name}">
            <div class="cat-info"><h3>${category.name}</h3></div>
        `;
        
        categoryGrid.appendChild(categoryCard);
        console.log(`Category card added for: ${category.name}`);
    });
    
    console.log('Total categories added:', defaultCategories.length);
}

// Helper function to generate random image ID for placeholder
function getRandomImageId() {
    const imageIds = [
        '1584917865442-de89df76afd3',
        '1553062407-98eeb64c6a62', 
        '1627123424574-724758594e93',
        '1553877522-43269d4ea984',
        '1551698618-1dfe5d97d256',
        '1594633312681-425c7b97ccd1'
    ];
    return imageIds[Math.floor(Math.random() * imageIds.length)];
}

document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    fetchProducts();
    loadCart();
    loadCategoriesForFilter();
    loadCategoriesForHome(); // Load categories for home page
    if (currentUser) loadOrders();
    
    // Force load default categories to ensure they show up
    setTimeout(() => {
        loadDefaultCategories();
    }, 1000);
    
    // Initialize hero slider
    initializeHeroSlider();
    
    // Icons ko render karne ke liye
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Initialize animations
    initializeAnimations();
});

// Hero Slider Functions
function initializeHeroSlider() {
    let currentSlideIndex = 0;
    const slides = document.querySelectorAll('.hero-slide');
    
    if (slides.length === 0) return;
    
    function showSlide(index) {
        const indicators = document.querySelectorAll('.indicator');
        
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(indicator => indicator.classList.remove('active'));
        
        if (slides[index]) {
            slides[index].classList.add('active');
        }
        if (indicators[index]) {
            indicators[index].classList.add('active');
        }
        currentSlideIndex = index;
    }
    
    function nextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length;
        showSlide(currentSlideIndex);
    }
    
    // Auto-advance slider
    setInterval(nextSlide, 5000);
    
    // Make functions globally available
    window.currentSlide = showSlide;
}

// Initialize Animations
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
            }
        });
    }, observerOptions);
    
    // Observe product cards and feature cards
    document.querySelectorAll('.product-card, .feature-card, .cat-card').forEach(card => {
        observer.observe(card);
    });
}

// Category filter function
function setCategory(category) {
    currentCategory = category;
    showSection('products');
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.value = category;
    }
    filterProducts();
    showToast(`Showing ${category} collection`, 'success');
}

// Set Collection
function setCollection(collection) {
    currentCollection = collection;
    showSection('products');
    showToast(`Showing ${collection} collection`, 'success');
}

// ============ AUTHENTICATION ============
function toggleAuth(formType) {
    if (formType === 'register') {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    } else {
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('register-form').style.display = 'none';
    }
}

async function register() {
    const name = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const phone = document.getElementById('reg-phone').value.trim();
    const password = document.getElementById('reg-password').value;
    const confirm = document.getElementById('reg-confirm').value;

    if (!name || !email || !phone || !password || !confirm) {
        alert('All fields required');
        return;
    }

    if (password !== confirm) {
        alert('Passwords do not match');
        return;
    }

    const phoneRegex = /^(\+92|92|0)?3\d{2}[\s-]?\d{7}$/;
    if (!phoneRegex.test(phone.replace(/\s+/g, ''))) {  
        alert('Invalid Pakistani phone number format. Use: 03xx-xxxxxxx, +923xxxxxxxxx, or 923xxxxxxxxx');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, password })
        });

        const data = await response.json();
        if (response.ok) {
            alert('Registration successful! Please login.');
            toggleAuth('login');
        } else {
            alert(data.detail || 'Registration failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function login() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        alert('Email and password required');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            currentUser = data.user;
            localStorage.setItem('user', JSON.stringify(currentUser));
            localStorage.setItem('token', data.token);
            updateAuthUI();
            alert('Login successful!');
            showSection('home');
            loadOrders();
        } else {
            alert(data.detail || 'Login failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    updateAuthUI();
    cart = [];
    localStorage.removeItem('cart');
    alert('Logged out successfully');
    showSection('home');
}

function updateAuthUI() {
    const authLink = document.getElementById('auth-link');
    const logoutLink = document.getElementById('logout-link');

    if (currentUser) {
        authLink.style.display = 'none';
        logoutLink.style.display = 'block';
    } else {
        authLink.style.display = 'block';
        logoutLink.style.display = 'none';
    }
}

// ============ NAVIGATION ============
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    window.scrollTo(0, 0);
}

// ============ PRODUCTS ============
async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        const data = await response.json();
        products = data.products || [];
        displayProducts(products);
    } catch (error) {
        console.error('Error fetching products:', error);
        document.getElementById('products-list').innerHTML = '<p>Error loading products</p>';
    }
}

function displayProducts(items) {
    const list = document.getElementById('products-list');
    
    if (items.length === 0) {
        list.innerHTML = '<p>No products found</p>';
        return;
    }

    list.innerHTML = items.map(product => `
        <div class="product-card">
            <div class="product-image-wrapper">
                ${product.images && product.images.length > 0 ? 
                    `<img src="${product.images[0]}" style="width:100%;height:100%;object-fit:cover;" alt="${product.name}" onerror="this.onerror=null;this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'100\' height=\'100\'%3E%3Crect fill=\'%23ddd\' width=\'100\' height=\'100\'/%3E%3Ctext x=\'50\' y=\'50\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\'%3EProduct%3C/text%3E%3C/svg%3E';">` : 
                    `<img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect fill='%23ddd' width='100' height='100'/%3E%3Ctext x='50' y='50' text-anchor='middle' dy='.3em' fill='%23999'%3EProduct%3C/text%3E%3C/svg%3E" style="width:100%;height:100%;" alt="${product.name}">`}
                <div class="add-to-cart-overlay" onclick="addToCart(${product.id})">
                    ADD TO CART
                </div>
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <p class="product-price">Rs. ${product.price.toLocaleString()}</p>
            </div>
        </div>
    `).join('');
    
    // Re-initialize feather icons for new elements
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// ============ ORDERS ============
async function proceedToOrder() {
    if (!currentUser) {
        showToast('Please login first', 'error');
        showSection('auth');
        return;
    }

    if (cart.length === 0) {
        showToast('Your cart is empty', 'error');
        return;
    }

    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const delivery = subtotal > 5000 ? 0 : 200;
    const total = subtotal + delivery;

    const orderDetails = cart.map(item => `${item.name} (Qty: ${item.quantity}) - Rs. ${item.price * item.quantity}`).join('\n');
    
    const message = `New Order from S.S BAGS:\n\n${orderDetails}\n\nSubtotal: Rs. ${subtotal}\nDelivery: ${delivery === 0 ? 'FREE' : `Rs. ${delivery}`}\nTotal: Rs. ${total}\n\nName: ${currentUser?.name || 'Guest'}\nEmail: ${currentUser?.email || 'Not provided'}`;
    
    const WHATSAPP_SHOP_NUMBER = '923150024508';
    const whatsappUrl = `https://wa.me/${WHATSAPP_SHOP_NUMBER}?text=${encodeURIComponent(message)}`;
    
    window.open(whatsappUrl, '_blank');
    
    // Clear cart after order
    cart = [];
    localStorage.removeItem('cart');
    updateCartUI();
    showToast('Order placed successfully! Check WhatsApp to confirm. Thank you for shopping at S.S BAGS!', 'success');
    showSection('orders');
}

async function loadOrders() {
    if (!currentUser) return;

    try {
        const response = await fetch(`${API_BASE}/orders/user/${currentUser.id}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        const data = await response.json();
        displayOrders(data.orders || []);
    } catch (error) {
        console.error('Error loading orders:', error);
        // Show sample orders for demo
        const sampleOrders = [
            {
                id: 1001,
                status: 'delivered',
                total_amount: 8500,
                created_at: new Date().toISOString(),
                items: [{ name: 'Premium Leather Backpack' }],
                delivery_address: 'Karachi, Pakistan'
            },
            {
                id: 1002,
                status: 'pending',
                total_amount: 6500,
                created_at: new Date().toISOString(),
                items: [{ name: 'Designer Handbag' }],
                delivery_address: 'Lahore, Pakistan'
            }
        ];
        displayOrders(sampleOrders);
    }
}

function displayOrders(orders) {
    const list = document.getElementById('orders-list');

    if (orders.length === 0) {
        list.innerHTML = '<p>No orders yet</p>';
        return;
    }

    list.innerHTML = orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <span class="order-id">Order #${order.id}</span>
                <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
            </div>
            <div class="order-details">
                <div class="order-detail-item">
                    <strong>Date:</strong> ${new Date(order.created_at).toLocaleDateString('ur-PK')}
                </div>
                <div class="order-detail-item">
                    <strong>Total:</strong> Rs. ${order.total_amount.toLocaleString()}
                </div>
                <div class="order-detail-item">
                    <strong>Items:</strong> ${order.items.length} product(s)
                </div>
                <div class="order-detail-item">
                    <strong>Address:</strong> ${order.delivery_address}
                </div>
            </div>
            ${order.status.toLowerCase() === 'pending' ? `
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee;">
                    <button class="btn btn-primary" onclick="resendViaWhatsApp(${order.id})" style="width: 100%;">ðŸ“± Resend via WhatsApp</button>
                </div>
            ` : ''}
        </div>
    `).join('');
}

// ============ WHATSAPP REDIRECT ============
/**
 * WhatsApp Redirect Function
 * Opens WhatsApp with pre-filled message
 * Supports both web and mobile platforms
 */
function redirectToWhatsApp(whatsappUrl, message, totalAmount) {
    console.log('ðŸ“± Opening WhatsApp with order details...');
    
    // Get device type
    const isAndroid = /Android/i.test(navigator.userAgent);
    const isIPhone = /iPhone|iPad|iPod/i.test(navigator.userAgent);
    const isDesktop = !isAndroid && !isIPhone;
    
    // WhatsApp shop number from environment (Update .env file with your actual number)
    const WHATSAPP_SHOP_NUMBER = '923150024508';  // This will be updated from .env in production
    
    let finalUrl;
    
    if (isAndroid || isIPhone) {
        // Mobile: Use WhatsApp app if installed
        finalUrl = `whatsapp://send?phone=${WHATSAPP_SHOP_NUMBER}&text=${encodeURIComponent(message)}`;
    } else {
        // Desktop: Use WhatsApp Web
        finalUrl = `https://wa.me/${WHATSAPP_SHOP_NUMBER}?text=${encodeURIComponent(message)}`;
    }
    
    console.log('ðŸ“¤ Message Details:');
    console.log('Total Amount: Rs. ' + totalAmount.toLocaleString());
    console.log('Target Number: ' + WHATSAPP_SHOP_NUMBER);
    console.log('Platform: ' + (isAndroid ? 'Android' : isIPhone ? 'iPhone' : 'Desktop'));
    
    // Open WhatsApp
    try {
        window.open(finalUrl, '_blank');
        
        // If mobile and it didn't work, fallback to web
        if ((isAndroid || isIPhone) && !window.open(finalUrl)) {
            console.log('âš ï¸  App not installed. Falling back to WhatsApp Web...');
            const webUrl = `https://wa.me/${WHATSAPP_SHOP_NUMBER}?text=${encodeURIComponent(message)}`;
            window.open(webUrl, '_blank');
        }
    } catch (error) {
        console.error('âŒ WhatsApp redirect failed:', error);
        alert('âŒ Could not open WhatsApp. Please try again or copy the message below:\n\n' + message);
    }
}

/**
 * Alternative Function - If user wants to retry WhatsApp
 */
function resendViaWhatsApp(orderId) {
    const order = allOrders.find(o => o.id === orderId);
    if (!order) {
        alert('Order not found');
        return;
    }
    
    const message = `Order #${order.id}

Customer: ${currentUser.name}
Email: ${currentUser.email}

Total: Rs. ${order.total_amount.toLocaleString()}

Payment: Cash on Delivery`;
    
    const WHATSAPP_SHOP_NUMBER = '923150024508';  // Update this in .env file for production
    const whatsappUrl = `https://wa.me/${WHATSAPP_SHOP_NUMBER}?text=${encodeURIComponent(message)}`;
    
    console.log('ðŸ”„ Resending order via WhatsApp...');
    redirectToWhatsApp(whatsappUrl, message, order.total_amount);
}

// ============ UTILITY FUNCTIONS ============

// Show Toast Notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutDown 0.3s ease-out forwards';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Animate Add to Cart
function animateAddToCart() {
    const cartIcon = document.querySelector('#cart-count').parentElement;
    cartIcon.style.animation = 'pulse 0.5s ease-out';
    setTimeout(() => {
        cartIcon.style.animation = '';
    }, 500);
}

// Mobile Menu Toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
    const navMenu = document.querySelector('.nav-menu');
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    
    if (!navMenu.contains(event.target) && !menuToggle.contains(event.target)) {
        navMenu.classList.remove('active');
    }
});

// Add slide out animation for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutDown {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============ PRODUCTS ============
function filterProducts() {
    const search = document.getElementById('search-input').value.toLowerCase();
    const category = document.getElementById('category-filter').value;
    const sort = document.getElementById('sort-filter').value;

    let filtered = products.filter(p => {
        const matchSearch = p.name.toLowerCase().includes(search) || 
                           p.description.toLowerCase().includes(search);
        const matchCategory = !category || p.category === category;
        return matchSearch && matchCategory;
    });

    if (sort === 'price-low') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (sort === 'price-high') {
        filtered.sort((a, b) => b.price - a.price);
    } else if (sort === 'newest') {
        filtered.sort((a, b) => b.id - a.id);
    }

    displayProducts(filtered);
}

// ============ CART ============
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) {
        // Use sample data if no product found
        const sampleProduct = sampleProducts.find(p => p.id === productId);
        if (!sampleProduct) return;
        
        const existingItem = cart.find(item => item.id === productId);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ ...sampleProduct, quantity: 1 });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartUI();
        showToast(`${sampleProduct.name} added to cart!`, 'success');
        animateAddToCart();
        return;
    }

    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
    showToast(`${product.name} added to cart!`, 'success');
    animateAddToCart();
}

function loadCart() {
    updateCartUI();
}

function updateCartUI() {
    const cartItems = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');

    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;

    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Your cart is empty</p>';
        document.getElementById('subtotal').textContent = 'Rs. 0';
        document.getElementById('delivery').textContent = 'FREE';
        document.getElementById('total').textContent = 'Rs. 0';
        return;
    }

    cartItems.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">Rs. ${item.price.toLocaleString()}</div>
            </div>
            <div class="cart-item-controls">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${index}, -1)">
                        <i data-feather="minus"></i>
                    </button>
                    <input type="text" class="quantity-input" value="${item.quantity}" readonly>
                    <button class="quantity-btn" onclick="updateQuantity(${index}, 1)">
                        <i data-feather="plus"></i>
                    </button>
                </div>
                <button class="remove-btn" onclick="removeFromCart(${index})">
                    <i data-feather="trash-2"></i> Remove
                </button>
            </div>
        </div>
    `).join('');

    calculateCartTotal();
    
    // Re-initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function updateQuantity(index, change) {
    const newQty = cart[index].quantity + change;
    
    if (newQty <= 0) {
        removeFromCart(index);
        return;
    }
    
    cart[index].quantity = newQty;
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
}

function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartUI();
    showToast('Item removed from cart', 'error');
}

function calculateCartTotal() {
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const delivery = subtotal > 5000 ? 0 : 200; // Free delivery over Rs. 5000
    const total = subtotal + delivery;

    document.getElementById('subtotal').textContent = `Rs. ${subtotal.toLocaleString()}`;
    document.getElementById('delivery').textContent = delivery === 0 ? 'FREE' : `Rs. ${delivery}`;
    document.getElementById('delivery').className = delivery === 0 ? 'free-delivery' : '';
    document.getElementById('total').textContent = `Rs. ${total.toLocaleString()}`;
}
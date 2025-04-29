

DROP DATABASE IF EXISTS RestaurantDB;

CREATE DATABASE RestaurantDB;

USE RestaurantDB;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    role ENUM('Admin', 'Waiter', 'Chef', 'Customer') NOT NULL,
    role_description TEXT,                 
    story TEXT,                             
    achievements TEXT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    image_url VARCHAR(255),
    contribution DECIMAL(10, 2) DEFAULT 0.00,
    is_deleted BOOLEAN DEFAULT FALSE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    address VARCHAR(255),
    deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE MenuItems (
    menu_item_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    available BOOLEAN DEFAULT TRUE,
    enable_water_track BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Meats (
    meat_id INT PRIMARY KEY AUTO_INCREMENT,
    meat_type ENUM('Chicken', 'Duck', 'Fish', 'Pork', 'Beef', 'Egg') NOT NULL, 
    description TEXT,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Ingredients (
    ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    meat_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meat_id) REFERENCES Meats(meat_id)  
);

CREATE TABLE MenuItemIngredients (
    menu_item_id INT,
    ingredient_id INT,
    quantity DECIMAL(10, 2) NOT NULL,  
    unit ENUM('l', 'g', 'kg', 'gallon') NOT NULL, 
    PRIMARY KEY (menu_item_id, ingredient_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    waiter_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Preparing', 'Completed', 'Canceled') DEFAULT 'Pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    recall_id BIGINT DEFAULT NULL,
    
    -- Guest info snapshot
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    address TEXT,
    city_or_town VARCHAR(100),
    zip_code VARCHAR(20),
    email VARCHAR(255),
    
    FOREIGN KEY (customer_id) REFERENCES Users(user_id),
    FOREIGN KEY (waiter_id) REFERENCES Users(user_id)
);


CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    menu_item_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
);

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    payment_method VARCHAR(50),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    menu_item_id INT,
    rating INT NOT NULL,
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Users(user_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
);

CREATE TABLE Carts (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE CartItems (
    cart_item_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT,
    menu_item_id INT,
    quantity INT NOT NULL,  
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES Carts(cart_id),  
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id) 
);



CREATE TABLE restaurant_profile (
    profile_id SERIAL PRIMARY KEY,
    description TEXT,
    rating DECIMAL(3,2) DEFAULT 0.00,
    image_url VARCHAR(255),
    facilities TEXT,
    opening_date DATE,
    opening_time TIME,
    closing_time TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
INSERT INTO restaurant_profile (
    description,
    rating,
    image_url,
    facilities,
    opening_date,
    opening_time,
    closing_time,
    created_at,
    updated_at
)
VALUES (
    'Kind Plate',
    4.95,
    'https://example.com/images/kind_plate_fancy_image.jpg',
    'Wheelchair Accessible, Pet-Friendly, Outdoor Seating, ASL Services, Vegan/Gluten-Free Options, Free Wi-Fi, Zero-Waste Practices, Live Music Nights, Community Cooking Classes',
    '2021-03-15',
    '10:00:00',
    '23:00:00',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO MenuItems (name, description, price, category, available, enable_water_track, image_url)
VALUES 
('Vegan Margherita Pizza', 'Classic cheese-free pizza with fresh basil, vegan mozzarella, and tomato sauce.', 12.99, 'Pizza', TRUE, FALSE, 'https://example.com/images/vegan_margherita.jpg'),
('Vegan Spaghetti Carbonara', 'Spaghetti pasta with a creamy cashew-based sauce, smoked tempeh, and nutritional yeast.', 14.50, 'Pasta', TRUE, FALSE, 'https://example.com/images/vegan_carbonara.jpg'),
('Vegan Caesar Salad', 'Crisp romaine lettuce with dairy-free Caesar dressing, croutons, and vegan parmesan.', 9.25, 'Salad', TRUE, FALSE, 'https://example.com/images/vegan_caesar_salad.jpg'),
('Grilled Veggie Sandwich', 'Grilled seasonal vegetables with lettuce, tomato, and a creamy vegan aioli on toasted whole-grain bread.', 11.75, 'Sandwich', TRUE, FALSE, 'https://example.com/images/grilled_veggie_sandwich.jpg'),
('Vegan Tiramisu', 'Traditional Italian coffee-flavored dessert made with coconut cream and dairy-free ladyfingers.', 6.80, 'Dessert', TRUE, FALSE, 'https://example.com/images/vegan_tiramisu.jpg');

INSERT INTO Users (username, password_hash, email, phone_number, role, role_description, story, achievements, first_name, last_name, image_url, contribution, address)
VALUES
('hana_greeter', 'hashed_password_13', 'hana@email.com', '1234567802', 'Waiter',
 'Greets guests using ASL and digital menus, ensuring all feel welcomed.',
 'My joy comes from helping first-time ASL users order confidently.',
 'Trained over 200 guests to use basic ASL greetings at the door.',
 'Hana', 'Nguyen', 'https://example.com/images/hana.jpg', 0.00, '111 Cypress St, City, Country'),

('kai_dishwasher', 'hashed_password_14', 'kai@email.com', '1234567803', 'Waiter',
 'Manages eco-friendly dishwashing systems with visual load indicators.',
 'I may be behind the scenes, but I know I’m helping keep the kitchen moving silently and smoothly.',
 'Reduced water use by 30% with new dish cycle techniques.',
 'Kai', 'Chen', 'https://example.com/images/kai.jpg', 0.00, '222 Palm St, City, Country'),

('zoe_signcoach', 'hashed_password_15', 'zoe@email.com', '1234567804', 'Waiter',
 'Leads ASL lunch breaks where staff practice signs together.',
 'I came for the food, stayed for the team spirit—and now I teach!',
 'Organized weekly ASL practice sessions improving inter-staff communication by 50%.',
 'Zoe', 'Adams', 'https://example.com/images/zoe.jpg', 0.00, '333 Spruce St, City, Country');




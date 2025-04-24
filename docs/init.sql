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
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT, 
    rating DECIMAL(3, 2) DEFAULT 0.00, 
    image_url VARCHAR(255),
    facilities TEXT, 
    opening_date DATE, 
    opening_time TIME,
    closing_time TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO MenuItems (name, description, price, category, available, enable_water_track, image_url)
VALUES 
('Margherita Pizza', 'Classic cheese and tomato pizza with fresh basil.', 12.99, 'Pizza', TRUE, FALSE, 'https://example.com/images/margherita.jpg'),
('Spaghetti Carbonara', 'Spaghetti pasta with creamy sauce, bacon, and cheese.', 14.50, 'Pasta', TRUE, FALSE, 'https://example.com/images/carbonara.jpg'),
('Caesar Salad', 'Crisp romaine lettuce with Caesar dressing, croutons, and parmesan.', 9.25, 'Salad', TRUE, FALSE, 'https://example.com/images/caesar_salad.jpg'),
('Grilled Chicken Sandwich', 'Grilled chicken breast with lettuce, tomato, and aioli on a toasted bun.', 11.75, 'Sandwich', TRUE, FALSE, 'https://example.com/images/chicken_sandwich.jpg'),
('Tiramisu', 'Traditional Italian coffee-flavored dessert.', 6.80, 'Dessert', TRUE, FALSE, 'https://example.com/images/tiramisu.jpg');


INSERT INTO restaurant_profile (
    description, 
    rating, 
    image_url, 
    facilities,
    opening_date, 
    opening_time, 
    closing_time
) VALUES
('Kind Plate', 4.75, 'https://example.com/images/italian.jpg', 'Wi-Fi, Outdoor Seating',
 '2022-06-15', '10:00:00', '22:00:00');


INSERT INTO MenuItems (name, description, price, category, available, enable_water_track, image_url)
VALUES 
('Margherita Pizza', 'Classic cheese and tomato pizza with fresh basil.', 12.99, 'Pizza', TRUE, FALSE, 'https://example.com/images/margherita.jpg'),
('Spaghetti Carbonara', 'Spaghetti pasta with creamy sauce, bacon, and cheese.', 14.50, 'Pasta', TRUE, FALSE, 'https://example.com/images/carbonara.jpg'),
('Caesar Salad', 'Crisp romaine lettuce with Caesar dressing, croutons, and parmesan.', 9.25, 'Salad', TRUE, FALSE, 'https://example.com/images/caesar_salad.jpg'),
('Grilled Chicken Sandwich', 'Grilled chicken breast with lettuce, tomato, and aioli on a toasted bun.', 11.75, 'Sandwich', TRUE, FALSE, 'https://example.com/images/chicken_sandwich.jpg'),
('Tiramisu', 'Traditional Italian coffee-flavored dessert.', 6.80, 'Dessert', TRUE, FALSE, 'https://example.com/images/tiramisu.jpg');




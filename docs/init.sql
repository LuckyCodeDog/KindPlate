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








INSERT INTO Users (
    username, password_hash, email, phone_number, role,
    first_name, last_name, image_url, contribution,
    is_deleted, status, address, deleted
) VALUES

('admin_user', 'hashed_password_1', 'admin@example.com', '1234567890', 'Admin',
 'Alice', 'Smith', 'https://example.com/images/admin.jpg', 150.00,
 FALSE, 'active', '123 Admin St.', FALSE),


('waiter_john', 'hashed_password_2', 'john.waiter@example.com', '2345678901', 'Waiter',
 'John', 'Doe', 'https://example.com/images/waiter.jpg', 50.25,
 FALSE, 'active', '456 Service Ave.', FALSE),


('chef_maria', 'hashed_password_3', 'maria.chef@example.com', '3456789012', 'Chef',
 'Maria', 'Lopez', 'https://example.com/images/chef.jpg', 75.50,
 FALSE, 'inactive', '789 Kitchen Rd.', FALSE),


('customer_lee', 'hashed_password_4', 'lee.customer@example.com', '4567890123', 'Customer',
 'Lee', 'Wang', 'https://example.com/images/customer1.jpg', 20.00,
 FALSE, 'active', '101 Customer Blvd.', FALSE),

('customer_kate', 'hashed_password_5', 'kate.customer@example.com', '5678901234', 'Customer',
 'Kate', 'Brown', 'https://example.com/images/customer2.jpg', 0.00,
 TRUE, 'inactive', '202 Hidden Ln.', TRUE);



INSERT INTO MenuItems (name, description, price, category, available, enable_water_track, image_url)
VALUES
('Chicken Burger', 'Juicy chicken patty with lettuce and mayo', 8.99, 'Burgers', TRUE, FALSE, 'https://example.com/images/chicken_burger.jpg'),
('Beef Steak', 'Tender beef steak with mashed potatoes', 15.99, 'Steaks', TRUE, FALSE, 'https://example.com/images/beef_steak.jpg'),
('Fish Tacos', 'Crispy fish with taco sauce and slaw', 10.99, 'Tacos', TRUE, FALSE, 'https://example.com/images/fish_tacos.jpg'),
('Vegetable Salad', 'Fresh vegetables with a vinaigrette dressing', 6.99, 'Salads', TRUE, FALSE, 'https://example.com/images/vegetable_salad.jpg'),
('Pork Ribs', 'BBQ pork ribs served with fries', 12.99, 'Ribs', TRUE, FALSE, 'https://example.com/images/pork_ribs.jpg'),
('Cheese Pizza', 'Classic cheese pizza with mozzarella', 9.99, 'Pizza', TRUE, TRUE, 'https://example.com/images/cheese_pizza.jpg'),
('Chicken Wings', 'Spicy chicken wings with dipping sauce', 7.99, 'Appetizers', TRUE, FALSE, 'https://example.com/images/chicken_wings.jpg'),
('Egg Fried Rice', 'Fried rice with eggs and vegetables', 5.99, 'Rice', TRUE, FALSE, 'https://example.com/images/egg_fried_rice.jpg'),
('Grilled Salmon', 'Grilled salmon with lemon butter sauce', 14.99, 'Seafood', TRUE, FALSE, 'https://example.com/images/grilled_salmon.jpg'),
('Spaghetti Carbonara', 'Pasta with creamy carbonara sauce', 11.99, 'Pasta', TRUE, TRUE, 'https://example.com/images/spaghetti_carbonara.jpg'),
('Beef Burger', 'Classic beef patty with lettuce and cheese', 9.99, 'Burgers', TRUE, FALSE, 'https://example.com/images/beef_burger.jpg'),
('Vegetarian Tacos', 'Tacos filled with grilled vegetables', 8.99, 'Tacos', TRUE, FALSE, 'https://example.com/images/vegetarian_tacos.jpg'),
('Margarita Pizza', 'Pizza with tomato, mozzarella, and basil', 10.99, 'Pizza', TRUE, FALSE, 'https://example.com/images/margarita_pizza.jpg'),
('Chicken Caesar Salad', 'Caesar salad with grilled chicken', 7.99, 'Salads', TRUE, TRUE, 'https://example.com/images/chicken_caesar_salad.jpg'),
('Lamb Chops', 'Grilled lamb chops with mint sauce', 16.99, 'Steaks', TRUE, FALSE, 'https://example.com/images/lamb_chops.jpg'),
('Shrimp Scampi', 'Shrimp in garlic butter sauce with pasta', 13.99, 'Seafood', TRUE, TRUE, 'https://example.com/images/shrimp_scampi.jpg'),
('Pasta Primavera', 'Pasta with a mix of fresh vegetables', 10.99, 'Pasta', TRUE, FALSE, 'https://example.com/images/pasta_primavera.jpg'),
('Fish and Chips', 'Battered fish with crispy fries', 11.99, 'Seafood', TRUE, FALSE, 'https://example.com/images/fish_and_chips.jpg'),
('Cheeseburger', 'Beef patty with cheese, pickles, and mustard', 8.99, 'Burgers', TRUE, FALSE, 'https://example.com/images/cheeseburger.jpg'),
('BBQ Chicken', 'BBQ chicken served with corn on the cob', 12.99, 'Chicken', TRUE, FALSE, 'https://example.com/images/bbq_chicken.jpg');


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
 '2022-06-15', '10:00:00', '22:00:00'),


 INSERT INTO Orders (
    customer_id, waiter_id, order_date, status, total_amount
) VALUES


(4, 2, NOW(), 'Pending', 45.50),


(4, 2, NOW(), 'Preparing', 72.30),


(5, 2, NOW(), 'Completed', 120.00),


(5, 2, NOW(), 'Canceled', 38.00),


(4, 2, NOW(), 'Completed', 90.75);

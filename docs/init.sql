DROP DATABASE IF EXISTS RestaurantDB;

CREATE DATABASE RestaurantDB;

USE RestaurantDB;

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    role ENUM('Admin', 'Manager', 'Staff', 'Customer') NOT NULL,
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

CREATE TABLE booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(120),
    guests INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'confirmed', 'cancelled') NOT NULL DEFAULT 'pending',
    reference_number VARCHAR(36) UNIQUE NOT NULL
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


INSERT INTO Users (username, password_hash, email, phone_number, role, role_description, story, achievements, first_name, last_name, image_url, contribution, address)
VALUES
('hana_greeter', 'hashed_password_13', 'hana@email.com', '1234567802', 'Manager',
 'Greets guests using ASL and digital menus, ensuring all feel welcomed.',
 'My joy comes from helping first-time ASL users order confidently.',
 'Trained over 200 guests to use basic ASL greetings at the door.',
 'Hana', 'Nguyen', 'https://example.com/images/hana.jpg', 0.00, '111 Cypress St, City, Country'),

('admin1', 'hashed_password_13', 'hana@email.com', '1234567802', 'Admin',
 'Greets guests using ASL and digital menus, ensuring all feel welcomed.',
 'My joy comes from helping first-time ASL users order confidently.',
 'Trained over 200 guests to use basic ASL greetings at the door.',
 'Hana', 'Nguyen', 'https://example.com/images/hana.jpg', 0.00, '111 Cypress St, City, Country'),
 
('kai_dishwasher', 'hashed_password_14', 'kai@email.com', '1234567803', 'Manager',
 'Manages eco-friendly dishwashing systems with visual load indicators.',
 'I may be behind the scenes, but I know I’m helping keep the kitchen moving silently and smoothly.',
 'Reduced water use by 30% with new dish cycle techniques.',
 'Kai', 'Chen', 'https://example.com/images/kai.jpg', 0.00, '222 Palm St, City, Country'),

('zoe_signcoach', 'hashed_password_15', 'zoe@email.com', '1234567804', 'Manager',
 'Leads ASL lunch breaks where staff practice signs together.',
 'I came for the food, stayed for the team spirit—and now I teach!',
 'Organized weekly ASL practice sessions improving inter-staff communication by 50%.',
 'Zoe', 'Adams', 'https://example.com/images/zoe.jpg', 0.00, '333 Spruce St, City, Country');
 


INSERT INTO MenuItems (name, description, price, category) VALUES
-- Appetizers
('Vegan Dumplings (6pc)', 'Asian housemade mixed vegetable dumplings, steamed or seared', 8.00, 'Appetizers'),
('Scallion Pancake', 'With dipping sauce', 7.00, 'Appetizers'),
('Barbeque "Roast Pork"', 'Sauteed soy protein with house-made barbeque sauce', 12.00, 'Appetizers'),
('King Oyster Mushrooms', 'Battered fried king oyster mushrooms tossed with chopped fresh peppers, seasoned with salt and pepper', 10.00, 'Appetizers'),
('Soy Nuggets', 'With vegan aioli dipping sauce', 12.00, 'Appetizers'),
('Spicy "Tuna" Avocado Roll', 'Avocado, cucumber, house-made vegan tuna (dried tomatoes)', 13.00, 'Appetizers'),

-- Entrees
('Sesame "Beef"', 'Stir-fried soy protein in sweet sesame sauce with mushrooms, bell peppers, onions with steamed kale', 21.00, 'Entrees'),
('General Tso''s "Chicken"', 'Stir-fried soy protein, broccoli and mixed vegetables in General Tso''s sauce', 23.00, 'Entrees'),
('Sweet and Sour "Chicken"', 'Battered soy protein, bell peppers, broccoli, cauliflower, pineapple, carrots, and onions in a housemade sweet and sour sauce', 22.00, 'Entrees'),
('Home Styled Mapo Tofu', 'Tofu, minced "meat", peas, hot peppers in brown sauce and garnished with scallions', 16.00, 'Entrees'),
('Beijing "Duck"', 'Roasted whole soy protein and sauteed oyster mushrooms with kale, Japanese pumpkin topped with almond slices', 25.00, 'Entrees'),
('"Spare Ribs" and Potatoes', 'Homestyle spare soy ribs and potatoes in delicious brown sauce', 22.00, 'Entrees'),
('Eggplant with Garlic Sauce', 'Eggplant, bell peppers, bok choy and wood ears with garlic sauce', 19.00, 'Entrees'),
('Sauteed Mixed Vegetables', 'Seasonal vegetables', 16.00, 'Entrees'),
('Pineapple Fried Rice', 'Mixed vegetables, topped with pineapples', 15.00, 'Entrees'),

-- Noodle Soups
('Curry "Chicken" Noodle Soup', 'Noodles, eggplant, snow peas, mushrooms, potatoes, cabbage, vegan soy chicken', 17.00, 'Noodle Soups'),
('BBQ "Roast Pork" Noodle Soup', 'Vegan soy pork, baby bok choy, rice noodle', 15.00, 'Noodle Soups'),
('Soy "Duck" Noodle Soup', 'Pressed tofu skin, vegan soy duck, baby bok choy, noodle', 16.00, 'Noodle Soups'),

-- Desserts
('Blueberry "Cheesecake" (Gluten-Free)', NULL, 8.00, 'Desserts'),
('Decadent Chocolate Cake (Nut-Free)', NULL, 8.00, 'Desserts'),
('Almond "Milk" & Chocolate Chip Cookie (Gluten-Free)', NULL, 8.00, 'Desserts'),

-- Beverages
('Double Espresso', NULL, 5.00, 'Beverages'),
('Long Black', NULL, 4.00, 'Beverages'),
('Cappuccino', NULL, 5.00, 'Beverages'),
('Latte', NULL, 5.00, 'Beverages'),
('Earl Grey Latte', NULL, 5.00, 'Beverages'),
('Hazelnut Latte', NULL, 7.00, 'Beverages'),
('Caramel Latte', NULL, 6.00, 'Beverages'),
('Mocha', NULL, 6.00, 'Beverages'),
('Hot Chocolate', NULL, 6.00, 'Beverages'),
('Mint Chocolate', NULL, 6.00, 'Beverages');








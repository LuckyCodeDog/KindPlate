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
    
    social_media_links JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE restaurant_opening_hours (
    opening_hours_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT, 
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
    opening_time TIME, 
    closing_time TIME, 
    is_closed BOOLEAN DEFAULT FALSE, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) 
);

INSERT INTO Users (username, password_hash, email, phone_number, role, first_name, last_name, image_url, contribution, status)
VALUES
('john_doe', 'hashed_password1', 'john.doe@example.com', '123-456-7890', 'Customer', 'John', 'Doe', 'https://example.com/images/john.jpg', 0.00, 'active'),
('jane_smith', 'hashed_password2', 'jane.smith@example.com', '123-456-7891', 'Waiter', 'Jane', 'Smith', 'https://example.com/images/jane.jpg', 0.00, 'active'),
('mark_jones', 'hashed_password3', 'mark.jones@example.com', '123-456-7892', 'Chef', 'Mark', 'Jones', 'https://example.com/images/mark.jpg', 0.00, 'active'),
('susan_williams', 'hashed_password4', 'susan.williams@example.com', '123-456-7893', 'Customer', 'Susan', 'Williams', 'https://example.com/images/susan.jpg', 0.00, 'inactive'),
('robert_brown', 'hashed_password5', 'robert.brown@example.com', '123-456-7894', 'Admin', 'Robert', 'Brown', 'https://example.com/images/robert.jpg', 0.00, 'active'),
('mary_davis', 'hashed_password6', 'mary.davis@example.com', '123-456-7895', 'Customer', 'Mary', 'Davis', 'https://example.com/images/mary.jpg', 0.00, 'active'),
('james_miller', 'hashed_password7', 'james.miller@example.com', '123-456-7896', 'Waiter', 'James', 'Miller', 'https://example.com/images/james.jpg', 0.00, 'inactive'),
('lisa_garcia', 'hashed_password8', 'lisa.garcia@example.com', '123-456-7897', 'Chef', 'Lisa', 'Garcia', 'https://example.com/images/lisa.jpg', 0.00, 'active'),
('daniel_martin', 'hashed_password9', 'daniel.martin@example.com', '123-456-7898', 'Customer', 'Daniel', 'Martin', 'https://example.com/images/daniel.jpg', 0.00, 'active'),
('elizabeth_clark', 'hashed_password10', 'elizabeth.clark@example.com', '123-456-7899', 'Admin', 'Elizabeth', 'Clark', 'https://example.com/images/elizabeth.jpg', 0.00, 'active'),
('kevin_lewis', 'hashed_password11', 'kevin.lewis@example.com', '123-456-7900', 'Chef', 'Kevin', 'Lewis', 'https://example.com/images/kevin.jpg', 0.00, 'active'),
('anna_white', 'hashed_password12', 'anna.white@example.com', '123-456-7901', 'Waiter', 'Anna', 'White', 'https://example.com/images/anna.jpg', 0.00, 'inactive'),
('chris_hall', 'hashed_password13', 'chris.hall@example.com', '123-456-7902', 'Customer', 'Chris', 'Hall', 'https://example.com/images/chris.jpg', 0.00, 'active'),
('nancy_allen', 'hashed_password14', 'nancy.allen@example.com', '123-456-7903', 'Admin', 'Nancy', 'Allen', 'https://example.com/images/nancy.jpg', 0.00, 'active'),
('brian_young', 'hashed_password15', 'brian.young@example.com', '123-456-7904', 'Chef', 'Brian', 'Young', 'https://example.com/images/brian.jpg', 0.00, 'active'),
('rebecca_king', 'hashed_password16', 'rebecca.king@example.com', '123-456-7905', 'Waiter', 'Rebecca', 'King', 'https://example.com/images/rebecca.jpg', 0.00, 'inactive'),
('william_lee', 'hashed_password17', 'william.lee@example.com', '123-456-7906', 'Customer', 'William', 'Lee', 'https://example.com/images/william.jpg', 0.00, 'active'),
('emily_wright', 'hashed_password18', 'emily.wright@example.com', '123-456-7907', 'Customer', 'Emily', 'Wright', 'https://example.com/images/emily.jpg', 0.00, 'active'),
('joseph_smith', 'hashed_password19', 'joseph.smith@example.com', '123-456-7908', 'Chef', 'Joseph', 'Smith', 'https://example.com/images/joseph.jpg', 0.00, 'inactive'),
('samantha_johnson', 'hashed_password20', 'samantha.johnson@example.com', '123-456-7909', 'Waiter', 'Samantha', 'Johnson', 'https://example.com/images/samantha.jpg', 0.00, 'active');

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

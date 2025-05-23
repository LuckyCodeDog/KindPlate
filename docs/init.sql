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
    total_water_saved DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Total water saved in liters',
    water_saving_level INT DEFAULT 1 COMMENT 'User water saving level (1-5)',
    water_saving_points INT DEFAULT 0 COMMENT 'Points earned from water saving',
    last_water_saving_date TIMESTAMP NULL COMMENT 'Last time user earned water saving points',
    badges VARCHAR(255) DEFAULT '' COMMENT 'User earned badges, comma separated',
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
    water_usage_l_per_kg DECIMAL(10,2) NOT NULL COMMENT 'Water usage in liters per kg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Ingredients (
    ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    meat_id INT,
    water_usage_l_per_kg DECIMAL(10,2) NOT NULL COMMENT 'Water usage in liters per kg',
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
    
    FOREIGN KEY (customer_id) REFERENCES Users(user_id)
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
    address TEXT,
    phone_number VARCHAR(20),
    story TEXT,
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
    address,
    phone_number,
    story,
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
    '123 Main St, Anytown, NZ',
    '1234567890',
    "Born from a belief that food can heal both people and the planet, Kind Plate began as a small kitchen run by a team of passionate chefs and advocates for social equity. Today, we've grown into a thriving hub where 70% of our staff are deaf or mute individuals, proving that great food needs no words—just heart.",
    4.95,
    'https://example.com/images/kind_plate_fancy_image.jpg',
    'Wheelchair Accessible, Pet-Friendly, Outdoor Seating, ASL Services, Vegan/Gluten-Free Options, Free Wi-Fi, Zero-Waste Practices, Live Music Nights, Community Cooking Classes',
    '2021-03-15',
    '10:00:00',
    '23:00:00',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);



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


INSERT INTO Users (
    username, password_hash, email, phone_number, role, role_description, story, achievements,
    first_name, last_name, image_url, contribution, address
) VALUES
('admin1', 'hashed_password_13', 'hana@email.com', '1234567802', 'Admin',
 'Greets guests using ASL and digital menus, ensuring all feel welcomed.',
 'My joy comes from helping first-time ASL users order confidently.',
 'Trained over 200 guests to use basic ASL greetings at the door.',
 'Hana', 'Nguyen', 'https://example.com/images/hana.jpg', 0.00, '111 Cypress St, City, Country'),

('emma', 'placeholder_hash', NULL, NULL, 'Manager',
 'Oversees operations and staff training in ASL/accessibility.',
 'I left corporate hospitality to work here—seeing deaf and hearing staff collaborate so seamlessly is magic.',
 'Increased deaf hires by 80% in 2026.',
 'Emma', '', 'Image', 0.00, NULL),

('sofia', 'placeholder_hash', NULL, NULL, 'Staff',
 'Designs zero-waste menus and trains staff on composting.',
 'Created Kind Plate''s signature "Root-to-Stem" salad using typically discarded veggie parts.',
 NULL,
 'Sofia', '', 'Image', 0.00, NULL),

('malik', 'placeholder_hash', NULL, NULL, 'Staff',
 'Heads the open-fire grill station, specializing in smoked jackfruit and charred veggies.',
 NULL,
 'Silent Smoke BBQ platter (voted Best Vegan BBQ by Eco Eats).',
 'Malik', '', 'Image', 0.00, NULL),

('diego', 'placeholder_hash', NULL, NULL, 'Staff',
 'Crafts latte art with eco-friendly oat milk, using visual cues to take orders.',
 'Customers love when I ''draw'' their requests—yesterday, a panda for a 6-year-old!',
 'His "ASL Alphabet Latte Series" (learn a sign with each order).',
 'Diego', '', 'Image', 0.00, NULL),

('aisha', 'placeholder_hash', NULL, NULL, 'Staff',
 'Organizes deaf-awareness dinners and cooking classes.',
 'Our Silent Dinners sell out monthly—guests leave with new ASL skills and full bellies!',
 'Next "Vegan + ASL 101" workshop on July 20.',
 'Aisha', '', 'Image', 0.00, NULL),

('tom', 'placeholder_hash', NULL, NULL, 'Staff',
 'Trains all staff on POS systems and customer service in ASL/English.',
 'I''ve worked 10+ restaurants—none made me prouder than hiring my first deaf trainee last month.',
 'His "Kindness Challenge" (round up your bill to donate to deaf youth programs).',
 'Tom', '', 'Image', 0.00, NULL),

('priya', 'placeholder_hash', NULL, NULL, 'Staff',
 'Develops gluten-free desserts with staff-favorite: cashew cheesecake.',
 'I decorate cakes with edible flowers from Carlos'' garden.',
 'Try her "Surprise Dessert" and let her choose for you!',
 'Priya', '', 'Image', 0.00, NULL),

('lena', 'placeholder_hash', NULL, NULL, 'Staff',
 'Trains new staff on digital order systems and ASL greetings.',
 'Lena''s smile lit up our anniversary dinner—she even taught us to sign ''I love you''!',
 'Sketches dish recommendations with emoji ratings on tablets.',
 'Lena', '', 'Image', 0.00, NULL),

('marco', 'placeholder_hash', NULL, NULL, 'Staff',
 'Serves bar drinks with illustrated tasting notes.',
 'Watch for my ''spicy'' warning—it''s a chili pepper doodle!',
 'Leaves origami animals with drink orders (his crane means "enjoy!").',
 'Marco', '', 'Image', 0.00, NULL),

('sarah', 'placeholder_hash', NULL, NULL, 'Staff',
 'Double-checks orders for allergies using color-coded flags.',
 'Deaf or hearing, everyone deserves to eat without fear—our visual allergen system ensures that.',
 'Reduced allergy incidents by 90% with her pictogram system.',
 'Sarah', '', 'Image', 0.00, NULL),

('taro', 'placeholder_hash', NULL, NULL, 'Staff',
 'Masters high-volume shifts with light-up table alerts.',
 'Taro senses when tables need refills before they ask.',
 'Guests love his "mindful dining" reminders (a lotus card with the bill).',
 'Taro', '', 'Image', 0.00, NULL),

('nia', 'placeholder_hash', NULL, NULL, 'Staff',
 'Runs the "Plant Pals" kids'' menu with ASL animal flashcards.',
 'Our toddler ate all her broccoli to learn the ASL sign—miracle!',
 'Draws cartoon veggies on receipts—carrots with superhero capes!',
 'Nia', '', 'Image', 0.00, NULL);


 INSERT INTO Meats (meat_type, description, water_usage_l_per_kg) VALUES 
('Chicken', 'Fresh chicken', 0.5),
('Duck', 'Tender duck', 0.7),
('Fish', 'Wild fish', 0.3),
('Pork', 'Lean pork', 0.6),
('Beef', 'Grass-fed beef', 0.8),
('Egg', 'Organic eggs', 0.1);


INSERT INTO Ingredients (name, water_usage_l_per_kg) VALUES
('almond milk', 0.2),
('almond slices', 0.1),
('avocado', 0.3),
('baby bok choy', 0.4),
('barbecue sauce', 0.5),
('bell peppers', 0.2),
('blueberries', 0.1),
('bok choy', 0.4),
('broccoli', 0.3),
('brown sauce', 0.5),
('cabbage', 0.4),
('carrots', 0.2),
('cashew', 0.2),
('cauliflower', 0.3),
('chocolate chips', 0.1),
('cocoa', 0.2),
('cucumber', 0.2),
('curry sauce', 0.5),
('dipping sauce', 0.5),
('dried tomatoes', 0.1),
('dumpling wrappers', 0.1),
('eggplant', 0.3),
('flour', 0.1),
('fresh peppers', 0.2),
('garlic', 0.1),
('garlic sauce', 0.5),
('general tso''s sauce', 0.5),
('ginger', 0.1),
('gluten-free flour', 0.1),
('hot peppers', 0.2),
('japanese pumpkin', 0.1),
('kale', 0.4),
('king oyster mushrooms', 0.2),
('maple syrup', 0.2),
('mixed vegetables', 0.3),
('mushrooms', 0.2),
('noodles', 0.1),
('oil', 0.3),
('onions', 0.2),
('oyster mushrooms', 0.2),
('peas', 0.3),
('pepper', 0.2),
('pineapple', 0.3),
('plant milk', 0.2),
('potatoes', 0.3),
('pressed tofu skin', 0.1),
('rice', 0.1),
('rice noodles', 0.1),
('salt', 0.1),
('scallions', 0.2),
('seasonal vegetables', 0.3),
('seaweed', 0.1),
('sesame sauce', 0.5),
('snow peas', 0.3),
('soy protein', 0.2),
('soy ribs', 0.6),
('soy sauce', 0.5),
('sugar', 0.1),
('sweet and sour sauce', 0.5),
('tofu', 0.1),
('vegan aioli', 0.5),
('vegan minced meat', 0.6),
('vegan soy chicken', 0.5),
('vegan soy duck', 0.7),
('vegan soy pork', 0.6),
('wood ears', 0.2);

CREATE TABLE WaterSavingBadges (
    badge_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    required_water_saved DECIMAL(10,2) NOT NULL COMMENT 'Required water saved in liters to earn this badge',
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE UserWaterSavingHistory (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_id INT,
    water_saved DECIMAL(10,2) NOT NULL COMMENT 'Water saved in liters',
    badge_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (badge_id) REFERENCES WaterSavingBadges(badge_id)
);

CREATE TABLE UserBadges (
    user_id INT,
    badge_id INT,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, badge_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (badge_id) REFERENCES WaterSavingBadges(badge_id)
);

-- 插入节水徽章数据
INSERT INTO WaterSavingBadges (name, description, required_water_saved, image_url) VALUES
('Sprout Starter', 'You''ve planted your first step toward sustainability!', 50.00, '/static/badges/sprout_starter.png'),
('Aqua Guardian', 'You''re protecting the planet one bite at a time.', 200.00, '/static/badges/aqua_guardian.png'),
('Water Warrior', 'You''ve saved enough water to fill 4 bathtubs. You''re a warrior!', 500.00, '/static/badges/water_warrior.png'),
('Eco Ripple Master', 'Your impact is making waves!', 1000.00, '/static/badges/eco_ripple_master.png'),
('Planet Paladin', 'You''ve saved the world a thousand liters at a time!', 2000.00, '/static/badges/planet_paladin.png'),
('Sustainability Sage', 'A wise guardian of the Earth''s resources.', 5000.00, '/static/badges/sustainability_sage.png'),
('KindPlate Legend', 'Your kindness echoes across the planet.', 10000.00, '/static/badges/kindplate_legend.png');

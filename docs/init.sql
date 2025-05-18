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
 'Created Kind Plate's signature "Root-to-Stem" salad using typically discarded veggie parts.',
 NULL,
 'Sofia', '', 'Image', 0.00, NULL),

('malik', 'placeholder_hash', NULL, NULL, 'Staff',
 'Heads the open-fire grill station, specializing in smoked jackfruit and charred veggies.',
 NULL,
 'Silent Smoke BBQ platter (voted Best Vegan BBQ by Eco Eats).',
 'Malik', '', 'Image', 0.00, NULL),

('diego', 'placeholder_hash', NULL, NULL, 'Staff',
 'Crafts latte art with eco-friendly oat milk, using visual cues to take orders.',
 'Customers love when I 'draw' their requests—yesterday, a panda for a 6-year-old!',
 'His "ASL Alphabet Latte Series" (learn a sign with each order).',
 'Diego', '', 'Image', 0.00, NULL),

('aisha', 'placeholder_hash', NULL, NULL, 'Staff',
 'Organizes deaf-awareness dinners and cooking classes.',
 'Our Silent Dinners sell out monthly—guests leave with new ASL skills and full bellies!',
 'Next "Vegan + ASL 101" workshop on July 20.',
 'Aisha', '', 'Image', 0.00, NULL),

('tom', 'placeholder_hash', NULL, NULL, 'Staff',
 'Trains all staff on POS systems and customer service in ASL/English.',
 'I've worked 10+ restaurants—none made me prouder than hiring my first deaf trainee last month.',
 'His "Kindness Challenge" (round up your bill to donate to deaf youth programs).',
 'Tom', '', 'Image', 0.00, NULL),

('priya', 'placeholder_hash', NULL, NULL, 'Staff',
 'Develops gluten-free desserts with staff-favorite: cashew cheesecake.',
 'I decorate cakes with edible flowers from Carlos' garden.',
 'Try her "Surprise Dessert" and let her choose for you!',
 'Priya', '', 'Image', 0.00, NULL),

('lena', 'placeholder_hash', NULL, NULL, 'Staff',
 'Trains new staff on digital order systems and ASL greetings.',
 'Lena's smile lit up our anniversary dinner—she even taught us to sign 'I love you'!',
 'Sketches dish recommendations with emoji ratings on tablets.',
 'Lena', '', 'Image', 0.00, NULL),

('marco', 'placeholder_hash', NULL, NULL, 'Staff',
 'Serves bar drinks with illustrated tasting notes.',
 'Watch for my 'spicy' warning—it's a chili pepper doodle!',
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
 'Runs the "Plant Pals" kids' menu with ASL animal flashcards.',
 'Our toddler ate all her broccoli to learn the ASL sign—miracle!',
 'Draws cartoon veggies on receipts—carrots with superhero capes!',
 'Nia', '', 'Image', 0.00, NULL);


 INSERT INTO Meats (meat_type, description) VALUES 
('Chicken', 'Fresh chicken'),
('Duck', 'Tender duck'),
('Fish', 'Wild fish'),
('Pork', 'Lean pork'),
('Beef', 'Grass-fed beef'),
('Egg', 'Organic eggs');

-- Insert sample ingredients
INSERT INTO Ingredients (name, description, meat_id) VALUES
('Rice Noodles', 'Thin rice noodles perfect for soups', NULL),
('Mushroom Mix', 'Mixed variety of fresh mushrooms', NULL),
('Soy Sauce', 'Traditional fermented soy sauce', NULL),
('Tofu', 'Firm organic tofu', NULL),
('Seaweed', 'Dried seaweed sheets', NULL),
('Bamboo Shoots', 'Fresh bamboo shoots', NULL),
('Green Onions', 'Fresh chopped green onions', NULL),
('Ginger', 'Fresh grated ginger', NULL),
('Plant-based Chicken', 'Soy-based chicken alternative', NULL),
('Vegan Fish Sauce', 'Plant-based fish sauce alternative', NULL),
('Coconut Milk', 'Fresh coconut milk', NULL),
('Rice', 'Premium jasmine rice', NULL);

-- Link ingredients to menu items (MenuItemIngredients)
INSERT INTO MenuItemIngredients (menu_item_id, ingredient_id, quantity, unit) VALUES
-- For Vegan Dumplings
(1, 4, 100, 'g'),  -- Tofu
(1, 7, 50, 'g'),   -- Green Onions
(1, 3, 0.05, 'l'), -- Soy Sauce

-- For Sesame "Beef"
(7, 3, 0.1, 'l'),   -- Soy Sauce
(7, 8, 30, 'g'),    -- Ginger
(7, 7, 50, 'g'),    -- Green Onions

-- For Curry "Chicken" Noodle Soup
(16, 1, 200, 'g'),   -- Rice Noodles
(16, 9, 150, 'g'),   -- Plant-based Chicken
(16, 11, 0.4, 'l'),  -- Coconut Milk
(16, 7, 30, 'g'),    -- Green Onions

-- For Home Styled Mapo Tofu
(10, 4, 300, 'g'),   -- Tofu
(10, 3, 0.08, 'l'),  -- Soy Sauce
(10, 7, 30, 'g'),    -- Green Onions
(10, 8, 20, 'g');    -- Ginger

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

INSERT INTO restaurant_profile (name, description, rating, story, image_url, facilities, opening_date, opening_time, closing_time)
VALUES
('Kind Plate', 
 'At Kind Plate, we are redefining the dining experience by blending bold, 100% plant-based flavors with radical inclusivity, environmental stewardship, and community empowerment. Every dish we create is a step towards a healthier planet and a more connected world. Our mission is to prove that great food doesn’t need to compromise taste or values.',
 4.95, 
 'Born from the belief that food can heal both people and the planet, Kind Plate was founded in 2021 by a team of passionate chefs and advocates for social equity. Today, 70% of our dedicated staff are deaf or mute, and we continue to foster an environment where inclusivity, sustainability, and the joy of food bring us together. Every meal here tells a story of resilience, connection, and purpose.',
 'https://example.com/images/kind_plate_fancy_image.jpg', 
 'Wheelchair Accessible, Pet-Friendly, Outdoor Seating, ASL Services, Vegan/Gluten-Free Options, Free Wi-Fi, Zero-Waste Practices, Live Music Nights, Community Cooking Classes', 
 '2021-03-15', 
 '10:00:00', 
 '23:00:00');


INSERT INTO MenuItems (name, description, price, category, available, enable_water_track, image_url)
VALUES 
('Vegan Margherita Pizza', 'Classic cheese-free pizza with fresh basil, vegan mozzarella, and tomato sauce.', 12.99, 'Pizza', TRUE, FALSE, 'https://example.com/images/vegan_margherita.jpg'),
('Vegan Spaghetti Carbonara', 'Spaghetti pasta with a creamy cashew-based sauce, smoked tempeh, and nutritional yeast.', 14.50, 'Pasta', TRUE, FALSE, 'https://example.com/images/vegan_carbonara.jpg'),
('Vegan Caesar Salad', 'Crisp romaine lettuce with dairy-free Caesar dressing, croutons, and vegan parmesan.', 9.25, 'Salad', TRUE, FALSE, 'https://example.com/images/vegan_caesar_salad.jpg'),
('Grilled Veggie Sandwich', 'Grilled seasonal vegetables with lettuce, tomato, and a creamy vegan aioli on toasted whole-grain bread.', 11.75, 'Sandwich', TRUE, FALSE, 'https://example.com/images/grilled_veggie_sandwich.jpg'),
('Vegan Tiramisu', 'Traditional Italian coffee-flavored dessert made with coconut cream and dairy-free ladyfingers.', 6.80, 'Dessert', TRUE, FALSE, 'https://example.com/images/vegan_tiramisu.jpg');

INSERT INTO Users (username, password_hash, email, phone_number, role, role_description, story, achievements, first_name, last_name, image_url, contribution, address)
VALUES
('emma_gm', 'hashed_password_1', 'emma@email.com', '1234567890', 'Waiter', 'Oversees operations and staff training in ASL/accessibility.', 'I left corporate hospitality to work here—seeing deaf and hearing staff collaborate so seamlessly is magic.', 'Increased deaf hires by 80% in 2026.', 'Emma', 'Smith', 'https://example.com/images/emma.jpg', 0.00, '123 Main St, City, Country'),

('chef_sofia', 'hashed_password_2', 'sofia@email.com', '1234567891', 'Waiter', 'Designs zero-waste menus and trains staff on composting.', 'Flavor Without Footprints', 'Created "Root-to-Stem" salad using typically discarded veggie parts.', 'Created "Root-to-Stem" salad using typically discarded veggie parts.', 'Sofia', 'Lopez', 'https://example.com/images/sofia.jpg', 0.00, '456 Elm St, City, Country'),

('chef_malik', 'hashed_password_3', 'malik@email.com', '1234567892', 'Waiter', 'Heads the open-fire grill station, specializing in smoked jackfruit and charred veggies.', 'Fire and Flavor, No Words Needed', 'Created the "Silent Smoke" BBQ platter, voted Best Vegan BBQ by Eco Eats.', 'Created the "Silent Smoke" BBQ platter, voted Best Vegan BBQ by Eco Eats.', 'Malik', 'Jones', 'https://example.com/images/malik.jpg', 0.00, '789 Oak St, City, Country'),

('diego_barista', 'hashed_password_4', 'diego@email.com', '1234567893', 'Waiter', 'Crafts latte art with eco-friendly oat milk, using visual cues to take orders.', 'Speaking Through Coffee Art', 'Created the "ASL Alphabet Latte Series" where customers learn a sign with each order.', 'Created the "ASL Alphabet Latte Series" for educational fun.', 'Diego', 'Martinez', 'https://example.com/images/diego.jpg', 0.00, '101 Pine St, City, Country'),

('aisha_events', 'hashed_password_5', 'aisha@email.com', '1234567894', 'Waiter', 'Organizes deaf-awareness dinners and cooking classes.', 'Building Bridges with Vegan Feasts', 'Our Silent Dinners sell out monthly—guests leave with new ASL skills and full bellies!', 'Organized monthly Silent Dinners that sell out each time.', 'Aisha', 'Williams', 'https://example.com/images/aisha.jpg', 0.00, '202 Maple St, City, Country'),

('tom_cashier', 'hashed_password_6', 'tom@email.com', '1234567895', 'Waiter', 'Trains all staff on POS systems and customer service in ASL/English.', 'The Bridge Between Kitchen and Community', 'Introduced the "Kindness Challenge" which encourages customers to donate to deaf youth programs.', 'Implemented the "Kindness Challenge" to support deaf youth programs.', 'Tom', 'Taylor', 'https://example.com/images/tom.jpg', 0.00, '303 Cedar St, City, Country'),

('priya_pastry', 'hashed_password_7', 'priya@email.com', '1234567896', 'Waiter', 'Develops gluten-free desserts, including a fan-favorite: cashew cheesecake.', 'Sweetness Needs No Words', 'Decorates cakes with edible flowers from Carlos’ garden.', 'Developed gluten-free desserts with popular cashew cheesecake.', 'Priya', 'Davis', 'https://example.com/images/priya.jpg', 0.00, '404 Birch St, City, Country'),

('lena_waitress', 'hashed_password_8', 'lena@email.com', '1234567897', 'Waiter', 'Trains new staff on digital order systems and ASL greetings.', 'Connecting Through Gestures & Tech', 'Sketches dish recommendations on tablets with emoji ratings.', 'Famous for sketching dish recommendations with emoji ratings on tablets.', 'Lena', 'Miller', 'https://example.com/images/lena.jpg', 0.00, '505 Willow St, City, Country'),

('marco_waiter', 'hashed_password_9', 'marco@email.com', '1234567898', 'Waiter', 'Serves bar drinks with illustrated tasting notes.', 'Mixology Without a Word', 'Leaves origami animals with drink orders to communicate flavors.', 'Known for leaving origami animals with drink orders, each with a meaning.', 'Marco', 'Garcia', 'https://example.com/images/marco.jpg', 0.00, '606 Fir St, City, Country'),

('sarah_allergy', 'hashed_password_10', 'sarah@email.com', '1234567899', 'Waiter', 'Double-checks orders for allergies using color-coded flags.', 'Your Safe Dining Guardian', 'Created a pictogram system that reduced allergy incidents by 90%.', 'Developed a color-coded allergen system that greatly reduced incidents.', 'Sarah', 'Johnson', 'https://example.com/images/sarah.jpg', 0.00, '707 Redwood St, City, Country'),

('taro_server', 'hashed_password_11', 'taro@email.com', '1234567800', 'Waiter', 'Masters high-volume shifts with light-up table alerts.', 'Calm in the Chaos', 'Known for mindful dining reminders with a lotus card with the bill.', 'Known for anticipating refills before customers ask, providing a calm experience.', 'Taro', 'Lee', 'https://example.com/images/taro.jpg', 0.00, '808 Ash St, City, Country'),

('nia_kids', 'hashed_password_12', 'nia@email.com', '1234567801', 'Waiter', 'Runs the "Plant Pals" kids’ menu with ASL animal flashcards.', 'Making Little Vegans Smile', 'Draws cartoon veggies on receipts, making the experience fun for kids.', 'Created a unique kids’ menu featuring fun ASL animal flashcards.', 'Nia', 'Kim', 'https://example.com/images/nia.jpg', 0.00, '909 Cherry St, City, Country');



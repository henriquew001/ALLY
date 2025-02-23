#!/bin/bash

# Verzeichnis für die SQL-Dateien
INIT_DIR="../database/init/"

# 00-create-users.sql
cat <<EOF > "$INIT_DIR/00-create-users.sql"
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store password as a hash!
    email VARCHAR(255) UNIQUE NOT NULL,
    role ENUM('basic', 'premium', 'professional', 'admin') NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    height INT,
    weight INT,
    goals TEXT,
    activation_code VARCHAR(255),
    activated BOOLEAN DEFAULT FALSE
);
EOF

# 01-create-meal_types.sql
cat <<EOF > "$INIT_DIR/01-create-meal_types.sql"
CREATE TABLE IF NOT EXISTS meal_types (
    meal_type_id INT AUTO_INCREMENT PRIMARY KEY,
    meal_type_name VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO meal_types (meal_type_name) VALUES
('Breakfast'),
('Brunch'),
('Lunch'),
('Dinner'),
('Snack'),
('Dessert'),
('Pre-workout Meal'),
('Post-workout Meal'),
('Midnight Snack');
EOF

# 02-create-food_groups.sql
cat <<EOF > "$INIT_DIR/02-create-food_groups.sql"
CREATE TABLE IF NOT EXISTS food_groups (
    food_group_id INT AUTO_INCREMENT PRIMARY KEY,
    food_group_name VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO food_groups (food_group_name) VALUES
('Cereals and Tubers'),
('Vegetables'),
('Fruits'),
('Beans'),
('Dairy'),
('Meats, Eggs, and Vegetable Proteins'),
('Oils and Fats'),
('Sugars and Sweets');
EOF

# 03-create-food_items.sql
cat <<EOF > "$INIT_DIR/03-create-food_items.sql"
CREATE TABLE IF NOT EXISTS food_items (
    food_item_id INT AUTO_INCREMENT PRIMARY KEY,
    food_group_id INT,
    food_item_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (food_group_id) REFERENCES food_groups(food_group_id)
);

INSERT INTO food_items (food_group_id, food_item_name) VALUES
-- Cereals and Tubers
(1, 'Rice'),
(1, 'Potatoes'),
(1, 'Bread'),
(1, 'Oats'),
(1, 'Corn'),
(1, 'Quinoa'),

-- Vegetables
(2, 'Carrots'),
(2, 'Broccoli'),
(2, 'Spinach'),
(2, 'Tomatoes'),
(2, 'Lettuce'),
(2, 'Onions'),
(2, 'Bell peppers'),
(2, 'Cucumbers'),

-- Fruits
(3, 'Apples'),
(3, 'Bananas'),
(3, 'Oranges'),
(3, 'Grapes'),
(3, 'Strawberries'),
(3, 'Blueberries'),

-- Beans
(4, 'Black beans'),
(4, 'Lentils'),
(4, 'Chickpeas'),
(4, 'Kidney beans'),

-- Dairy
(5, 'Milk'),
(5, 'Yogurt'),
(5, 'Cheese'),

-- Meats, Eggs, and Vegetable Proteins
(6, 'Chicken'),
(6, 'Beef'),
(6, 'Fish'),
(6, 'Eggs'),
(6, 'Tofu'),
(6, 'Almonds'),
(6, 'Walnuts'),
(6, 'Chia seeds'),

-- Oils and Fats
(7, 'Olive oil'),
(7, 'Avocado oil'),
(7, 'Butter'),

-- Sugars and Sweets
(8, 'Sugar'),
(8, 'Honey'),
(8, 'Chocolate'),
(8, 'Candy');
EOF

# 04-create-meals.sql
cat <<EOF > "$INIT_DIR/04-create-meals.sql"
CREATE TABLE IF NOT EXISTS meals (
    meal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_type_id INT,
    meal_date DATE,
    meal_time TIME,
    description TEXT,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_type_id) REFERENCES meal_types(meal_type_id)
);
EOF

# 05-create-meal_items.sql
cat <<EOF > "$INIT_DIR/05-create-meal_items.sql"
CREATE TABLE IF NOT EXISTS meal_items (
    meal_item_id INT AUTO_INCREMENT PRIMARY KEY,
    meal_id INT,
    food_item_id INT,
    quantity DECIMAL(10, 2),
    FOREIGN KEY (meal_id) REFERENCES meals(meal_id),
    FOREIGN KEY (food_item_id) REFERENCES food_items(food_item_id)
);
EOF

# 06-create-shopping_list.sql
cat <<EOF > "$INIT_DIR/06-create-shopping_list.sql"
CREATE TABLE IF NOT EXISTS shopping_list (
    shopping_list_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_id INT,
    item_date DATE,
    quantity DECIMAL(10, 2),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
);
EOF

# 07-create-food_diary.sql
cat <<EOF > "$INIT_DIR/07-create-food_diary.sql"
CREATE TABLE IF NOT EXISTS food_diary (
    diary_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_type_id INT,
    diary_date DATE,
    diary_time TIME,
    notes TEXT,
    feeling ENUM('Excellent', 'Good', 'Neutral', 'Poor', 'Very Poor'),
    feeling_details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_type_id) REFERENCES meal_types(meal_type_id)
);
EOF

# 08-create-food_diary_entries.sql
cat <<EOF > "$INIT_DIR/08-create-food_diary_entries.sql"
CREATE TABLE IF NOT EXISTS food_diary_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    diary_date DATE,
    entry_time TIME,
    meal_type_id INT,
    hunger_level ENUM('Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely'),
    food_consumed TEXT,
    quantity VARCHAR(255),
    feeling ENUM('Excellent', 'Good', 'Neutral', 'Poor', 'Very Poor'),
    feeling_details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_type_id) REFERENCES meal_types(meal_type_id)
);
EOF

# 09-create-habits.sql
cat <<EOF > "$INIT_DIR/09-create-habits.sql"
CREATE TABLE IF NOT EXISTS habits (
    habit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    habit_name VARCHAR(255),
    habit_date DATE,
    habit_time TIME,
    completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
EOF

# 10-create-measurements.sql
cat <<EOF > "$INIT_DIR/10-create-measurements.sql"
CREATE TABLE IF NOT EXISTS measurements (
    measurement_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    measurement_datetime DATETIME,
    weight DECIMAL(5, 2),
    abdominal_circumference DECIMAL(5, 2),
    arms DECIMAL(5, 2),
    calves DECIMAL(5, 2),
    hips DECIMAL(5, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
EOF

# 11-insert-initial-data.sql
cat <<EOF > "$INIT_DIR/11-insert-initial-data.sql"
-- Admin user
INSERT INTO users (username, password, email, role, activated) VALUES ('admin', 'your_strong_admin_password_hashed', 'admin@consciousfit.com', 'admin', true);
-- Professional user
INSERT INTO users (username, password, email, role, activated) VALUES ('professional1', 'professional_password_hashed', 'professional1@consciousfit.com', 'professional', true);
-- Basic user
INSERT INTO users (username, password, email, role, activated) VALUES ('user1', 'user_password_hashed', 'user1@example.com', 'basic', true);
-- Premium user
INSERT INTO users (username, password, email, role, activated) VALUES ('premium1', 'premium_password_hashed', 'premium1@example.com', 'premium', true);
EOF

# Verzeichnis erstellen, falls es nicht existiert
mkdir -p "$INIT_DIR"

echo "SQL-Dateien wurden im Verzeichnis '$INIT_DIR' erstellt."

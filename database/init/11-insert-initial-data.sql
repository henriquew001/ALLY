-- Admin user
INSERT INTO users (username, password, email, role, activated) VALUES ('admin', 'your_strong_admin_password_hashed', 'admin@consciousfit.com', 'admin', true);
-- Professional user
INSERT INTO users (username, password, email, role, activated) VALUES ('professional1', 'professional_password_hashed', 'professional1@consciousfit.com', 'professional', true);
-- Basic user
INSERT INTO users (username, password, email, role, activated) VALUES ('user1', 'user_password_hashed', 'user1@example.com', 'basic', true);
-- Premium user
INSERT INTO users (username, password, email, role, activated) VALUES ('premium1', 'premium_password_hashed', 'premium1@example.com', 'premium', true);

CREATE SCHEMA IF NOT EXISTS chat;

CREATE TABLE IF NOT EXISTS chat.users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    online BOOLEAN NOT NULL,
    ip_addr VARCHAR(50),
    port INT
);

CREATE TABLE IF NOT EXISTS chat.messages (
    message_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sender_id INT REFERENCES chat.users(user_id),
    receiver_id INT REFERENCES chat.users(user_id),
    message_text TEXT
);

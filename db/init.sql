CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR (200) UNIQUE NOT NULL, 
    displayname VARCHAR (200),
    email VARCHAR (200), 
    balance int DEFAULT 0,
    created_on TIMESTAMP NOT NULL,
    last_login TIMESTAMP
    );

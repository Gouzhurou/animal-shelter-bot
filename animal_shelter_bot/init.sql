CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0),
    city VARCHAR(30) NOT NULL,
    role user_role NOT NULL
);
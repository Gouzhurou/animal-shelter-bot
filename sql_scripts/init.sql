CREATE TABLE client (
    id      BIGSERIAL PRIMARY KEY,
    name    VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    email   VARCHAR(50) NOT NULL,
    age     INTEGER     NOT NULL CHECK (age >= 0),
    city    VARCHAR(30) NOT NULL,
    role    VARCHAR(10) NOT NULL CHECK (role IN ('user', 'admin'))
);

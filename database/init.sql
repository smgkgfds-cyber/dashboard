CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    employees INTEGER NOT NULL
);

INSERT INTO companies (name, industry, city, employees)
VALUES
    ('Northwind Analytics', 'Analytics', 'Tallinn', 120),
    ('Baltic Retail', 'Retail', 'Riga', 340),
    ('Data Systems', 'IT', 'Vilnius', 210),
    ('Smart Logistics', 'Logistics', 'Tallinn', 185),
    ('Finance Group', 'Finance', 'Riga', 450);
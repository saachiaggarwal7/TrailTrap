-- MySQL dump
-- FinCore Technologies
-- Backup Date: 2025-05-31

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    department VARCHAR(50),
    email VARCHAR(100),
    joined_on DATE
);

INSERT INTO employees VALUES
(101,'Jason Morris','Finance','jason_morris@fincore.internal','2022-01-15'),
(102,'Sasha Lee','Engineering','sasha_lee@fincore.internal','2021-08-12'),
(103,'Ajay Sharma','Infrastructure','ajay_sharma@fincore.internal','2023-02-20'),
(104,'Emma Williams','HR','emma_williams@fincore.internal','2022-09-10');
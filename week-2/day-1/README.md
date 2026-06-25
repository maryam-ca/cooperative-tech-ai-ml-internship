# Week 2 - Day 6

# SQL Fundamentals: SELECT, JOINs, GROUP BY & Window Functions

## Cooperative Tech Private Limited – AI/ML Internship Program

### Prepared By: Maryam Fatima
### Week: 2
### Day: 6
### Date: June 2026

---

# Introduction

Day 6 marked the beginning of Week 2 of the AI/ML Internship Program and introduced SQL (Structured Query Language), one of the most essential technologies used in Data Science, Data Analytics, Machine Learning, and Database Management.

Unlike CSV files used in Week 1, real-world business data is usually stored in relational databases. SQL provides a powerful way to retrieve, filter, organize, and analyze this data efficiently. During this task, PostgreSQL and pgAdmin 4 were used to create databases, manage tables, insert records, and execute various SQL queries.

This practical exercise provided hands-on experience with database operations and demonstrated how structured data can be manipulated and analyzed using SQL.

---

# Objectives

## The main objectives of this task were:

- Understand Relational Databases
- Learn SQL Fundamentals
- Create and Manage Tables
- Insert and Retrieve Data
- Apply Filtering and Sorting Techniques
- Use Aggregate Functions
- Perform Grouping Operations
- Connect Multiple Tables using JOINs
- Implement Window Functions
- Analyze Structured Data Efficiently

---

# Tools and Technologies Used

## PostgreSQL

PostgreSQL was used as the Relational Database Management System (RDBMS) for storing and managing data.

## pgAdmin 4

pgAdmin 4 was used as the graphical interface for writing and executing SQL queries.

## SQL

Structured Query Language (SQL) was used for database interaction and data analysis.

## Git & GitHub

Git and GitHub were used for version control and project submission.

---

# Database Creation

## Database Name

```text
hms_db2
```

A dedicated PostgreSQL database was created to perform all Day 6 SQL activities.

---

# Table Creation

## Employees Table

The Employees table was created to store employee information.

### Attributes

| Column Name | Data Type |
|------------|-----------|
| employee_id | INT |
| name | VARCHAR(50) |
| department | VARCHAR(50) |
| salary | INT |
| age | INT |

### SQL Query

```sql
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary INT,
    age INT
);
```

---

# Data Insertion

Sample employee records were inserted into the table.

### SQL Query

```sql
INSERT INTO employees VALUES
(1,'Ali','IT',50000,24),
(2,'Sara','HR',45000,26),
(3,'Ahmed','IT',70000,30),
(4,'Fatima','Finance',60000,28),
(5,'Bilal','IT',55000,25),
(6,'Ayesha','HR',48000,27),
(7,'Usman','Finance',65000,31),
(8,'Zain','Marketing',52000,29);
```

### Result

Eight employee records were successfully inserted into the Employees table.

---

# SQL Operations Performed

## 1. Retrieving All Records

The SELECT statement was used to display all employee records.

### SQL Query

```sql
SELECT * FROM employees;
```

### Purpose

To verify that data had been inserted correctly.

---

## 2. Selecting Specific Columns

Only the required columns were retrieved from the table.

### SQL Query

```sql
SELECT name, salary
FROM employees;
```

### Purpose

To display employee names and salaries only.

---

## 3. Filtering Records Using WHERE

The WHERE clause was used to filter records based on specific conditions.

### SQL Query

```sql
SELECT *
FROM employees
WHERE salary > 50000;
```

### Purpose

To identify employees earning more than 50,000.

---

## 4. Sorting Data Using ORDER BY

Records were sorted according to salary.

### SQL Query

```sql
SELECT *
FROM employees
ORDER BY salary DESC;
```

### Purpose

To display employees from highest salary to lowest salary.

---

## 5. Limiting Results Using LIMIT

The LIMIT clause was used to retrieve only the top records.

### SQL Query

```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 3;
```

### Purpose

To display the top three highest-paid employees.

---

# Aggregate Functions

Aggregate functions were used to perform calculations on multiple rows.

---

## COUNT()

### SQL Query

```sql
SELECT COUNT(*)
FROM employees;
```

### Purpose

To calculate the total number of employees.

---

## AVG()

### SQL Query

```sql
SELECT AVG(salary)
FROM employees;
```

### Purpose

To calculate the average salary.

---

## MAX()

### SQL Query

```sql
SELECT MAX(salary)
FROM employees;
```

### Purpose

To identify the highest salary.

---

## MIN()

### SQL Query

```sql
SELECT MIN(salary)
FROM employees;
```

### Purpose

To identify the lowest salary.

---

## SUM()

### SQL Query

```sql
SELECT SUM(salary)
FROM employees;
```

### Purpose

To calculate the total salary expenditure.

---

# GROUP BY Operations

The GROUP BY clause was used to organize records into groups.

---

## Average Salary by Department

### SQL Query

```sql
SELECT department,
AVG(salary) AS average_salary
FROM employees
GROUP BY department;
```

### Purpose

To calculate the average salary for each department.

---

## Employee Count by Department

### SQL Query

```sql
SELECT department,
COUNT(*) AS total_employees
FROM employees
GROUP BY department;
```

### Purpose

To determine the number of employees working in each department.

---

# Working with Multiple Tables

To understand relationships between tables, a second table named Projects was created.

---

# Projects Table

### Attributes

| Column Name | Data Type |
|------------|-----------|
| project_id | INT |
| employee_id | INT |
| project_name | VARCHAR(100) |

### SQL Query

```sql
CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    employee_id INT,
    project_name VARCHAR(100)
);
```

---

# Project Data Insertion

### SQL Query

```sql
INSERT INTO projects VALUES
(1,1,'ERP System'),
(2,3,'AI Assistant'),
(3,4,'Finance Portal'),
(4,7,'Billing System');
```

---

# SQL JOIN Operations

JOIN operations were performed to combine data from multiple tables.

---

## INNER JOIN

### SQL Query

```sql
SELECT
e.name,
p.project_name
FROM employees e
INNER JOIN projects p
ON e.employee_id = p.employee_id;
```

### Purpose

To display employees who are assigned to projects.

### Outcome

Only matching records from both tables were displayed.

---

## LEFT JOIN

### SQL Query

```sql
SELECT
e.name,
p.project_name
FROM employees e
LEFT JOIN projects p
ON e.employee_id = p.employee_id;
```

### Purpose

To display all employees regardless of whether they are assigned to a project.

### Outcome

All employees were displayed, including those without projects.

---

# Window Functions

Window Functions were used to perform calculations across rows while preserving individual records.

---

## ROW_NUMBER()

### SQL Query

```sql
SELECT
name,
salary,
ROW_NUMBER()
OVER(
ORDER BY salary DESC
) AS ranking
FROM employees;
```

### Purpose

To assign a unique ranking to employees based on salary.

---

## RANK()

### SQL Query

```sql
SELECT
name,
salary,
RANK()
OVER(
ORDER BY salary DESC
) AS ranking
FROM employees;
```

### Purpose

To rank employees according to salary.

---

## Running Total

### SQL Query

```sql
SELECT
name,
salary,
SUM(salary)
OVER(
ORDER BY salary
) AS running_total
FROM employees;
```

### Purpose

To calculate cumulative salary totals.

---

## PARTITION BY

### SQL Query

```sql
SELECT
department,
name,
salary,
SUM(salary)
OVER(
PARTITION BY department
ORDER BY salary
) AS department_total
FROM employees;
```

### Purpose

To calculate department-wise running totals.

---

# Challenges Faced

## During this task, the following challenges were encountered:

- Understanding relational database concepts
- Learning how tables are connected through keys
- Writing JOIN queries correctly
- Understanding GROUP BY operations
- Implementing Window Functions
- Working with multiple SQL statements

These challenges were resolved through practical implementation and repeated query execution.

---

# Key Learnings

## After completing Day 6, the following concepts were learned:

- Database Fundamentals
- SQL Query Writing
- Data Retrieval Techniques
- Filtering and Sorting Data
- Aggregate Functions
- Group-Based Analysis
- Relational Database Design
- Table Relationships
- INNER JOIN and LEFT JOIN
- Window Functions
- SQL-Based Data Analysis

---

# Conclusion

Day 6 provided a comprehensive introduction to SQL and relational databases. Multiple SQL operations were successfully performed, including table creation, data insertion, filtering, sorting, aggregation, grouping, joining tables, and implementing advanced window functions.

The knowledge gained through this task established a strong foundation for future database management, data analysis, and machine learning workflows. SQL is an essential skill for every Data Analyst, Data Scientist, and AI/ML Engineer, and this activity significantly improved practical database handling skills.

---

# Status

✅ Database Created

✅ Employees Table Created

✅ Projects Table Created

✅ Data Inserted Successfully

✅ SELECT Queries Completed

✅ WHERE Filtering Completed

✅ ORDER BY Implemented

✅ Aggregate Functions Applied

✅ GROUP BY Operations Completed

✅ INNER JOIN Completed

✅ LEFT JOIN Completed

✅ Window Functions Implemented

✅ PostgreSQL Successfully Used

✅ Day 6 Successfully Completed
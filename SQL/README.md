Day 3 Task Plan (SQL Power Day)
🔹 Part 1: SQL Concepts to Learn (2–3 hours)
1️⃣ SQL Joins (very important for real projects & interviews)

Focus on:

INNER JOIN

LEFT JOIN

RIGHT JOIN

FULL JOIN (theory + use case)

👉 Practice understanding:

When data matches

When data is missing

How NULLs appear

Tables to imagine:

employees

departments

orders

customers

2️⃣ Subqueries (Beginner → Intermediate)

Learn:

Subquery in WHERE

Subquery in SELECT

Subquery in FROM

IN, EXISTS, ANY, ALL

Key idea:

“Query inside a query to answer complex questions simply.”

🔹 Part 2: Solve 15 Real SQL Queries (3–4 hours)

Use 3 tables (this mimics real-world work):

🗂 Tables

employees(emp_id, name, dept_id, salary)

departments(dept_id, dept_name)

orders(order_id, emp_id, amount, order_date)

🧠 15 Real SQL Practice Questions
🔸 Joins (1–8)

Get all employees with their department names

Get employees who don’t belong to any department

Get all departments even if they have no employees

Find employees working in the Sales department

Count employees in each department

Find departments with more than 5 employees

Get employee names and total order amount they handled

Find employees who have never handled any orders

🔸 Subqueries (9–15)

Find employees earning more than average salary

Find employees earning the highest salary

Find departments with average salary > 50,000

Find employees who handled orders worth more than total average order amount

Find employees whose salary is higher than any employee in Sales

Find employees whose salary is higher than all employees in HR

Find the second highest salary (classic 🔥)

🔹 Part 3: Mini Challenge (Optional but 🔥)

👉 Write 2 queries using:

JOIN + subquery

GROUP BY + HAVING + subquery

Example:

“Employees whose total order amount is greater than the company average”
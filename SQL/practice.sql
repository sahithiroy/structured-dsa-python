SELECT * FROM employees;

comment:Get all employees with their department names

select e.name,e.emp_id,e.dept_id,e.salary,d.dept_name d.dept_id 
from employee e
left join department d
on e.dept_id=d.dept_id;


comment:Get employees who don’t belong to any department
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
LEFT JOIN departments d
ON e.dept_id = d.dept_id
WHERE e.dept_id IS NULL;


comment:Get all departments even if they have no employees
select e.name,e.emp_id,e.dept_id,e.salary,d.dept_name d.dept_id 
from employee e
right join department d
on e.dept_id=d.dept_id where e.emp_id is null;

comment:Find employees working in the Sales department
select e.name,e.emp_id,e.dept_id,e.salary,d.dept_name d.dept_id 
from employee e
right join department d
on e.dept_id=d.dept_id where d.dept_name='Sales';

comment:Count employees in each department
select d.dept_name, count(e.emp_id) as employee_count
from department d 
left join employee e on d.dept_id = e.dept_id
group by d.dept_name;


comment:Find departments with more than 5 employees
select d.dept_name, count(e.emp_id) as employee_count
from department d 
left join employee e on d.dept_id = e.dept_id
group by d.dept_name
having count(e.emp_id) > 5;

comment:Get employee names and total order amount they handled
SELECT e.emp_id, e.name, COALESCE(SUM(o.amount), 0) AS total_order_amount
FROM employees e
LEFT JOIN orders o
ON e.emp_id = o.emp_id
GROUP BY e.emp_id, e.name;


comment:Find employees who have never handled any orders
select e.emp_id,e.name
from employee e
left join orders o on e.emp_id=o.emp_id
where o.emp_id is null;


comment:Find employees earning more than average salary
select emp_id,name,salary from employee
where salary>(select avg(salary) from employee);

comment:Find employees earning the highest salary
select emp_id,name,salary from employee
where salary=(select max(salary) from employee);

comment:Find departments with average salary > 50,000

select d.dept_name, avg(e.salary) as avg_salary
from department d
left join employee e on d.dept_id = e.dept_id
group by d.dept_name
having avg(e.salary) > 50000;


comment:Find employees who handled orders worth more than total average order amount
SELECT e.emp_id, e.name, COALESCE(SUM(o.amount), 0) AS total_order_amount
FROM employees e
LEFT JOIN orders o
ON e.emp_id = o.emp_id
GROUP BY e.emp_id, e.name
HAVING COALESCE(SUM(o.amount), 0) > (SELECT AVG(amount) FROM orders);

comment:Find employees whose salary is higher than any employee in Sales

SELECT e.emp_id, e.name, e.salary
FROM employees e    
WHERE e.salary > (SELECT MAX(salary) FROM employees WHERE dept_id = (SELECT dept_id FROM departments WHERE dept_name = 'Sales'));

comment:Find employees whose salary is higher than all employees in HR
SELECT e.emp_id, e.name, e.salary
FROM employees e    
WHERE e.salary > (SELECT MAX(salary) FROM employees WHERE dept_id = (SELECT dept_id FROM departments WHERE dept_name = 'HR'));

comment:Find the second highest salary
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
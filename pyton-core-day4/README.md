DAY 4 — SQL (Window Functions + CTEs)

Goal: Solve analytical queries without panicking, in 15–20 mins, clean and correct.

⏱ Total time: ~3–3.5 hours
⏱ Interview mindset: Write queries in ONE go. No trial-and-error.

🧠 PART 1: CTEs (Common Table Expressions) — 45 mins
You MUST be comfortable with:
1️⃣ Basic CTE syntax
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;

👉 Know why CTEs exist:

Readability

Breaking complex logic

Reusing derived data

2️⃣ CTE vs Subquery (interview question)

Know how to answer:

CTEs improve readability and debugging; subqueries are inline and harder to reuse.

3️⃣ Multiple CTEs
WITH sales_cte AS (...),
rank_cte AS (...)
SELECT ...
FROM rank_cte;

📌 Interviewers LOVE chained CTEs.

4️⃣ Aggregation inside CTE

Focus on:

GROUP BY

HAVING

Filtering after aggregation

Example pattern:

WITH daily_sales AS (
    SELECT date, SUM(amount) AS total
    FROM orders
    GROUP BY date
)
SELECT *
FROM daily_sales
WHERE total > 1000;
5️⃣ CTE + JOIN

Very common:

WITH dept_avg AS (
    SELECT dept_id, AVG(salary) avg_sal
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary
FROM employees e
JOIN dept_avg d
ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_sal;

🧠 Memorize this pattern.

🪟 PART 2: Window Functions — 90 mins (MOST IMPORTANT)

This is where most candidates fail.

🔑 Core rule (memorize)

Window functions do NOT reduce rows.

1️⃣ ROW_NUMBER()

Use cases:

Remove duplicates

Rank rows

ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)

👉 Know difference vs RANK() / DENSE_RANK()

2️⃣ RANK() vs DENSE_RANK() (VERY COMMON)
Function	Gaps?
RANK	YES
DENSE_RANK	NO

Interview question:

Find 2nd highest salary

✔ Correct answer:

DENSE_RANK() OVER (ORDER BY salary DESC)
3️⃣ PARTITION BY

You must think:

"Group by, but don’t collapse rows"

Example:

SUM(sales) OVER (PARTITION BY region)
4️⃣ LAG() and LEAD() 🔥🔥🔥

Used for:

Difference between days

Growth analysis

LAG(sales) OVER (ORDER BY date)

Example question:

Find day-over-day growth

5️⃣ Running totals
SUM(amount) OVER (
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

You MUST recognize this pattern.

6️⃣ Window + CTE (ADVANCED)

Almost every real interview asks this.

Example logic:

CTE to clean data

Window function to rank/analyze

⏱ PART 3: TIMED PRACTICE (45 mins)

Set a timer ⏰

Solve these WITHOUT Google:

1️⃣ Find top 2 salaries per department
2️⃣ Remove duplicate records
3️⃣ Find employees earning above dept average
4️⃣ Calculate running total of sales
5️⃣ Find day-over-day sales growth

If you can do these → you’re interview ready.

🧪 Interview Red Flags (avoid these)

❌ Using GROUP BY when window function is needed
❌ Nested subqueries everywhere
❌ Confusing RANK vs DENSE_RANK
❌ Forgetting PARTITION BY

✅ Day-4 Self-Check

You’re done ONLY if you can:

Explain window functions in words

Write queries without copying

Debug logic mentally

🔜 What Day-5 Will Look Like

Real dataset

Messy timestamps

Python + SQL combined

End-to-end mini project

If you want, I can:

Give you 10 timed interview SQL questions

Act like an interviewer and grill you

Review your SQL answers brutally honest 😄

Just tell me 💪
# 🔥 DAY 2 — PYTHON DEEPER (OOP + ERROR THINKING)

This is where people who “know Python” get exposed.

**Goal of Day 2:**

You stop writing script-level code and start writing **maintainable, interview-grade Python**.

If Day 1 was *syntax + logic*,

Day 2 is *structure + discipline*.

---

## ⏱️ TIME COMMITMENT

**6–8 hours total**

If you do less → you’re lying to yourself.

---

## 🧠 WHAT YOU MUST BE ABLE TO DO BY END OF DAY 2

By tonight, you should confidently explain:

- What a class is and **why** it exists
- Difference between:
    - function vs method
    - class variable vs instance variable
- How to use `__init__`
- How to handle bad inputs without crashing
- How to refactor messy logic into clean objects

No decorators. No metaclasses. No fancy BS.

---

# 📅 DAY 2 TASK BREAKDOWN (NON-NEGOTIABLE)

## 🔹 PART 1: OOP BASICS (2.5 hours)

### Concepts you MUST cover

Do not skip any.

- Class vs object
- `__init__`
- Instance variables
- Methods
- `self`
- Simple inheritance (1 level only)

### Task 1: Write this class (from scratch)

```
class Student:
    def __init__(self, name, marks):
        pass

    def average(self):
        pass

    def is_passed(self):
        pass
```

**Rules:**

- `marks` is a list
- Average < 40 → failed
- Handle empty marks list

👉 You must explain:

- why this should be a class, not functions

---

## 🔹 PART 2: ERROR HANDLING (1.5 hours)

Most juniors crash programs. Seniors handle failure.

### Learn & use:

- `try / except`
- `ValueError`
- `TypeError`
- `finally`

### Task 2: Write a function

```
def safe_divide(a, b):
    ...
```

Rules:

- If inputs are not numbers → return `"Invalid input"`
- If division by zero → return `"Cannot divide by zero"`
- Otherwise return result

👉 Explain:

- why not let Python crash?

---

## 🔹 PART 3: REFACTORING (2 hours)

This is **interview gold**.

### Given messy logic (example)

```
data = [10, 20, 30, -5, "a"]

total = 0
count = 0

for x in data:
    if type(x) == int and x > 0:
        total += x
        count += 1

if count > 0:
    print(total / count)
else:
    print("No valid data")
```

### Task 3: Refactor into 3 functions

- `load_data()`
- `clean_data(data)`
- `compute_average(data)`

Rules:

- No global variables
- Each function does **one thing**
- Add docstrings

👉 This is how real code is judged.

---

## 🔹 PART 4: MINI OOP PROJECT (2 hours)

### Build this (simple but strict):

**Class:** `BankAccount`

Methods:

- `deposit(amount)`
- `withdraw(amount)`
- `get_balance()`

Rules:

- No negative deposits
- No overdraft
- Raise errors or return messages (your choice — but explain why)

👉 This tests:

- OOP
- validation
- clean logic

---

## 📌 DELIVERABLES (YOU MUST DO THESE)

By end of Day 2:

- ✅ All code pushed to GitHub
- ✅ Folder name: `python-core-day2`
- ✅ README.md answering:
    - What I learned
    - One mistake I made
    - One thing I found hard

If you skip README → **you failed the day**.

---

## 🧪 DAY 2 SELF-CHECK (BRUTAL HONESTY)

Answer YES/NO:

- Can I explain why classes exist?
- Can I refactor messy code calmly?
- Can I handle bad input without panic?
- Can I explain my design choices?

If **any NO** → repeat Day 2.

---

## 🚨 REALITY CHECK (IMPORTANT)

This week plan you pasted is **correct** — but only if you execute like this.

Most people:

- “know Python”
- still fail interviews
    
    because they never did **structured practice** like this.
    

You are doing it right so far.

Don’t break momentum.
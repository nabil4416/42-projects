
---

```markdown
# push_swap (42)

## 📌 Overview
**push_swap** is an algorithmic project from the 42 curriculum.  
The goal is to sort a stack of integers using a limited set of operations, while producing the **minimum number of moves possible**.

This project focuses on:
- algorithmic thinking
- data structures (linked lists, stacks)
- time complexity
- strict memory management in C

---

## 🧠 Core Concepts
- Two stacks: **A** and **B**
- A restricted instruction set (`sa`, `pb`, `ra`, `rra`, …)
- No direct access to array indexing
- Every operation must be explicitly printed

---

## ⚙️ Algorithm Strategy

### 🔹 Small inputs (≤ 5 elements)
For small stacks, a **custom optimized sorting strategy** is used:
- direct comparisons
- minimal rotations
- guaranteed low operation count

### 🔹 Large inputs (> 5 elements)
For larger stacks, the project uses a **binary Radix Sort** approach:

1. Values are first **compressed into indexes** (0 → n-1)
2. Sorting is done **bit by bit**, from least significant to most significant
3. Elements are pushed to stack B or rotated in A depending on the current bit
4. Stack B is merged back into A after each pass

This guarantees:
- predictable complexity
- stable behavior
- scalability up to 500 elements

---

## 🧱 Project Architecture

```

.
├── push_swap.h
├── main.c
├── parse_args.c
├── parse_check.c
├── split_ws.c
├── index.c
├── radix.c
├── sort_small.c
├── stack.c
├── stack_utils.c
├── ops_push.c
├── ops_swap.c
├── ops_rotate.c
├── ops_reverse_rotate.c
├── error.c
├── free.c
└── Makefile

````

---

## 🔐 Memory Management
- No memory leaks
- No double free
- No use-after-free
- All allocations are centralized and properly released

Verified using:
- `valgrind`
- evaluation test suite

---

## 🚀 Usage

### Compile
```bash
make
````

### Run

```bash
./push_swap 3 2 1
```

### Example

```bash
ARG="4 67 3 87 23"
./push_swap $ARG | ./checker $ARG
```

---

## 🧪 Testing

* Official 42 evaluation tests
* Custom edge cases
* Randomized stress tests
* Leak checks with Valgrind

---

## 🎓 Skills Demonstrated

* Algorithm design & optimization
* Linked list manipulation
* Bitwise operations
* Defensive programming in C
* Clean architecture under strict constraints
* Oral defense & code explainability

---

## 🏫 Context

This project was completed as part of the **42 Network curriculum**, under strict coding standards and peer evaluation.

```
---


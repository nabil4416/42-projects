# 🧩 Libft — My First C Library

## 📖 Project Overview

**Libft** is the very first project in the 42 curriculum.  
Its goal is to **rebuild a custom version of the C standard library**, step by step, by re-implementing key standard functions such as `memcpy`, `strdup`, `atoi`, and more — all from scratch, **without using the original library**.

This project is the foundation of everything in the Common Core.  
It forces you to understand how memory works, how pointers behave, and how to write code that is not only functional but also **robust, readable, and leak-free**.

---

## 🧠 Learning Objectives

- Reimplement functions from the **libc**  
- Handle **pointers and type casting** safely  
- Master **dynamic memory allocation and freeing**  
- Work with **arrays and strings** at a low level  
- Build and manipulate **linked lists** (bonus part)  
- Respect the **42 Norminette** and modular project architecture  
- Manage compilation using a **Makefile** and static libraries (`.a`)

---

## 🏗️ Project Architecture

```

libft/
├── Makefile               # Builds the libft.a library
├── libft.h                # All function prototypes + struct definitions
├── ft_*.c                 # Mandatory and additional functions
├── bonus/ft_lst*.c        # Linked list functions (bonus part)
└── main.c                 # Custom test file (not submitted)

````

Each `.c` file implements **one function only**, and all prototypes are declared in `libft.h`.  
The header file also contains the structure definition for linked lists:

```c
typedef struct s_list
{
	void			*content;
	struct s_list	*next;
}	t_list;
````

This structure taught me to manipulate **generic data types** using `void *`, and to understand **type casting** when dealing with unknown data.

---

## ⚙️ Compilation

```bash
make            # Builds libft.a
make clean      # Removes object files
make fclean     # Removes libft.a
make re         # Rebuild everything
```

To use Libft in another project:

```bash
gcc main.c -L. -lft -I. -o test
```

---

## 🔍 Example

```c
#include "libft.h"
#include <stdio.h>

int	main(void)
{
	char	str[] = "Ambition & consistency";
	printf("Length: %zu\n", ft_strlen(str));
	return (0);
}
```

**Expected output:**

```
Length: 21
```

---

## 🧩 Implemented Functions

### 🔹 Part 1 — libc Functions

| Category   | Functions                                                                                                   |
| ---------- | ----------------------------------------------------------------------------------------------------------- |
| Memory     | `ft_memset`, `ft_bzero`, `ft_memcpy`, `ft_memmove`, `ft_memchr`, `ft_memcmp`                                |
| Strings    | `ft_strlen`, `ft_strlcpy`, `ft_strlcat`, `ft_strchr`, `ft_strrchr`, `ft_strncmp`, `ft_strnstr`, `ft_strdup` |
| Characters | `ft_isalpha`, `ft_isdigit`, `ft_isalnum`, `ft_isascii`, `ft_isprint`, `ft_tolower`, `ft_toupper`            |
| Conversion | `ft_atoi`                                                                                                   |
| Allocation | `ft_calloc`                                                                                                 |

### 🔹 Part 2 — Additional Functions

`ft_substr`, `ft_strjoin`, `ft_strtrim`, `ft_split`, `ft_itoa`, `ft_strmapi`, `ft_striteri`, `ft_putchar_fd`, `ft_putstr_fd`, `ft_putendl_fd`, `ft_putnbr_fd`

### 🔹 Bonus — Linked Lists

`ft_lstnew`, `ft_lstadd_front`, `ft_lstadd_back`, `ft_lstsize`, `ft_lstlast`, `ft_lstdelone`, `ft_lstclear`, `ft_lstiter`, `ft_lstmap`

---

## 🧱 How the Project Works (Architecture Explanation)

Libft is **modular**:
each function is self-contained, tested separately, and compiled into object files (`.o`) that are later grouped into a single static library (`libft.a`).

When you link this library, you can call your custom `ft_` functions from any C program as if they were built-in.

The project can be seen as three logical layers:

1. **Low-level memory layer** — `ft_memset`, `ft_bzero`, `ft_memcpy`, `ft_memmove`
   → Teaches you how data moves in memory, byte by byte, and how to handle **overlapping memory regions** safely (`ft_memmove` was one of the hardest to debug).

2. **String manipulation layer** — functions like `ft_strlcpy`, `ft_strtrim`, `ft_split`
   → These were tricky because of **pointer arithmetic**, **null-termination**, and **memory protection** (ensuring you don’t read or write beyond allocated space).

3. **Dynamic data & list layer** — functions using `malloc`, and linked lists (`t_list`)
   → Learning to **allocate, protect, and free** memory correctly was essential, especially in `ft_split`, where each substring must be freed if an allocation fails.

---

## ⚠️ The Hard Parts

### 1️⃣ `void *` and Casting

Understanding `void *` was initially confusing — it’s a **generic pointer** that can point to any data type.
You have to **cast** it before dereferencing, for example:

```c
*(int *)ptr
```

This concept was key for writing `ft_memcpy`, `ft_memmove`, and all list functions.

---

### 2️⃣ Memory Overlap in `ft_memmove`

At first, I didn’t realize that copying bytes **forward** could corrupt data when the source and destination overlap.
The fix was to detect overlap and copy **backward** when necessary:

```c
if (dst > src)
    copy from the end;
else
    copy from the beginning;
```

---

### 3️⃣ Memory Protection

Functions like `ft_strjoin`, `ft_substr`, and `ft_split` require careful allocation:

* Check if `malloc` returned `NULL`
* Never access freed or uninitialized memory
* Always **return `NULL`** when an allocation fails
* Free previously allocated parts before returning

---

### 4️⃣ Freeing `ft_split`

`ft_split` allocates an array of strings — each one must be freed individually.
I implemented a helper to clean up properly:

```c
static void	free_all(char **arr, int i)
{
	while (i >= 0)
		free(arr[i--]);
	free(arr);
}
```

Without this, one failed allocation could lead to massive memory leaks.

---

### 5️⃣ The Norminette Discipline

Keeping each function **under 25 lines**, respecting indentation, and avoiding forbidden constructs was its own challenge.
It forced me to **refactor**, to split complex logic into smaller static helpers, and to write code that is both clean and concise.

---

## 🧪 Testing & Debugging

I tested each function using:

* **Custom `main.c` files** with edge cases
* **Francinette** (42’s official tester)
* **Valgrind** for memory leaks
* **printf debugging** to track pointer values and memory content

Example test for `ft_split`:

```c
char **tab = ft_split(" 42  school  project ", ' ');
for (int i = 0; tab[i]; i++)
	printf("[%s]\n", tab[i]);
ft_free_split(tab);
```

---

## 💡 What I Learned

* Deep understanding of **pointers**, **arrays**, and **memory layout**
* The importance of **defensive programming**
* Writing code that is **leak-free and modular**
* How to think like the **compiler and operating system**
* Real discipline through **Norminette** and code style rules

---

## 🧰 Tools Used

* **Language:** C (C11)
* **Compiler:** `gcc -Wall -Wextra -Werror`
* **OS:** Ubuntu / Linux (42 environment)
* **Editor:** VSCode + Vim
* **Testing tools:** Francinette, Valgrind, custom main files

---

## 🏁 Project Status

✅ Completed and validated
📍 Part of the **Common Core** at **École 19 (42 Brussels Network)**
🔗 [My GitHub Profile](https://github.com/nabil4416)

---

## ✨ Final Thought

> “Understanding memory is understanding the soul of C.
> Everything else is just syntax.”


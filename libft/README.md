```md
# 🧩 Libft — Rebuilding the C Standard Library

![C](https://img.shields.io/badge/language-C-blue)
![Norminette](https://img.shields.io/badge/Norminette-OK-brightgreen)
![42](https://img.shields.io/badge/42%20Project-Libft-%23000000)

---

## 📖 Overview

**Libft** is the very first project in the **42 curriculum**.  
Its goal is to rebuild a **custom version of the C standard library**, from scratch — by re-implementing fundamental functions such as `memcpy`, `strdup`, `atoi`, and more, **without using the original libc**.

This project lays the foundation for all upcoming work in the Common Core.  
It teaches you how memory really works, how pointers behave, and how to write code that is **robust, modular, and memory-safe**.

---

## 🧠 Learning Objectives

- Recreate standard **libc** functions  
- Understand and manipulate **pointers and type casting**  
- Master **dynamic memory allocation and freeing**  
- Manipulate **arrays, strings, and lists** at a low level  
- Write **clean, Norminette-compliant** code  
- Build and manage a **static library** (`libft.a`)  
- Organize code into **modular folders** and compile with a **Makefile**

---

## 🏗️ Project Architecture

```

libft/
├── includes/
│   └── libft.h                # All function prototypes
├── srcs/
│   ├── ctype/                 # Character classification (ft_isalpha, ft_isdigit, etc.)
│   ├── string/                # String manipulation (ft_strlen, ft_strdup, etc.)
│   ├── memory/                # Memory operations (ft_memcpy, ft_memmove, etc.)
│   ├── convert/               # Conversion functions (ft_atoi, ft_itoa, etc.)
│   ├── io/                    # Output to file descriptors (ft_putchar_fd, etc.)
│   └── list/                  # Bonus: linked lists (ft_lstnew, ft_lstadd_back, etc.)
├── Makefile
└── README.md

````

Each `.c` file contains **a single function**, and all prototypes are declared in `includes/libft.h`.  
The header also defines the `t_list` structure for the bonus part:

```c
typedef struct s_list
{
	void			*content;
	struct s_list	*next;
}	t_list;
````

This structure helped me understand **generic pointers (`void *`)**, and how to safely cast them when manipulating arbitrary data.

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
gcc main.c -L. -lft -Iincludes -o test
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

**Output:**

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

## 🧱 Internal Architecture & Key Concepts

Libft is **modular**: each function is self-contained, tested independently, and compiled into `.o` files that are later grouped into a static library (`libft.a`).

When linked, this library lets you use your own `ft_` functions in any C program as if they were built-in.

### 1️⃣ Low-Level Memory Layer

Functions like `ft_memset`, `ft_bzero`, `ft_memcpy`, and `ft_memmove` taught me how data moves **byte by byte** in memory — and how to handle **overlaps** safely in `ft_memmove`.

### 2️⃣ String Manipulation Layer

Functions like `ft_strlcpy`, `ft_strtrim`, or `ft_split` required mastering **pointer arithmetic**, **NULL-termination**, and **memory safety**.

### 3️⃣ Dynamic Data Layer

Functions using `malloc` (like `ft_itoa`, `ft_split`, or linked lists) introduced **error handling**, **clean-up on failure**, and **freeing partial allocations**.

---

## ⚠️ The Tricky Parts

### 🔸 `void *` and Casting

Understanding `void *` was key — it can point to **any type**, but you must cast it before dereferencing:

```c
*(int *)ptr;
```

### 🔸 Handling Overlap in `ft_memmove`

Copying bytes forward caused corruption when source and destination overlapped.
Solution: detect overlap and copy **backward** if necessary.

### 🔸 Memory Protection

Functions like `ft_split` require robust protection:

* Check every `malloc`
* Free previous allocations on failure
* Always return `NULL` safely

Helper function:

```c
static void	free_all(char **arr, int i)
{
	while (i >= 0)
		free(arr[i--]);
	free(arr);
}
```

### 🔸 Norminette Discipline

Keeping every function under **25 lines**, with perfect indentation and no forbidden constructs, forced clean design and modular thinking.

---

## 🧪 Testing & Debugging

I tested with:

* **Custom main.c** edge cases
* **Francinette** (42 tester)
* **Valgrind** for leaks
* **printf debugging** to visualize memory and pointer behavior

Example:

```c
char **tab = ft_split(" 42  school  project ", ' ');
for (int i = 0; tab[i]; i++)
	printf("[%s]\n", tab[i]);
ft_free_split(tab);
```

---

## 🧰 Tools Used

* **Language:** C (C11)
* **Compiler:** `gcc -Wall -Wextra -Werror`
* **OS:** Ubuntu / Linux (42 environment)
* **Editor:** VSCode + Vim
* **Testing:** Francinette, Valgrind, custom scripts

---

## 💡 Key Takeaways

* Deep understanding of **pointers** and **memory layout**
* Writing **modular, defensive, leak-free** code
* Applying **algorithmic thinking** to low-level operations
* Understanding **how libc works under the hood**

---

## 🏁 Project Status

✅ Completed and validated
📍 Part of the **Common Core** at **42 Belgium Network**
🔗 [My GitHub Profile](https://github.com/nabil4416)
---

> 🧠 “To master C is to master memory. Everything else is just syntax.”


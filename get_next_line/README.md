# 📄 get_next_line

*A minimal line-by-line reader written in C for the 42 curriculum.*

---

## 🌍 Overview

`get_next_line` is designed to read **one line at a time** from a file descriptor, no matter the line length.
It teaches key low-level concepts:

* File descriptors & `read()`
* Buffer-based reading
* Memory allocation & leak prevention
* Persistent state using a **static stash**

---

# ⚙️ How the Function Works (Short Version)

1. A **static stash** keeps leftover data between calls.
2. `read_file()` reads data in chunks (`BUFFER_SIZE`) and appends it to the stash.
3. When a newline appears, `extract_line()` returns the first full line.
4. `update_stash()` removes the returned line from the stash.
5. Function repeats until EOF.

Simple loop:

```
read_file → detect newline → extract_line → update_stash → return line
```

---

# 🧩 Breakdown of Each Function

### 🔒 `stash` (static)

Stores data between calls.
Survives across function calls → essential for multi-line reading.

---

### 📥 `read_file(int fd, char *stash)`

* Allocates a temporary buffer
* Reads until a newline appears or EOF
* Appends new data to stash
* Frees buffer before returning

Common traps fixed:

* handling `s1 == NULL` in `ft_strjoin`
* freeing `buf` on `read()` error
* preventing infinite loops on `bytes_read <= 0`

---

### 📝 `extract_line(char *stash)`

* Returns the **first full line**, including `'\n'` if present
* Stops when reaching newline
* Allocates memory only for that line

Why include the newline?
→ The project requires reproducing the exact line format.

---

### 🔄 `update_stash(char *stash)`

* Removes the extracted line from stash
* Allocates a new stash containing only the remainder
* Frees the old stash
* Returns NULL when nothing is left

---

### 🎯 `get_next_line(int fd)`

The orchestrator.
Validates input → reads → extracts → updates → returns the line.

---

# 🧯 Memory Issues I Fixed

| Problem                        | Fix                                                 |
| ------------------------------ | --------------------------------------------------- |
| Lost stash during `ft_strjoin` | safe handling of NULL + freeing old stash correctly |
| `read()` error leaking `buf`   | free before returning                               |
| Infinite loop at EOF           | check `bytes_read <= 0`                             |
| Last line not freed            | handled in `update_stash`                           |

---

# 🧪 Testing

### Compile

```bash
cc -Wall -Wextra -Werror get_next_line.c get_next_line_utils.c main.c -D BUFFER_SIZE=42
```

### Test with a main

```c
while ((line = get_next_line(fd))) {
    printf("%s", line);
    free(line);
}
```

### Tools I used

* **Valgrind** (leaks, invalid reads)
* **gnlTester** (mandatory/edge cases)
* Custom test mains

---

# ⚠️ Common Pitfalls

* Forgetting `buf[bytes_read] = '\0'`
* Joining without checking `malloc` failures
* Returning `""` instead of `NULL` at EOF
* Not freeing stash at the right time
* Mismanaging `BUFFER_SIZE = 1`

---

# 📚 Useful Resources

* `man open`, `man read`, `man malloc`
* [https://harm-smits.github.io/42docs/projects/get_next_line](https://harm-smits.github.io/42docs/projects/get_next_line)
* [https://cr0w.gitbook.io/j0xhn/42-school/get-next-line](https://cr0w.gitbook.io/j0xhn/42-school/get-next-line)
* `valgrind --leak-check=full`

---

# 🤝 Final Words

If you’re starting this project:
focus on **memory flow**, understand **file descriptors**, and keep your stash logic clean.
Once this clicks, the rest of the C modules will feel much easier.

Happy coding! 🚀

---

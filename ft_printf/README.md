# 🔢 ft_printf — Custom printf Implementation

> **42 Project — Rebuilding a simplified version of `printf` using variadic functions and low-level writing.**

## 📌 Project Goal

Reproduce the core behavior of the standard `printf` function, using only:

* `write`
* `malloc` / `free`
* `va_start`, `va_arg`, `va_copy`, `va_end`

This project teaches how to parse formatted strings, handle multiple data types, and manage memory safely while working with variadic arguments.

---

## 🚀 Supported Conversions

My `ft_printf()` currently handles:

| Conversion  | Description                      |
| ----------- | -------------------------------- |
| `%c`        | Print a character                |
| `%s`        | Print a string                   |
| `%d` / `%i` | Signed decimal integer           |
| `%x`        | Lowercase hexadecimal (unsigned) |
| `%%`        | Print a literal `%`              |

Each conversion returns the **number of characters printed**, or `-1` on write error.

---

## 🧠 Project Structure

```
ft_printf/
├── ft_printf.c
├── dispatch.c
├── handle_token.c
├── ft_putchar.c
├── ft_putstr.c
├── ft_putnbr_dec.c
├── ft_putnbr_hex.c
├── ft_utils.c
├── ft_printf.h
└── Makefile
```

### 🔍 How it Works

* `ft_printf()` iterates over the format string.
* When it encounters `%`, it calls `handle_token()`.
* `handle_token()` reads the next character and calls `dispatch()`.
* `dispatch()` redirects to the correct printing function.
* Each printing function returns how many characters it wrote.

---

## 🧪 Example Usage

```c
#include "ft_printf.h"

int main(void)
{
    ft_printf("Hello %s!\n", "Isaac");
    ft_printf("Decimal: %d\n", 42);
    ft_printf("Hex: %x\n", 255);
    ft_printf("Char: %c\n", 'A');
    ft_printf("Percent: %%\n");
    return 0;
}
```

---

## 📦 Build Instructions

### Build the library:

```bash
make
```

### Clean object files:

```bash
make clean
```

### Remove all build artifacts:

```bash
make fclean
```

### Rebuild from scratch:

```bash
make re
```

---

## 🛠️ Technical Notes

* Full error handling for `write()`
* No forbidden functions (`printf`, `itoa`, etc.)
* Decimal and hexadecimal conversions implemented manually
* Correct use of `va_list` for variadic argument parsing
* Code fully Norminette-compliant

This project strengthened my understanding of:

* pointers and memory flow
* parsing algorithms
* low-level output
* safe and clean C programming practices

---

## 📚 References

* `man 3 printf`
* `man 2 write`
* Variadic functions documentation (`va_list`)
* 42 subject PDF & Norminette rules

---

## 👤 Author

**Isaac Nabil**
42 Belgium Student | Front-end dev → Software Engineer
📍 Belgium
🔗 GitHub: [https://github.com/nabil4416](https://github.com/nabil4416)


# Resources
https://www.cprogramming.com/tutorial/printf-format-strings.html <br />
https://blog.aaronballman.com/2012/06/how-variable-argument-lists-work-in-c/ <br />
https://stackoverflow.com/questions/38023473/include-first-argument-in-va-list-object <br />
https://wiki.sei.cmu.edu/confluence/display/c/EXP47-C.+Do+not+call+va_arg+with+an+argument+of+the+incorrect+type <br />
https://newbedev.com/char-type-in-va-arg <br />
http://underpop.online.fr/j/java/help/using-flags-in-the-printf-format-string-formatted-output.html.gz <br />
https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/va-arg-va-copy-va-end-va-start?view=msvc-170 <br />
https://velog.io/@ljiwoo59/ftprintf <br />
https://www.lix.polytechnique.fr/~liberti/public/computing/prog/c/C/FUNCTIONS/format.html

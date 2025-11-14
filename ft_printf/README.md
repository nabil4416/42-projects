## 1️⃣ README.md (advanced + concise)

````markdown
# ft_printf

![Language](https://img.shields.io/badge/language-C-blue)
![42 Project](https://img.shields.io/badge/42-Project-000000?logo=42&logoColor=white)
![Repo stars](https://img.shields.io/github/stars/nabil4416/ft_printf?style=flat-square)
![Build](https://img.shields.io/github/actions/workflow/status/nabil4416/ft_printf/ci.yml?branch=main&label=build)

<p align="center">
  <img src="assets/ft_printf-logo.svg" alt="ft_printf logo" width="220">
</p>

---

## 📌 Overview

`ft_printf` is a custom implementation of the standard C `printf` function, written as part of the **42** curriculum.

The goal is to:

- Parse a **format string**
- Handle a subset of **format specifiers**
- Use **variadic functions** (`va_list`)
- Write output using **low-level I/O** (`write`)
- Return the **number of characters printed**, like the real `printf`.

This project is a key step to understanding:
- how formatted output works internally,
- how to manage memory and buffers safely,
- how to design small, reusable printing utilities.

---

## ✅ Supported Conversions

`ft_printf()` currently handles:

| Specifier | Description                    |
|----------|---------------------------------|
| `%c`     | Single character                |
| `%s`     | String                          |
| `%d`     | Signed decimal integer          |
| `%i`     | Signed decimal integer (alias)  |
| `%x`     | Unsigned hexadecimal (lowercase)|
| `%%`     | Literal percent sign `%`        |

Each call returns the **total number of characters written**, or `-1` on error (e.g. `write()` failure).

---

## 🧠 Design & Architecture

Typical file layout:

```text
ft_printf/
├── ft_printf.c        # Main ft_printf entry point
├── handle_token.c     # Parsing of '%' tokens
├── dispatch.c         # Dispatch table for conversions
├── ft_putchar.c       # Low-level char output
├── ft_putstr.c        # String output
├── ft_putnbr_dec.c    # Decimal integer output
├── ft_putnbr_hex.c    # Hexadecimal output
├── ft_utils.c         # Helpers (length, checks, etc.)
├── ft_printf.h        # Prototypes and includes
└── Makefile
````

### Flow

1. `ft_printf()` walks through the format string.
2. Regular characters are written directly with `write()`.
3. On `'%'`, it calls `handle_token()`:

   * validates the next character,
   * forwards control to `dispatch()`.
4. `dispatch()` selects the appropriate function based on the specifier:

   * `%c` → `ft_putchar`
   * `%s` → `ft_putstr`
   * `%d`/`%i` → `ft_putnbr_dec`
   * `%x` → `ft_putnbr_hex`
5. Each helper returns how many characters it wrote.
6. `ft_printf()` accumulates this count and returns it.

Error handling is propagated: if a write fails, the functions return `-1` and the error bubbles up.

---

## 🧪 Example Usage

```c
#include "ft_printf.h"

int main(void)
{
    ft_printf("Hello %s!\n", "World");
    ft_printf("Decimal: %d | Hex: %x\n", 42, 42);
    ft_printf("Char: %c | Percent: %%\n", 'A');
    ft_printf("Negative: %d\n", -12345);
    return 0;
}
```

---

## 🛠 Build

Build the static library:

```bash
make
```

Clean object files:

```bash
make clean
```

Remove all build artifacts:

```bash
make fclean
```

Rebuild from scratch:

```bash
make re
```

You can link the library with a test file:

```bash
cc main.c libftprintf.a -o test_ftprintf
./test_ftprintf
```

*(Adapt the library filename if your Makefile uses a different name.)*

---

## 🧪 Testing vs. stdio printf

A simple test driver is provided in `main.c` (see below in this repo).
It compares `ft_printf` output and return values with the standard `printf` for:

* basic strings and characters
* positive and negative integers
* edge cases (`INT_MIN`, `INT_MAX`)
* hexadecimal values
* mixed format strings

---

## 📚 References

* `man 3 printf`
* `man 2 write`
* C standard library documentation
* 42 subject PDF & Norm rules

---

## 👤 Author

**Isaac Nabil**
42 Belgium — ft_printf project
🔗 GitHub: [nabil4416](https://github.com/nabil4416)

````

> 🔧 Note: the **build badge** assumes you’ll later add a GitHub Actions workflow called `ci.yml` in `.github/workflows/`. Until then, the badge may show “no status” — that’s normal.

---

## 2️⃣ Logo file — `assets/ft_printf-logo.svg`

Crée un dossier `assets/` à la racine du repo, puis ajoute ce fichier sous le nom `ft_printf-logo.svg` :

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg width="420" height="120" viewBox="0 0 420 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E3A8A"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>
    <style>
      .bg { fill: #0F172A; }
      .badge { fill: url(#grad); }
      .title { fill: #E5E7EB; font-family: "Fira Code", monospace; font-size: 34px; font-weight: 600; }
      .subtitle { fill: #9CA3AF; font-family: "Fira Code", monospace; font-size: 14px; }
      .mono { fill: #FACC15; font-family: "Fira Code", monospace; font-size: 16px; }
    </style>
  </defs>

  <!-- Background -->
  <rect class="bg" x="0" y="0" width="420" height="120" rx="18" />

  <!-- Gradient badge -->
  <rect class="badge" x="20" y="24" width="70" height="70" rx="16" />

  <!-- Curly brace / percent combo -->
  <text x="40" y="67" class="mono">{</text>
  <text x="55" y="90" class="mono">%</text>

  <!-- Title -->
  <text x="120" y="53" class="title">ft_printf</text>

  <!-- Subtitle -->
  <text x="120" y="78" class="subtitle">minimal printf • variadic C • 42 project</text>
</svg>
````

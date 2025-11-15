## 🧩 README.md

````markdown
# 📜 get_next_line

Projet de l'école **42** — Lire un fichier ligne par ligne, de manière efficace, sans fuite mémoire et sans dépendance à la libc (autre que `read`, `malloc` et `free`).

---

## 🧠 Objectif

L’objectif de `get_next_line` est d’implémenter une fonction qui retourne **une ligne lue depuis un descripteur de fichier** à chaque appel.  
Elle doit fonctionner indépendamment du **BUFFER_SIZE**, gérer les **EOF propres**, et éviter toute **fuite mémoire**.

---

## ⚙️ Prototype

```c
char *get_next_line(int fd);
````

* `fd` : le descripteur de fichier à lire (`open()` doit avoir été appelé avant)
* Retour :

  * La **ligne suivante** lue depuis le fichier, incluant le `\n` si présent
  * `NULL` quand il n’y a plus rien à lire (ou en cas d’erreur)

---

## 🧩 Exemple d’utilisation

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int fd = open("test.txt", O_RDONLY);
    char *line;

    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

---

## 🧱 Structure du projet

```
get_next_line/
│
├── get_next_line.c        # Fonction principale + logique de lecture
├── get_next_line_utils.c  # Fonctions utilitaires (ft_strlen, ft_strjoin, etc.)
├── get_next_line.h        # Prototypes et définition du BUFFER_SIZE
└── main.c                 # Programme de test
```

---

## ⚡ Compilation

```bash
cc -Wall -Wextra -Werror get_next_line.c get_next_line_utils.c main.c -D BUFFER_SIZE=42
```

Tu peux modifier la taille du buffer au moment de la compilation :

```bash
cc ... -D BUFFER_SIZE=10
```

---

## 📄 Fichiers de test recommandés

Pour tester différents cas :

* `test.txt` : lignes normales
* `test_multilines.txt` : plusieurs petites lignes
* `test_empty.txt` : fichier vide
* `test_weird.txt` : lignes vides, fins sans `\n`, etc.

Exécution :

```bash
./a.out test.txt
```

---

## 🧪 Tests automatiques

Tu peux tester la robustesse et les fuites mémoire avec :

```bash
valgrind --leak-check=full ./a.out test.txt
```

---

## 🧠 Points clés du projet

* Gestion dynamique de la mémoire
* Lecture par morceaux via `read()`
* Concaténation et découpe des chaînes (`ft_strjoin`, `ft_strchr`, …)
* Conservation de la “suite” entre appels grâce à une variable **statique**
* Bonne gestion des EOF et des fichiers sans retour à la ligne final

---

## 🏆 Bonus (optionnel)

* Support **multi-file descriptor** (un stash par `fd`)
* Gestion efficace de très grands fichiers
* Tests avec différents `BUFFER_SIZE` pour prouver la robustesse

--

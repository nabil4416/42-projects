#include "libft.h"
#include <stdio.h>
#include <string.h>   // strcpy, memset, etc.
#include <strings.h>  // bzero (selon les systèmes)


/*to use this test, 1 make, 2 gcc main.c libft.a -I. -o test
then write : ./test*/


// Callback pour ft_strmapi
static char add_index(unsigned int i, char c)
{
    return (c + i);
}

void    test_memory(void)
{
    char buf1[20], buf2[20];

    printf("\n=== MEMORY ===\n");

    // memset
    ft_memset(buf1, 'A', 5);
    memset(buf2, 'A', 5);
    printf("ft_memset  : %.*s\n", 5, buf1);
    printf("memset     : %.*s\n", 5, buf2);

    // bzero
    ft_bzero(buf1, 3);
    bzero(buf2, 3);
    printf("ft_bzero   : [%d][%d][%d]\n", buf1[0], buf1[1], buf1[2]);
    printf("bzero      : [%d][%d][%d]\n", buf2[0], buf2[1], buf2[2]);

    // memcpy
    strcpy(buf1, "123456789");
    strcpy(buf2, "123456789");
    ft_memcpy(buf1, "ABC", 3);
    memcpy(buf2, "ABC", 3);
    printf("ft_memcpy  : %s\n", buf1);
    printf("memcpy     : %s\n", buf2);

    // memmove (test overlap)
    strcpy(buf1, "HELLOWORLD");
    strcpy(buf2, "HELLOWORLD");
    ft_memmove(buf1 + 2, buf1, 5);
    memmove(buf2 + 2, buf2, 5);
    printf("ft_memmove : %s\n", buf1);
    printf("memmove    : %s\n", buf2);
}

void    test_string(void)
{
    printf("\n=== STRING ===\n");

    printf("ft_strlen(\"Hello\") = %zu\n", ft_strlen("Hello"));
    printf("ft_strchr(\"Hello\", 'l') = %s\n", ft_strchr("Hello", 'l'));
    printf("ft_strrchr(\"Hello\", 'l') = %s\n", ft_strrchr("Hello", 'l'));
    printf("ft_strncmp(\"abc\", \"abd\", 2) = %d\n", ft_strncmp("abc", "abd", 2));

    char dst[10];
    printf("ft_strlcpy = %zu\n", ft_strlcpy(dst, "abcdef", sizeof(dst)));
    printf("result = %s\n", dst);

    char *dup = ft_strdup("42");
    printf("ft_strdup = %s\n", dup);
    free(dup);

    printf("ft_strnstr = %s\n", ft_strnstr("HelloWorld", "World", 10));

    char *sub = ft_substr("Hello42World", 5, 2);
    printf("ft_substr(\"Hello42World\", 5, 2) = %s\n", sub);
    free(sub);

    char *join = ft_strjoin("Hello", "42");
    printf("ft_strjoin = %s\n", join);
    free(join);

    char *trim = ft_strtrim("--Hello--", "-");
    printf("ft_strtrim(\"--Hello--\", \"-\") = %s\n", trim);
    free(trim);

    char **tab = ft_split("  Hello  42  Student  ", ' ');
    printf("ft_split:\n");
    if (tab)
    {
        for (int i = 0; tab[i]; i++)
            printf("  [%s]\n", tab[i]);
        for (int i = 0; tab[i]; i++)
            free(tab[i]);
        free(tab);
    }

    char *mapped = ft_strmapi("abc", add_index);
    printf("ft_strmapi(\"abc\", add_index) = %s\n", mapped);
    free(mapped);
}

void    test_convert(void)
{
    char *itoa_res;

    printf("\n=== CONVERT ===\n");

    printf("ft_atoi(\"42\") = %d\n", ft_atoi("42"));
    printf("ft_atoi(\"   -123\") = %d\n", ft_atoi("   -123"));
    itoa_res = ft_itoa(123);
    printf("ft_itoa(123) = %s\n", itoa_res);
    free(itoa_res);
}

void    test_ctype(void)
{
    printf("\n=== CTYPE ===\n");

    printf("ft_isalpha('A') = %d\n", ft_isalpha('A'));
    printf("ft_isdigit('9') = %d\n", ft_isdigit('9'));
    printf("ft_isalnum('@') = %d\n", ft_isalnum('@'));
    printf("ft_isascii(200) = %d\n", ft_isascii(200));
    printf("ft_isprint(32)  = %d\n", ft_isprint(32));
    printf("ft_toupper('a') = %d\n", ft_toupper('a'));
    printf("ft_tolower('Z') = %d\n", ft_tolower('Z'));
}

void    test_io(void)
{
    printf("\n=== IO ===\n");
    printf("ft_putchar_fd('A', 1) → ");
    ft_putchar_fd('A', 1);
    printf("\n");

    printf("ft_putstr_fd(\"Hello\", 1) → ");
    ft_putstr_fd("Hello", 1);
    printf("\n");

    printf("ft_putendl_fd(\"World\", 1) → ");
    ft_putendl_fd("World", 1);

    printf("ft_putnbr_fd(12345, 1) → ");
    ft_putnbr_fd(12345, 1);
    printf("\n");
}

int main(void)
{
    test_memory();
    test_string();
    test_convert();
    test_ctype();
    test_io();
    return 0;
}


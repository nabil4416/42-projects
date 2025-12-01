#include <stdio.h>
#include <stdlib.h>
#include "get_next_line.h"

//premier test: Pass an arbitrary file descriptor … on which it is not possible to read, for example 42. The function must return NULL.

int main(void)
{
    char *line;

    line = get_next_line(42);
    if (!line)
        printf("line is NULL\n");
    else
    {
        printf("line = [%s]\n", line);
        free(line);
    }
    return (0);
}

/*int main(void)
{
    char *line;

    while ((line = get_next_line(0)) != NULL)  // 0 = stdin
    {
        printf("%s", line);
        free(line);
    }
    return (0);
}*/


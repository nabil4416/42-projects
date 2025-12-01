#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include "get_next_line.h"

//premier test: Pass an arbitrary file descriptor … on which it is not possible to read, for example 42. The function must return NULL.
printf("=====First Test====");
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

//deuxieme test:
printf("=====Second Test====");
int main(int argc, char **argv)
{
    int   fd;
    char *line;
    int   i = 0;

    if (argc != 2)
    {
        printf("Usage: %s <file>\n", argv[0]);
        return (1);
    }
    fd = open(argv[1], O_RDONLY);
    if (fd < 0)
    {
        perror("open");
        return (1);
    }
    while ((line = get_next_line(fd)) != NULL)
    {
        printf("LINE %d: [%s]\n", i++, line);
        free(line);
    }
    close(fd);
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


#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include "get_next_line.h"

/*
** Petite fonction utilitaire pour tester un fd
*/
static void test_fd(const char *label, int fd)
{
	char *line;
	int   i = 1;

	printf("\n===== Test: %s =====\n", label);
	if (fd < 0)
	{
		perror("open");
		return;
	}
	while ((line = get_next_line(fd)) != NULL)
	{
		printf("[%s] line %d: %s", label, i, line);
		if (line[0] != '\0' && line[ft_strlen(line) - 1] != '\n')
			printf(" <-- (no \\n at end)\n");
		else
			printf("\n");
		free(line);
		i++;
	}
	close(fd);
}

/*
** Test interleaving (bonus) : lire sur 2 fd en alternance
*/
static void test_two_fds(const char *file1, const char *file2)
{
	int   fd1 = open(file1, O_RDONLY);
	int   fd2 = open(file2, O_RDONLY);
	char *l1;
	char *l2;
	int   i = 1;

	printf("\n===== Test multi-FD (bonus) =====\n");
	if (fd1 < 0 || fd2 < 0)
	{
		perror("open");
		if (fd1 >= 0)
			close(fd1);
		if (fd2 >= 0)
			close(fd2);
		return;
	}
	while (1)
	{
		l1 = get_next_line(fd1);
		l2 = get_next_line(fd2);
		if (!l1 && !l2)
			break;
		printf("[multi] round %d\n", i++);
		if (l1)
		{
			printf(" fd1: %s", l1);
			free(l1);
		}
		else
			printf(" fd1: (NULL)\n");
		if (l2)
		{
			printf(" fd2: %s", l2);
			free(l2);
		}
		else
			printf(" fd2: (NULL)\n");
	}
	close(fd1);
	close(fd2);
}

int	main(void)
{
	/* à adapter à tes fichiers de test */
	test_fd("fichier normal", open("normal.txt", O_RDONLY));
	test_fd("fichier vide", open("empty.txt", O_RDONLY));
	test_fd("ligne sans \\n final", open("no_newline.txt", O_RDONLY));
	test_fd("ligne très longue", open("long_line.txt", O_RDONLY));

	/* test FD invalide */
	printf("\n===== Test: fd invalide =====\n");
	char *line = get_next_line(-1);
	if (!line)
		printf("get_next_line(-1) -> NULL ✅\n");
	else
	{
		printf("get_next_line(-1) -> \"%s\" ❌ (devrait être NULL)\n", line);
		free(line);
	}

	/* test BUFFER_SIZE petit (compile avec -D BUFFER_SIZE=1 par ex.) */

	/* test multi-fd (bonus) si tu as implémenté stash par fd */
	test_two_fds("normal.txt", "long_line.txt");

	return (0);
}


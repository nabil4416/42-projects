#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>     // pour strlen
#include "get_next_line.h"

/*
 * Affiche proprement une ligne :
 * - on ajoute un \n si la ligne n'en contient pas à la fin
 *   (pour mieux voir ce qui se passe dans le terminal).
 */
static void print_line(const char *label, int index, const char *line)
{
	size_t	len;

	printf("[%s] line %d: ", label, index);
	if (!line)
	{
		printf("(NULL)\n");
		return;
	}
	printf("%s", line);
	len = strlen(line);
	if (len == 0 || line[len - 1] != '\n')
		printf("\\n manquant (ajouté par main)\n");
}

/*
 * Teste un fichier donné :
 * - ouverture
 * - lecture ligne par ligne avec get_next_line
 * - vérifie qu'après EOF, un appel supplémentaire renvoie encore NULL
 */
static void	test_file(const char *label, const char *path)
{
	int		fd;
	char	*line;
	char	*extra_line;
	int		i;

	printf("\n===== Test fichier: %s (%s) =====\n", label, path);
	fd = open(path, O_RDONLY);
	if (fd < 0)
	{
		perror("open");
		return;
	}
	i = 1;
	while ((line = get_next_line(fd)) != NULL)
	{
		print_line(label, i, line);
		free(line);
		i++;
	}
	printf("Fin de fichier atteinte (get_next_line -> NULL)\n");

	/* appel supplémentaire après EOF : doit aussi renvoyer NULL sans fuite */
	extra_line = get_next_line(fd);
	if (extra_line != NULL)
	{
		printf("⚠️  Problème: get_next_line renvoie encore quelque chose après EOF !\n");
		print_line(label, i, extra_line);
		free(extra_line);
	}
	else
		printf("✅ Appel supplémentaire après EOF -> NULL (OK)\n");

	close(fd);
}

/*
 * Teste un fd invalide : get_next_line(-1) doit renvoyer NULL
 * sans crash, sans fuite.
 */
static void	test_invalid_fd(void)
{
	char	*line;

	printf("\n===== Test fd invalide (-1) =====\n");
	line = get_next_line(-1);
	if (line == NULL)
		printf("✅ get_next_line(-1) -> NULL (OK)\n");
	else
	{
		printf("⚠️  Problème: get_next_line(-1) renvoie une chaîne: \"%s\"\n", line);
		free(line);
	}
}

int	main(void)
{
	/* À TOI de créer ces fichiers dans ton dossier : */
	test_file("fichier normal", "normal.txt");
	test_file("fichier vide", "empty.txt");
	test_file("sans newline final", "no_newline.txt");
	test_file("ligne très longue", "long_line.txt");

	test_invalid_fd();

	return (0);
}


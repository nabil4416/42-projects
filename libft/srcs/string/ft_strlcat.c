/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/20 15:38:02 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 13:24:27 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

size_t	ft_strlcat(char *dest, const char *src, size_t size)
{
	size_t	dest_len;
	size_t	str_len;
	size_t	i;

	dest_len = 0;
	while (dest_len < size && dest[dest_len])
		dest_len++;
	str_len = ft_strlen(src);
	if (dest_len == size)
		return (size + str_len);
	i = 0;
	while (src[i] && (dest_len + 1 + i) < size)
	{
		dest[dest_len + i] = src[i];
		i++;
	}
	dest[dest_len + i] = '\0';
	return (dest_len + str_len);
}

/*#include <stdio.h>

int	main(void)
{
	char dest[10] = "HI";
	char src[] = " there!";
	size_t size = 10;

	size_t result = ft_strlcat(dest, src, size);

	printf("Resultat: \"%s\"\n", dest);
	printf("Valeur retournee: %zu\n", result);
	printf("taille du buffer (size) = %zu\n", size);
	return 0;
}*/

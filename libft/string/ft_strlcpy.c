/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 16:38:53 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/30 15:33:19 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcpy(char *dest, const char *src, size_t destsize)
{
	size_t	i;
	size_t	src_len;

	if (!dest || !src)
		return (0);
	src_len = 0;
	while (src[src_len])
		src_len++;
	if (destsize == 0)
		return (src_len);
	i = 0;
	while (src[i] && i < destsize - 1)
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (src_len);
}

/*#include <stdio.h>

int	main(void)
{
	char	src[] = "hello, world";
	char	dest[6];

	size_t	result = ft_strlcpy(dest, src, sizeof(dest));
	printf("dest: %s\n", dest);
	printf("longueur de la src: %zu\n", result);
	return 0;
}*/

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 15:26:21 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 17:31:01 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	unsigned char	*str;
	unsigned char	letr;
	size_t			i;

	str = (unsigned char *)s;
	letr = (unsigned char)c;
	i = 0;
	while (i < n)
	{
		if (str[i] == letr)
			return ((void *) &str[i]);
		i++;
	}
	return (NULL);
}

/*#include <stdio.h>

int	main(void)
{
	char	txt[] = "Harvey";
	char	*result = ft_memchr(txt, 'v', 5);
	if (result != NULL)
		printf("found: %c\n", *result);
	else
		printf("not found\n");
	return 0;
}*/

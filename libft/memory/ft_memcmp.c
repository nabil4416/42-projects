/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 17:15:06 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/29 09:32:28 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	unsigned char	*str1;
	unsigned char	*str2;
	size_t			i;

	str1 = (unsigned char *)s1;
	str2 = (unsigned char *)s2;
	i = 0;
	while (i < n)
	{
		if (str1[i] != str2[i])
			return (str1[i] - str2[i]);
		i++;
	}
	return (0);
}

/*#include <stdio.h>

int	main(void)
{
	char txt1[] = "Harvey";
	char txt2[] = "HarVey";

	printf("compare6 txt1, txt2: %d\n", ft_memcmp(txt1, txt2, 6));
	printf("compare4 txt1, txt2: %d\n", ft_memcmp(txt1, txt2, 4));
	printf("compare2 txt1, txt2: %d\n", ft_memcmp(txt1, txt2, 3));
	return 0;
}*/

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 14:21:22 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 17:39:34 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	size_t	i;

	i = 0;
	while ((s1[i] || s2[i]) && i < n)
	{
		if ((unsigned char) s1[i] != (unsigned char) s2[i])
			return ((unsigned char) s1[i] - (unsigned char) s2[i]);
		i++;
	}
	return (0);
}

/*#include <stdio.h>
int	main(void)
{
	printf("1/abc et abc: %d\n", ft_strncmp("abc", "abc", 3));
	printf("2/abc et abd: %d\n", ft_strncmp("abc", "abd", 3));
	printf("3/abd et abc: %d\n", ft_strncmp("abd", "abc", 3));
	printf("4/abc et abcde: %d\n", ft_strncmp("abc", "abcde", 3));
	printf("5/abc et abcde: %d\n", ft_strncmp("abc", "abcde", 5));
	printf("6/abcd et abcz: %d\n", ft_strncmp("abcd", "abcz", 4));
	printf("7/abcd et abcz: %d\n", ft_strncmp("abcd", "abcz", 0));
 	return 0;
}*/

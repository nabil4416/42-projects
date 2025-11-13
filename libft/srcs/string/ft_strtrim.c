/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/25 14:07:11 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 15:45:51 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	is_in_set(char c, const char *set)
{
	size_t	i;

	i = 0;
	while (set[i])
	{
		if (set[i] == c)
			return (1);
		i++;
	}
	return (0);
}

char	*ft_strtrim(const char *s1, const char *set)
{
	size_t	start;
	size_t	end;

	if (!s1 || !set)
		return (NULL);
	start = 0;
	while (s1[start] && is_in_set(s1[start], set))
		start++;
	end = ft_strlen(s1);
	while (end > start && is_in_set(s1[end -1], set))
		end--;
	return (ft_substr(s1, start, end - start));
}

/*#include <stdio.h>

int	main(void)
{
	printf("1.+++Ambition 10+++ => +: %s\n", 
			ft_strtrim("+++Ambition 10+++", "+ "));
	printf("2.abcAmbition 10abc => abc: %s\n", 
			ft_strtrim("abcAmbition 10abc", "abc"));
	printf("3.Ambition => \" \": %s\n", ft_strtrim("Ambition", " "));
	printf("4.---------- => -: %s\n", ft_strtrim("----------", "-"));
	printf("5.\"\"=> abc: %s\n", ft_strtrim("", "abc"));
	printf("6.   Ambition   =>\" \" %s\n", ft_strtrim("   Ambition   ", " "));
	return 0;
}*/

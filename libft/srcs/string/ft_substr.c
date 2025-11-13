/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/25 12:23:31 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/25 12:55:27 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(const char *s, unsigned int start, size_t len)
{
	char	*sub;
	size_t	i;

	if (!s)
		return (NULL);
	if (start >= ft_strlen(s))
		return (ft_strdup(""));
	if (len > ft_strlen(s + start))
		len = ft_strlen(s + start);
	sub = malloc((len + 1) * sizeof(char));
	if (!sub)
		return (NULL);
	i = 0;
	while (i < len)
	{
		sub[i] = s[start + i];
		i++;
	}
	sub[i] = '\0';
	return (sub);
}
/*#include <stdio.h>
int	main(void)
{
	char txt1[] = "Ambition & consistency";
	char *subtxt1;
	subtxt1 = ft_substr(txt1, 11, 11);
	printf("subtxt1: %s\n", subtxt1);
	subtxt1 = ft_substr(txt1, 8, 14);
	printf("subtxt1: %s\n", subtxt1);
	subtxt1 = ft_substr(txt1, 24, 14);
        printf("subtxt1: %s\n", subtxt1);
	return 0;
}*/

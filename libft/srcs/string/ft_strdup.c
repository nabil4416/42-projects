/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/25 11:26:03 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/25 12:15:18 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s1)
{
	size_t	len_s;
	char	*new;
	size_t	i;

	len_s = ft_strlen(s1);
	new = malloc(len_s + 1);
	if (!new)
		return (NULL);
	i = 0;
	while (i < len_s)
	{
		new[i] = s1[i];
		i++;
	}
	new[i] = '\0';
	return (new);
}
/*#include <stdio.h>

int	main(void)
{
	char txt1[] = "Ambition & consistency";
	char *new;
	new = ft_strdup(txt1);
	if (new)
		printf("new: %s\n", new);
	else
		return (1);
	free(new);
}*/

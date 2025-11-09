/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 12:45:14 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 15:54:43 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr( const char *s, int c)
{
	char	letr;
	int	i;

	letr = (char)c;
	i = 0;
	while (s[i])
		i++;
	while (i >= 0)
	{
		if (s[i] == letr)
			return ((char *) &s[i]);
		i--;
	}
	return (NULL);
}
/*#include <stdio.h>

int	main(void)
{
	char	*txt = "Ambition, consistency, succes";
	char *last_comma = ft_strrchr(txt, ',');
	printf("After lasat comma: %s\n", last_comma);
	char *last_z = ft_strrchr(txt, 'z');
	if (last_z == NULL)
		printf("not found\n");
	return 0;
}*/

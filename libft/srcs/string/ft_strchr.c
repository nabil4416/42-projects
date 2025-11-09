/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/21 11:20:45 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/29 09:53:31 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *s, int c)
{
	unsigned int	i;
	char			letr;

	letr = (char)c;
	i = 0;
	while (s[i])
	{
		if (s[i] == letr)
			return ((char *) &s[i]);
		i++;
	}
	if (letr == '\0')
		return ((char *) &s[i]);
	return (NULL);
}

/*#include <stdio.h>

int	main(void)
{
	char txt[] = "Ambition";
	char *first_i = ft_strchr(txt, 'i');
	printf("la position de i found: %s\n", first_i);
	char *first_z = ft_strchr(txt, 'z');
	if (first_z == NULL)
		printf("No 'z' found!\n");
	return 0;
}*/

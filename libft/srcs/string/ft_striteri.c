/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 12:25:33 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/27 12:52:28 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	unsigned int	i;

	if (!s || !f)
		return ;
	i = 0;
	while (s[i] != '\0')
	{
		f(i, &s[i]);
		i++;
	}
}

/*#include <stdio.h>
#include <ctype.h>
void	to_upper(unsigned int i, char *c)
{
	(void)i;
	if (*c >= 'a' && *c <= 'z')
		*c = *c - 'a' + 'A';
}

int	main(void)
{
	char a1[] = "salut 42!";
	printf("=== Test 1: to_upper ===\n");
	printf("Avant: %s\n", a1);
	ft_striteri(a1, to_upper);
	printf("Après: %s\n\n", a1);
	return 0;
}*/

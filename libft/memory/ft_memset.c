/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 10:15:01 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/29 09:55:44 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *s, int c, size_t n)
{
	size_t			i;
	unsigned char	*tmp_ptr;

	tmp_ptr = (unsigned char *) s;
	i = 0;
	while (i < n)
	{
		tmp_ptr[i] = (unsigned char)c;
		i++;
	}
	return (s);
}

/*#include <stdio.h>

int	main(void)
{
	char str[30] = "Ambition and consistency";
	printf("Avant : %s\n", str);
	ft_memset(str + 9, '&', 3);
	printf("After : %s\n", str);
	return 0;
}*/	

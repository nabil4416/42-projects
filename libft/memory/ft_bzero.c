/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 11:41:43 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 17:38:10 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_bzero(void *s, size_t n)
{
	size_t				i;
	unsigned char		*tmp_ptr;

	tmp_ptr = (unsigned char *)s;
	i = 0;
	while (i < n)
	{
		tmp_ptr[i] = 0;
		i++;
	}
}

/*#include <stdio.h>

int	main(void)
{
	//int	i;
	char txt[30] = "Ambition and consistency";

	printf("before: %s\n", txt);
	ft_bzero(txt, 3);
	printf("after: ");
	printf("%s\n", txt);
	return 0;
}*/

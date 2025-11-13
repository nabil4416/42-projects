/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 16:30:12 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/30 11:30:37 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t count, size_t size)
{
	void	*tmp;
	size_t	total;

	if (count && size && count > SIZE_MAX / size)
		return (NULL);
	total = count * size;
	tmp = malloc(total);
	if (!tmp)
		return (NULL);
	ft_bzero(tmp, total);
	return (tmp);
}
/*#include <stdio.h>

int	main(void)
{
	int	*tableau;
	size_t n = 5;
	size_t s = sizeof(int);
	size_t i = 0;

	tableau = ft_calloc(n, s);
	if (!tableau)
	{
		printf("allocation erreur\n");
		return 1;
	}

	while (i < n)
	{
		printf("%d ", tableau[i]);
		i++;
	}
	printf("\n");
	return 0;
}*/

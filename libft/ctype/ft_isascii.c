/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isascii.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 17:45:27 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/18 18:05:58 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

int	ft_isascii(int c)
{
	if (c >= 0 && c <= 127)
		return (1);
	return (0);
}

/*#include <stdio.h>

int	main(void)
{
	printf("is a ascii: %d\n", ft_isascii('a'));
	printf("is 200 ascii: %d\n", ft_isascii(200));
	printf("is Z ascii: %d\n", ft_isascii('Z'));
	printf("is # ascii: %d\n", ft_isascii('#'));
	return 0;
}*/

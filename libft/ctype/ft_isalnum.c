/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalnum.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/17 18:06:21 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 16:07:26 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isalnum(int c)
{
	if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
		|| (c >= '0' && c <= '9'))
		return (1);
	return (0);
}

/*#include <stdio.h>

int	main(void)
{
	printf("is a alnum: %d\n", ft_isalnum('a'));
	printf("is R alnum: %d\n", ft_isalnum('R'));
	printf("is ! alnum: %d\n", ft_isalnum('!'));
	printf("is & alnum: %d\n", ft_isalnum('&'));
	return 0;
}*/

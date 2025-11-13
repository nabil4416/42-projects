/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isdigit.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/17 17:54:32 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 16:07:47 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isdigit(int c)
{
	if (c >= '0' && c <= '9')
		return (1);
	return (0);
}

/*#include <stdio.h>

int	main(void)
{
	printf("is 3 digit: %d\n", ft_isdigit('3'));
	printf("is a digit: %d\n", ft_isdigit('a'));
	printf("is 8 digit: %d\n", ft_isdigit('8'));
	printf("is @ digit: %d\n", ft_isdigit('@'));
	return 0;
}*/

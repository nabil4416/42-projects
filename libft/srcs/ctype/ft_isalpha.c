/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalpha.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/17 16:25:30 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 16:06:07 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isalpha(int c)
{
	if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
		return (1);
	return (0);
}

/*#include <stdio.h>

int	main(void)
{
	printf("is 'a' alphabet: %d\n", ft_isalpha('a'));
	printf("is 'N' alphabet: %d\n", ft_isalpha('N'));
	printf("is '!' alphabet: %d\n", ft_isalpha('!'));
	printf("is '(' alphabet: %d\n", ft_isalpha('('));
	return 0;
}*/

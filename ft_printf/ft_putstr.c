/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/02 10:40:22 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/08 12:37:48 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putstr(char *str)
{
	int	i;

	if (!str)
		return (write(1, "(null)", 6));
	i = 0;
	while (str[i])
	{
		if (write(1, &str[i], 1) < 0)
			return (-1);
		i++;
	}
	return (i);
}

/*#include <stdio.h>

int	main(void)
{
	int	a;
	int	b;
	a = ft_putstr("hello, world!");
	write(1, "\n",1);
	b = ft_putstr(NULL);
	write(1, "\n", 1);
	printf("retours: %d et %d\n", a, b);
	return 0;
}*/

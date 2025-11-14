/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/02 10:41:23 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/07 10:33:41 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"
#include <stdio.h>
#include <limits.h>

int	main(void)
{
	void	*p = (void *)0x7ffeeabc1234;
	void	*z = NULL;
	int		a;
	int		b;

	ft_printf("===== TESTS FT_PRINTF =====\n");
	a = ft_printf("1: %c %s %p %d %i %u %x %X %%\n",
		'A', "hello", p, -42, 42, 4294967295u, 255, 255);
	ft_printf("ft_printf return = %d\n", a);

	printf("===== TESTS PRINTF ORIGINAL =====\n");
	b = printf("1: %c %s %p %d %i %u %x %X %%\n",
		'A', "hello", p, -42, 42, 4294967295u, 255, 255);
	printf("printf return = %d\n", b);

	ft_printf("===== CAS PARTICULIERS =====\n");
	ft_printf("NULL string  : [%s]\n", (char *)0);
	ft_printf("NULL pointer : [%p]\n", z);
	ft_printf("Zero decimal : [%d]\n", 0);
	ft_printf("Zero unsigned: [%u]\n", 0u);
	ft_printf("Zero hex     : [%x]\n", 0u);

	return (0);
}

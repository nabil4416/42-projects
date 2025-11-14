/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_hex_iter.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/02 10:39:55 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/02 10:40:00 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr_hex_upper_iter(unsigned int n)
{
	const char	*base = "0123456789ABCDEF";
	char		buf[8];
	int			i;
	int			ret;
	int			written;

	if (n == 0)
		return (ft_putchar('0'));
	i = 0;
	while (n != 0)
	{
		buf[i++] = base[n % 16];
		n = n / 16;
	}
	written = 0;
	i--;
	while (i >= 0)
	{
		ret = ft_putchar(buf[i]);
		if (ret < 0)
			return (-1);
		written = written + ret;
		i--;
	}
	return (written);
}

/*#include <stdio.h>
#include <unistd.h>

int     main(void)
{
        int     ret;

        write(1, "Test 2 : ", 9);
        ret = ft_putnbr_hex_upper_iter(255);
        write(1, "\n", 1);
        printf(" -> retour = %d (printf = %d)\n\n", ret, printf("%x", 255));

        return (0);
}*/

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 09:46:56 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/07 09:47:10 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	put_hex_ul(unsigned long n)
{
	const char	base[] = "0123456789abcdef";
	char		buf[sizeof(unsigned long) * 2];
	int			i;
	int			ret;
	int			count;

	if (n == 0)
		return (write(1, "0", 1));
	i = 0;
	while (n != 0)
	{
		buf[i++] = base[n % 16];
		n /= 16;
	}
	count = i;
	while (--i >= 0)
	{
		ret = write(1, &buf[i], 1);
		if (ret < 0)
			return (-1);
	}
	return (count);
}

int	ft_putptr(const void *ptr)
{
	int				w;
	unsigned long	addr;

	if (!ptr)
		return (write(1, "(nil)", 5));
	w = write(1, "0x", 2);
	if (w < 0)
		return (-1);
	addr = (unsigned long)ptr;
	w = put_hex_ul(addr);
	if (w < 0)
		return (-1);
	return (w + 2);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 09:44:34 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/07 09:44:55 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr(int n)
{
	long	nb;
	int		count;
	int		ret;

	nb = n;
	count = 0;
	if (nb < 0)
	{
		if (write(1, "-", 1) < 0)
			return (-1);
		count++;
		nb = -nb;
	}
	if (nb >= 10)
	{
		ret = ft_putnbr(nb / 10);
		if (ret < 0)
			return (-1);
		count += ret;
	}
	if (ft_putchar((nb % 10) + '0') < 0)
		return (-1);
	return (count + 1);
}

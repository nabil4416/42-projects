/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunbr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/07 09:45:49 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/07 09:46:09 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putunbr(unsigned int n)
{
	char	buf[10];
	int		i;
	int		ret;
	int		count;

	if (n == 0)
		return (write(1, "0", 1));
	i = 0;
	while (n != 0)
	{
		buf[i++] = (char)('0' + (n % 10));
		n /= 10;
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

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/02 10:36:11 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/07 17:18:59 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	print_unknown(char k)
{
	int	r;

	r = ft_putchar(k);
	if (r < 0)
		return (-1);
	return (2);
}

static int	dispatch(va_list *ap, char k)
{
	if (k == 'c')
		return (ft_putchar(va_arg(*ap, int)));
	if (k == 's')
		return (ft_putstr(va_arg(*ap, char *)));
	if (k == 'd' || k == 'i')
		return (ft_putnbr(va_arg(*ap, int)));
	if (k == 'u')
		return (ft_putunbr(va_arg(*ap, unsigned int)));
	if (k == 'x')
		return (ft_putnbr_hex_iter(va_arg(*ap, unsigned int)));
	if (k == 'X')
		return (ft_putnbr_hex_upper_iter(va_arg(*ap, unsigned int)));
	if (k == 'p')
		return (ft_putptr(va_arg(*ap, void *)));
	if (k == '%')
		return (ft_putchar('%'));
	if (write(1, "%", 1) < 0)
		return (-1);
	return (print_unknown(k));
}

static int	handle_token(const char **fmt, va_list *ap)
{
	int	r;

	if (**fmt != '%')
	{
		r = write(1, *fmt, 1);
		(*fmt)++;
		return (r);
	}
	if (*(*fmt + 1) == '\0')
		return (-2);
	r = dispatch(ap, *(*fmt + 1));
	(*fmt) += 2;
	return (r);
}

int	ft_printf(const char *fmt, ...)
{
	va_list	ap;
	int		total;
	int		r;

	if (!fmt)
		return (-1);
	va_start(ap, fmt);
	total = 0;
	while (*fmt)
	{
		r = handle_token(&fmt, &ap);
		if (r == -2)
			break ;
		if (r < 0)
		{
			va_end(ap);
			return (-1);
		}
		total += r;
	}
	va_end(ap);
	return (total);
}

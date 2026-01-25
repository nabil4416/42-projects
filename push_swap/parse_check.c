/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_check.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:28:44 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:28:58 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_digit(char c)
{
	return (c >= '0' && c <= '9');
}

static int	parse_sign(char *s, int *i)
{
	int	sign;

	sign = 1;
	if (s[*i] == '+' || s[*i] == '-')
	{
		if (s[*i + 1] == '\0')
			return (0);
		if (s[*i] == '-')
			sign = -1;
		(*i)++;
	}
	return (sign);
}

static int	parse_digits(char *s, int i, int sign, int *out)
{
	long	n;

	n = 0;
	while (s[i] != '\0')
	{
		if (is_digit(s[i]) == 0)
			return (0);
		n = n * 10 + (s[i] - '0');
		if (sign == 1 && n > INT_MAX)
			return (0);
		if (sign == -1 && - n < INT_MIN)
			return (0);
		i++;
	}
	*out = (int)(n * sign);
	return (1);
}

int	is_valid_int(char *s, int *out)
{
	int	i;
	int	sign;

	if (s == NULL || s[0] == '\0' || out == NULL)
		return (0);
	i = 0;
	sign = parse_sign(s, &i);
	if (sign == 0)
		return (0);
	return (parse_digits(s, i, sign, out));
}

int	has_duplicate(t_node *a, int v)
{
	while (a != NULL)
	{
		if (a->value == v)
			return (1);
		a = a->next;
	}
	return (0);
}

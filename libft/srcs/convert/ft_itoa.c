/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 15:23:36 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 15:59:27 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	count_digits(long n)
{
	size_t	count;

	count = 1;
	while (n >= 10)
	{
		n /= 10;
		count++;
	}
	return (count);
}

char	*ft_itoa(int n)
{
	char	*str;
	long	nb;
	size_t	len;
	int		is_negative;

	nb = (long)n;
	is_negative = (nb < 0);
	if (is_negative)
		nb = -nb;
	len = count_digits(nb) + is_negative;
	str = (char *)malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	str[len] = '\0';
	if (nb == 0)
		str[--len] = '0';
	while (nb > 0)
	{
		str[--len] = (nb % 10) + '0';
		nb /= 10;
	}
	if (is_negative)
		str[0] = '-';
	return (str);
}

/*#include <stdio.h>
#include <limits.h>


static void test(int n)
{
    char *s = ft_itoa(n);
    if (!s) { printf("ft_itoa(%d) -> NULL\n", n); return; }
    printf("ft_itoa(%d) = \"%s\"\n", n, s);
    free(s);
}

int main(void)
{
    test(0);            // "0"
    test(7);            // "7"
    test(42);           // "42"
    test(-7);           // "-7"
    test(-12345);       // "-12345"
    test(INT_MAX);      // "2147483647"
    test(INT_MIN);      // "-2147483648"
    return 0;
}*/

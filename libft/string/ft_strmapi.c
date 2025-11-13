/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 17:36:25 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/28 15:54:10 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	size_t	i;
	size_t	n;
	char	*out;

	if (!s || !f)
		return (NULL);
	n = ft_strlen(s);
	out = (char *)malloc(sizeof(char) * (n + 1));
	if (!out)
		return (NULL);
	i = 0;
	while (i < n)
	{
		out[i] = f((unsigned int)i, s[i]);
		i++;
	}
	out[n] = '\0';
	return (out);
}

/*#include <stdio.h>
#include <ctype.h>
#include "libft.h"

// Alterne min/maj selon l'index
static char alt_case(unsigned int i, char c)
{
    if (!isalpha((unsigned char)c)) return c;
    return (i % 2 == 0) ? (char)toupper((unsigned char)c)
                        : (char)tolower((unsigned char)c);
}

// Décale ASCII de +1 (ex: 'a'→'b'), laisse '\0' géré par l'appelant
static char shift1(unsigned int i, char c)
{
    (void)i;
    return (char)(c + 1);
}

int main(void)
{
    char *s1 = ft_strmapi("Bonjour 42", alt_case);
    char *s2 = ft_strmapi("abcXYZ", shift1);

    printf("alt_case : %s\n", s1);   // "BoNjOuR 42"
    printf("shift1   : %s\n", s2);   // "bcdYZA"

    free(s1);
    free(s2);

    // Cas vide
    char *s3 = ft_strmapi("", alt_case);
    printf("vide     : '%s'\n", s3); // ""
    free(s3);
    return 0;
}*/

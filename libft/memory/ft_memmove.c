/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/19 16:19:46 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/29 14:20:06 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t len)
{
	unsigned char		*tmp_dest;
	const unsigned char	*tmp_src;
	size_t				i;

	if (dest == NULL && src == NULL)
		return (NULL);
	tmp_src = (const unsigned char *)src;
	tmp_dest = (unsigned char *)dest;
	i = 0;
	if (tmp_dest < tmp_src)
	{
		while (i < len)
		{
			tmp_dest[i] = tmp_src[i];
			i++;
		}
	}
	else if (tmp_dest > tmp_src)
		while (len-- > 0)
			tmp_dest[len] = tmp_src[len];
	return (dest);
}

/*#include <stdio.h>

int	main(void)
{
	char	txt1[20] = "abcdef123456";
	char	txt2[20] = "abcdef123456";
	char	txt3[30] = "qwerty";
	ft_memmove(txt3, txt1, 2);
	printf("ft_memmove overlap: %s\n", txt3);
	ft_memmove(txt2 + 3, txt2, 2);
    printf("std ft_memmove overlap: %s\n", txt2);
	printf("len = 0 return dest? : %p\n", 
	ft_memmove(txt2, txt1, 0));
	return 0;
}*/

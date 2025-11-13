/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putendl_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 11:57:02 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/30 10:51:51 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putendl_fd(char *s, int fd)
{
	if (!s)
		return ;
	if (fd < 1)
		return ;
	write(fd, s, ft_strlen(s));
	write(fd, "\n", 1);
}

/*int	main(void)
{
	ft_putendl_fd("Bonjour 42", 1);
	ft_putendl_fd(NULL, 1); // rien
	return (0);
}*/

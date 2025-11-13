/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/27 16:10:14 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/30 10:53:36 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putstr_fd(char *s, int fd)
{
	if (!s)
		return ;
	if (fd < 1)
		return ;
	write(fd, s, ft_strlen(s));
}
/*int	main(void)
{
	ft_putstr_fd("Hello", 1);
	ft_putchar_fd('\n', 1);
	ft_putstr_fd(NULL, 1); // rien ne se passe
	return (0);
}*/

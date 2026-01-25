/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   error.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:24:38 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:24:54 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ft_error_exit(t_node **a, t_node **b, char **split)
{
	if (split != NULL)
		free_split(split);
	free_stack(a);
	free_stack(b);
	write(2, "Error\n", 6);
	exit(1);
}

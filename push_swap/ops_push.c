/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ops_push.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:07:43 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:08:42 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	push_stack(t_node **dst, t_node **src)
{
	t_node	*tmp;

	if (dst == NULL || src == NULL || *src == NULL)
		return (0);
	tmp = *src;
	*src = (*src)->next;
	tmp->next = *dst;
	*dst = tmp;
	return (1);
}

void	pa(t_node **a, t_node **b)
{
	if (push_stack(a, b))
		write(1, "pa\n", 3);
}

void	pb(t_node **a, t_node **b)
{
	if (push_stack(b, a))
		write(1, "pb\n", 3);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ops_swap.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:08:10 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:08:29 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	swap_stack(t_node **s)
{
	t_node	*first;
	t_node	*second;

	if (s == NULL || *s == NULL || (*s)->next == NULL)
		return (0);
	first = *s;
	second = (*s)->next;
	first->next = second->next;
	second->next = first;
	*s = second;
	return (1);
}

void	sa(t_node **a)
{
	if (swap_stack(a))
		write(1, "sa\n", 3);
}

void	sb(t_node **b)
{
	if (swap_stack(b))
		write(1, "sb\n", 3);
}

void	ss(t_node **a, t_node **b)
{
	int	done;

	done = 0;
	if (swap_stack(a))
		done = 1;
	if (swap_stack(b))
		done = 1;
	if (done)
		write(1, "ss\n", 3);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ops_rrotate.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:10:04 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:10:16 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static t_node	*stack_prev_last(t_node *s)
{
	if (s == NULL || s->next == NULL)
		return (NULL);
	while (s->next != NULL && s->next->next != NULL)
		s = s->next;
	return (s);
}

static int	rrotate_stack(t_node **s)
{
	t_node	*prev;
	t_node	*last;

	if (s == NULL || *s == NULL || (*s)->next == NULL)
		return (0);
	prev = stack_prev_last(*s);
	last = prev->next;
	prev->next = NULL;
	last->next = *s;
	*s = last;
	return (1);
}

void	rra(t_node **a)
{
	if (rrotate_stack(a))
		write(1, "rra\n", 4);
}

void	rrb(t_node **b)
{
	if (rrotate_stack(b))
		write(1, "rrb\n", 4);
}

void	rrr(t_node **a, t_node **b)
{
	int	done;

	done = 0;
	if (rrotate_stack(a))
		done = 1;
	if (rrotate_stack(b))
		done = 1;
	if (done)
		write(1, "rrr\n", 4);
}

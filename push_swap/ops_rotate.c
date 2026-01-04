/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ops_rotate.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:09:19 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:09:30 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static t_node	*stack_last(t_node *s)
{
	while (s != NULL && s->next != NULL)
		s = s->next;
	return (s);
}

static int	rotate_stack(t_node **s)
{
	t_node	*first;
	t_node	*last;

	if (s == NULL || *s == NULL || (*s)->next == NULL)
		return (0);
	first = *s;
	*s = first->next;
	first->next = NULL;
	last = stack_last(*s);
	last->next = first;
	return (1);
}

void	ra(t_node **a)
{
	if (rotate_stack(a))
		write(1, "ra\n", 3);
}

void	rb(t_node **b)
{
	if (rotate_stack(b))
		write(1, "rb\n", 3);
}

void	rr(t_node **a, t_node **b)
{
	int	done;

	done = 0;
	if (rotate_stack(a))
		done = 1;
	if (rotate_stack(b))
		done = 1;
	if (done)
		write(1, "rr\n", 3);
}

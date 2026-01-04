/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:29:55 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:30:06 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_size(t_node *s)
{
	int	n;

	n = 0;
	while (s != NULL)
	{
		n++;
		s = s->next;
	}
	return (n);
}

int	is_sorted(t_node *s)
{
	while (s != NULL && s->next != NULL)
	{
		if (s->value > s->next->value)
			return (0);
		s = s->next;
	}
	return (1);
}

int	min_index_pos(t_node *s)
{
	int	pos;
	int	best_pos;
	int	best;

	pos = 0;
	best_pos = 0;
	best = INT_MAX;
	while (s != NULL)
	{
		if (s->index < best)
		{
			best = s->index;
			best_pos = pos;
		}
		pos++;
		s = s->next;
	}
	return (best_pos);
}

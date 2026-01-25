/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_small.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:10:26 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:10:36 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	sort_two(t_node **a)
{
	if ((*a)->index > (*a)->next->index)
		sa(a);
}

static void	sort_three(t_node **a)
{
	int	x;
	int	y;
	int	z;

	x = (*a)->index;
	y = (*a)->next->index;
	z = (*a)->next->next->index;
	if (x > y && y < z && x < z)
		sa(a);
	else if (x > y && y > z)
	{
		sa(a);
		rra(a);
	}
	else if (x > y && y < z && x > z)
		ra(a);
	else if (x < y && y > z && x < z)
	{
		sa(a);
		ra(a);
	}
	else if (x < y && y > z && x > z)
		rra(a);
}

static void	move_min_to_top(t_node **a)
{
	int	pos;
	int	n;

	pos = min_index_pos(*a);
	n = stack_size(*a);
	while (pos > 0 && pos <= n / 2)
	{
		ra(a);
		pos--;
	}
	while (pos > n / 2 && pos < n)
	{
		rra(a);
		pos++;
		if (pos == n)
			pos = 0;
	}
}

static void	sort_five(t_node **a, t_node **b)
{
	while (stack_size(*a) > 3)
	{
		move_min_to_top(a);
		pb(a, b);
	}
	sort_three(a);
	while (*b != NULL)
		pa(a, b);
}

void	sort_small(t_node **a, t_node **b)
{
	int	n;

	n = stack_size(*a);
	if (n <= 1)
		return ;
	if (n == 2)
		sort_two(a);
	else if (n == 3)
		sort_three(a);
	else if (n == 4 || n == 5)
		sort_five(a, b);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:09:40 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:09:50 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	max_bits(int n)
{
	int	bits;

	bits = 0;
	while ((n >> bits) != 0)
		bits++;
	return (bits);
}

static void	move_back_to_a(t_node **a, t_node **b)
{
	while (*b != NULL)
		pa(a, b);
}

void	radix_sort(t_node **a, t_node **b)
{
	int	i;
	int	j;
	int	n;
	int	bits;

	n = stack_size(*a);
	bits = max_bits(n - 1);
	i = 0;
	while (i < bits)
	{
		j = 0;
		while (j < n)
		{
			if ((((*a)->index >> i) & 1) == 0)
				pb(a, b);
			else
				ra(a);
			j++;
		}
		move_back_to_a(a, b);
		i++;
	}
}

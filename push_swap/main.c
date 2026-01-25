/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:25:04 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 15:11:31 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	main(int argc, char **argv)
{
	t_node	*a;
	t_node	*b;

	a = NULL;
	b = NULL;
	if (argc < 2)
		return (0);
	parse_args(argc, argv, &a);
	if (is_sorted(a) == 1)
		return (free_stack(&a), 0);
	compress_index(a);
	if (stack_size(a) <= 5)
		sort_small(&a, &b);
	else
		radix_sort(&a, &b);
	free_stack(&a);
	free_stack(&b);
	return (0);
}

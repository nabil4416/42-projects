/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:22:20 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:23:31 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	push_value(t_node **a, int v, char **split)
{
	t_node	*n;

	if (has_duplicate(*a, v) == 1)
		ft_error_exit(a, NULL, split);
	n = node_new(v);
	if (n == NULL)
		ft_error_exit(a, NULL, split);
	stack_add_back(a, n);
}

static void	parse_split(char **split, t_node **a)
{
	int	i;
	int	v;

	i = 0;
	while (split[i] != NULL)
	{
		if (is_valid_int(split[i], &v) == 0)
			ft_error_exit(a, NULL, split);
		push_value(a, v, split);
		i++;
	}
}

void	parse_args(int argc, char **argv, t_node **a)
{
	char	**split;
	int		i;

	i = 1;
	while (i < argc)
	{
		split = ft_split_ws(argv[i]);
		if (split == NULL)
			ft_error_exit(a, NULL, NULL);
		if (split[0] == NULL)
			ft_error_exit(a, NULL, split);
		parse_split(split, a);
		free_split(split);
		i++;
	}
	if (*a == NULL)
		ft_error_exit(a, NULL, NULL);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:25:49 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:26:10 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <limits.h>

typedef struct s_node
{
	int				value;
	int				index;
	struct s_node	*next;
}	t_node;

/* error / free */
void	ft_error_exit(t_node **a, t_node **b, char **split);
void	free_split(char **split);
void	free_stack(t_node **s);

/* split whitespace */
char	**ft_split_ws(char const *s);

/* parsing */
void	parse_args(int argc, char **argv, t_node **a);
int		is_valid_int(char *s, int *out);
int		has_duplicate(t_node *a, int v);

/* stack utils */
t_node	*node_new(int v);
void	stack_add_back(t_node **s, t_node *newn);
int		stack_size(t_node *s);
int		is_sorted(t_node *s);
int		min_index_pos(t_node *s);

/* operations */
void	sa(t_node **a);
void	sb(t_node **b);
void	ss(t_node **a, t_node **b);
void	pa(t_node **a, t_node **b);
void	pb(t_node **a, t_node **b);
void	ra(t_node **a);
void	rb(t_node **b);
void	rr(t_node **a, t_node **b);
void	rra(t_node **a);
void	rrb(t_node **b);
void	rrr(t_node **a, t_node **b);

/* indexing */
void	compress_index(t_node *a);

/* sorting */
void	sort_small(t_node **a, t_node **b);
void	radix_sort(t_node **a, t_node **b);

#endif
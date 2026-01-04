/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:26:52 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:27:08 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*node_new(int v)
{
	t_node	*n;

	n = malloc(sizeof(t_node));
	if (n == NULL)
		return (NULL);
	n->value = v;
	n->index = -1;
	n->next = NULL;
	return (n);
}

void	stack_add_back(t_node **s, t_node *newn)
{
	t_node	*cur;

	if (s == NULL || newn == NULL)
		return ;
	if (*s == NULL)
	{
		*s = newn;
		return ;
	}
	cur = *s;
	while (cur->next != NULL)
		cur = cur->next;
	cur->next = newn;
}

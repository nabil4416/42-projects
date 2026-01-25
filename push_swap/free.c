/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   free.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:27:28 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:27:42 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	free_split(char **split)
{
	int	i;

	if (split == NULL)
		return ;
	i = 0;
	while (split[i] != NULL)
	{
		free(split[i]);
		i++;
	}
	free(split);
}

void	free_stack(t_node **s)
{
	t_node	*cur;
	t_node	*nxt;

	if (s == NULL || *s == NULL)
		return ;
	cur = *s;
	while (cur != NULL)
	{
		nxt = cur->next;
		free(cur);
		cur = nxt;
	}
	*s = NULL;
}

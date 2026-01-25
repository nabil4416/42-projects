/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   split_ws.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 14:29:14 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/23 14:29:31 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_space(char c)
{
	if (c == ' ' || c == '\t' || c == '\n')
		return (1);
	if (c == '\v' || c == '\f' || c == '\r')
		return (1);
	return (0);
}

static int	count_words(char const *s)
{
	int	i;
	int	w;

	i = 0;
	w = 0;
	while (s[i] != '\0')
	{
		while (s[i] != '\0' && is_space(s[i]) == 1)
			i++;
		if (s[i] != '\0')
			w++;
		while (s[i] != '\0' && is_space(s[i]) == 0)
			i++;
	}
	return (w);
}

static char	*word_dup(char const *s, int start, int end)
{
	char	*out;
	int		i;

	out = (char *)malloc(sizeof(char) * (end - start + 1));
	if (out == NULL)
		return (NULL);
	i = 0;
	while (start < end)
	{
		out[i] = s[start];
		i++;
		start++;
	}
	out[i] = '\0';
	return (out);
}

static int	fill_tab(char const *s, char **tab)
{
	int	i;
	int	j;
	int	start;

	i = 0;
	j = 0;
	while (s[i] != '\0')
	{
		while (s[i] != '\0' && is_space(s[i]) == 1)
			i++;
		start = i;
		while (s[i] != '\0' && is_space(s[i]) == 0)
			i++;
		if (i > start)
		{
			tab[j] = word_dup(s, start, i);
			if (tab[j] == NULL)
				return (tab[j] = NULL, free_split(tab), 0);
			j++;
		}
	}
	tab[j] = NULL;
	return (1);
}

char	**ft_split_ws(char const *s)
{
	char	**tab;

	if (s == NULL)
		return (NULL);
	tab = (char **)malloc(sizeof(char *) * (count_words(s) + 1));
	if (tab == NULL)
		return (NULL);
	if (fill_tab(s, tab) == 0)
		return (NULL);
	return (tab);
}

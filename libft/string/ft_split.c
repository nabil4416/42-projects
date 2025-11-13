/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/30 10:20:54 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/10/30 10:22:53 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void	*free_all(char **tab, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n)
	{
		free(tab[i]);
		i++;
	}
	free(tab);
	return (NULL);
}

static char	*copy_word(char const *s, size_t start, size_t len)
{
	char	*word;
	size_t	j;

	word = (char *)malloc(len + 1);
	if (!word)
		return (NULL);
	j = 0;
	while (j < len)
	{
		word[j] = s[start + j];
		j++;
	}
	word[len] = '\0';
	return (word);
}

static int	fill_words(char const *s, char c, char **tab)
{
	size_t	i;
	size_t	idx;
	size_t	len;

	i = 0;
	idx = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (!s[i])
			break ;
		len = 0;
		while (s[i + len] && s[i + len] != c)
			len++;
		tab[idx] = copy_word(s, i, len);
		if (!tab[idx])
			return (free_all(tab, idx), -1);
		idx++;
		i += len;
	}
	tab[idx] = NULL;
	return (0);
}

char	**ft_split(char const *s, char c)
{
	size_t	i;
	size_t	count;
	char	**tab;

	if (!s)
		return (NULL);
	i = 0;
	count = 0;
	while (s[i])
	{
		while (s[i] && s[i] == c)
			i++;
		if (!s[i])
			break ;
		count++;
		while (s[i] && s[i] != c)
			i++;
	}
	tab = (char **)malloc(sizeof(char *) * (count + 1));
	if (!tab)
		return (NULL);
	if (fill_words(s, c, tab) < 0)
		return (NULL);
	return (tab);
}

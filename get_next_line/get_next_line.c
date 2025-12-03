/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/15 10:55:42 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/11/15 16:19:08 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static void	cleanup_stock(char **stock)
{
	if (*stock)
	{
		free(*stock);
		*stock = NULL;
	}
}

static char	*read_file(int fd, char *stock)
{
	char	*buf;
	char	*tmp;
	ssize_t	bytes_read;

	buf = malloc(BUFFER_SIZE + 1);
	if (!buf)
		return (cleanup_stock(&stock), NULL);
	bytes_read = 1;
	while (!ft_strchr(stock, '\n') && bytes_read > 0)
	{
		bytes_read = read(fd, buf, BUFFER_SIZE);
		if (bytes_read < 0)
			return (free(buf), cleanup_stock(&stock), NULL);
		buf[bytes_read] = '\0';
		tmp = ft_strjoin(stock, buf);
		free(stock);
		stock = tmp;
		if (!stock)
			return (free(buf), NULL);
	}
	free(buf);
	return (stock);
}

static char	*extract_line(char *stock)
{
	char	*line;
	size_t	i;

	if (!stock || !*stock)
		return (NULL);
	i = 0;
	while (stock[i] && stock[i] != '\n')
		i++;
	line = malloc(i + (stock[i] == '\n') + 1);
	if (!line)
		return (NULL);
	i = 0;
	while (stock[i] && stock[i] != '\n')
	{
		line[i] = stock[i];
		i++;
	}
	if (stock[i] == '\n')
		line[i++] = '\n';
	line[i] = '\0';
	return (line);
}

static char	*update_stock(char *stock)
{
	char	*new_stock;
	size_t	i;
	size_t	j;

	i = 0;
	while (stock[i] && stock[i] != '\n')
		i++;
	if (!stock[i])
		return (free(stock), NULL);
	new_stock = malloc(ft_strlen(stock) - i + 1);
	if (!new_stock)
		return (free(stock), NULL);
	i++;
	j = 0;
	while (stock[i])
		new_stock[j++] = stock[i++];
	new_stock[j] = '\0';
	free(stock);
	return (new_stock);
}

char	*get_next_line(int fd)
{
	static char	*stock;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
	{
		cleanup_stock(&stock);
		return (NULL);
	}
	stock = read_file(fd, stock);
	if (!stock)
		return (NULL);
	line = extract_line(stock);
	stock = update_stock(stock);
	if (!line && stock)
	{
		cleanup_stock(&stock);
		return (NULL);
	}
	return (line);
}

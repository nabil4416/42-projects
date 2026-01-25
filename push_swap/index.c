/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   index.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: nkhotbi <nkhotbi@student.42belgium.be>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 15:07:10 by nkhotbi           #+#    #+#             */
/*   Updated: 2025/12/29 10:32:23 by nkhotbi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	fill_array(t_node *a, int *arr)
{
	int	i;

	i = 0;
	while (a != NULL)
	{
		arr[i] = a->value;
		i++;
		a = a->next;
	}
}

static void	sort_int_array(int *arr, int n)
{
	int	i;
	int	j;
	int	key;

	i = 1;
	while (i < n)
	{
		key = arr[i];
		j = i - 1;
		while (j >= 0 && arr[j] > key)
		{
			arr[j + 1] = arr[j];
			j--;
		}
		arr[j + 1] = key;
		i++;
	}
}

static int	bin_search(int *arr, int n, int target)
{
	int	lo;
	int	hi;
	int	mid;

	lo = 0;
	hi = n - 1;
	while (lo <= hi)
	{
		mid = lo + (hi - lo) / 2;
		if (arr[mid] == target)
			return (mid);
		if (arr[mid] < target)
			lo = mid + 1;
		else
			hi = mid - 1;
	}
	return (-1);
}

static void	apply_index(t_node *a, int *arr, int n)
{
	int	pos;

	while (a != NULL)
	{
		pos = bin_search(arr, n, a->value);
		if (pos == -1)
		{
			free(arr);
			ft_error_exit(&a, NULL, NULL);
		}
		a->index = pos;
		a = a->next;
	}
}

void	compress_index(t_node *a)
{
	int		n;
	int		*arr;

	n = stack_size(a);
	arr = (int *)malloc(sizeof(int) * n);
	if (arr == NULL)
		ft_error_exit(&a, NULL, NULL);
	fill_array(a, arr);
	sort_int_array(arr, n);
	apply_index(a, arr, n);
	free(arr);
}

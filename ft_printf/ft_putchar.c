#include "ft_printf.h"

int	ft_putchar(int k)
{
	write(1, &k, 1);
	return (1);
}

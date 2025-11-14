# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/02 10:38:14 by nkhotbi           #+#    #+#              #
#    Updated: 2025/11/08 13:23:20 by nkhotbi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME    = libftprintf.a

CC      = cc
CFLAGS  = -Wall -Wextra -Werror
AR      = ar rcs
RM      = rm -f

DEPS    = ft_printf.h

SRC =  ft_putchar.c \
       ft_putstr.c \
       ft_putnbr.c \
       ft_putunbr.c \
       ft_putptr.c \
       ft_putnbr_hex_iter.c \
       ft_putnbr_hex_upper_iter.c \
       ft_printf.c

OBJ = $(SRC:.c=.o)

.PHONY: all clean fclean re

all: $(NAME)

$(NAME): $(OBJ)
	$(AR) $(NAME) $(OBJ)

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all


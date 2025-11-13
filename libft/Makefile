# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nkhotbi <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/30 12:02:43 by nkhotbi           #+#    #+#              #
#    Updated: 2025/10/30 12:02:48 by nkhotbi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME	= libft.a

CC		= cc
CFLAGS	= -Wall -Wextra -Werror -I.

# ====================== SOURCES ====================== #

SRCS	= \
	convert/ft_atoi.c \
	convert/ft_itoa.c \
	\
	ctype/ft_isalpha.c \
	ctype/ft_isdigit.c \
	ctype/ft_isalnum.c \
	ctype/ft_isascii.c \
	ctype/ft_isprint.c \
	ctype/ft_tolower.c \
	ctype/ft_toupper.c \
	\
	io/ft_putchar_fd.c \
	io/ft_putstr_fd.c \
	io/ft_putendl_fd.c \
	io/ft_putnbr_fd.c \
	\
	memory/ft_memset.c \
	memory/ft_bzero.c \
	memory/ft_memcpy.c \
	memory/ft_memmove.c \
	memory/ft_memchr.c \
	memory/ft_memcmp.c \
	memory/ft_calloc.c \
	\
	string/ft_strlen.c \
	string/ft_strdup.c \
	string/ft_strlcpy.c \
	string/ft_strlcat.c \
	string/ft_strchr.c \
	string/ft_strrchr.c \
	string/ft_strncmp.c \
	string/ft_strnstr.c \
	string/ft_substr.c \
	string/ft_strjoin.c \
	string/ft_strtrim.c \
	string/ft_split.c \
	string/ft_strmapi.c \
	string/ft_striteri.c

OBJS	= $(SRCS:.c=.o)

# ====================== RULES ====================== #

all: $(NAME)

$(NAME): $(OBJS)
	@ar rcs $(NAME) $(OBJS)
	@echo "✅ $(NAME) built"

%.o: %.c libft.h
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "Compiled: $<"

clean:
	@rm -f $(OBJS)
	@echo "🧹 Objects removed"

fclean: clean
	@rm -f $(NAME)
	@echo "🧹 libft.a removed"

re: fclean all

.PHONY: all clean fclean re


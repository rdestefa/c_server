CC     =	gcc
CFLAGS =	-g -Wall -Werror -std=gnu99 -Iinclude
LD     =	gcc
LDFLAGS=	-Llib
AR     =	ar
ARFLAGS=	rcs
TARGETS=	bin/server

all:		$(TARGETS)

clean:
	@echo Cleaning...
	@rm -f $(TARGETS) lib/*.a src/*.o *.log *.input

.PHONY:		all clean

# Rules for bin/server, lib/libserver.a, and any intermediate objects

src/%.o:		src/%.c
	@echo Compiling $@...
	@$(CC) $(CFLAGS) -c -o $@ $^

bin/server:		src/server.o lib/libserver.a
	@echo Linking $@...
	@$(LD) $(LDFLAGS) -o $@ $^

lib/libserver.a:		src/forking.o src/handler.o src/request.o src/single.o src/socket.o src/utils.o
	@echo Linking $@...
	@$(AR) $(ARFLAGS) $@ $^

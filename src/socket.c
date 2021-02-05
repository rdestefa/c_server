/* socket.c: Simple Socket Functions */

#include "server.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

/**
 * Allocate socket, bind it, and listen to specified port.
 *
 * @param   port        Port number to bind to and listen on.
 * @return  Allocated server socket file descriptor.
 **/
int socket_listen(const char *port) {
   /* Look up server address information */
   struct addrinfo *results;        /* Get a linked list of results (machine can have multiple IPs) */
   struct addrinfo  hints = {
      .ai_family   = AF_UNSPEC,     /* IPv4 or IPv6 */
      .ai_socktype = SOCK_STREAM,   /* TCP (Transmission Control Protocol) */
      .ai_flags    = AI_PASSIVE,    /* Listen on socket */
   };

   int status = getaddrinfo(NULL, port, &hints, &results);

   /* Check for failure */
   if (status != 0) {
      return -1;
   }

   /* For each address entry, allocate socket, bind, and listen */
   int server_fd = -1;

   for (struct addrinfo *p = results; p && server_fd < 0; p = p->ai_next) {
      /* Allocate socket */
      server_fd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
      
      /* Check for failure */
      if (server_fd < 0) {
         continue;
      }

      /* Bind socket to port */
      if (bind(server_fd, p->ai_addr, p->ai_addrlen) < 0) {
         close(server_fd);
         server_fd = -1;
         continue;
      }

      /* Listen on socket */
      if (listen(server_fd, SOMAXCONN) < 0) {
         close(server_fd);
         server_fd = -1;
         continue;
      }
   }
    
   freeaddrinfo(results);  
   return server_fd;
}

/* vim: set expandtab sts=4 sw=4 ts=8 ft=c: */

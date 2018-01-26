/*
 * gcc -o login_heap login_heap.c -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <stdlib.h>

void handler()
{
	puts("Timeout");
	exit(1);
}
void ready()
{
	signal(14, handler);
	alarm(0x40);
	setvbuf(stdout, 0LL, 2, 0LL);
	return setvbuf(stdin, 0LL, 2, 0LL);
}
void login()
{
	system("/bin/sh");
}

char *auth;
char *service;

int main(int argc, char **argv)
{
	char line[128];
	ready();

	while(1) {
		if (auth){
		      printf("[ auth = %p ]\n", auth);
		      printf("[ %s ]\n", auth);
		}
		if (service){
		      printf("[ service = %p ]\n", service);
		      printf("[ %s ]\n", service);
		}

		if(fgets(line, sizeof(line), stdin) == NULL) break;
		
		if(strncmp(line, "auth ", 5) == 0) {
			auth = malloc(0x40);
			memset(auth, 0, 0x40);
		if(strlen(line + 5) < 0x38) {
			strcpy(auth, line + 5);
		}
		}
		if(strncmp(line, "reset", 5) == 0) {
			free(auth);
		}
		if(strncmp(line, "service", 6) == 0) {
			service = strdup(line + 7);
		}
		if(strncmp(line, "login", 5) == 0) {
			if(*(auth+0x38)) {
				printf("you have logged in already!\n");
				login();
			} else {
				printf("please enter your password\n");
			}
		}
	}
	puts("hahaha~~");
}

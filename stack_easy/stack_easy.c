/*
 * gcc -o stack_easy stack_easy.c -fno-stack-protector -no-pie
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
int main(int argc, char *argv[])
{
	volatile int modified;
	char buffer[64];
	puts("do not change modified variable!!\n");

	ready();
	modified = 0;
	gets(buffer);

	if(modified != 0) {
		printf("you have changed the 'modified' variable\n");
	} else {
		printf("Try again?\n");
	}
}

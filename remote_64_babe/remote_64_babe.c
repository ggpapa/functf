/*
 * gcc -o remote_64_babe remote_64_babe.c -fno-stack-protector -no-pie
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
	char buffer[16];
	ready();
	puts("== Let's do 64bit babe ==\n");
	printf("Input :", buffer);
	gets(buffer);
	printf("Your Data :%s\n", buffer);
}

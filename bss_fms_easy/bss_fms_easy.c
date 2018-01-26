/*
 * gcc -o bss_fms_easy bss_fms_easy.c -fno-stack-protector -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int target;
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
void shell()
{
	system("/bin/sh"); 
	_exit(1);
}
void vul3()
{
	char buffer[512];
	fgets(buffer, sizeof(buffer), stdin);
	printf(buffer);
	exit(1);   
}
int main(int argc, char *argv[])
{
	char buffer[16];
	ready();
	puts("== Let's do bss fms easy ==");
	printf("%p\n",vul3);
	vul3();
}

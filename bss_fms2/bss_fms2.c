/*
 * gcc -o bss_fms2 bss_fms2.c -fno-stack-protector -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

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

void vul2()
{
	char buffer[512];

	fgets(buffer, sizeof(buffer), stdin);
	printf(buffer);
	        
	printf("your name?");
	fgets(buffer, sizeof(buffer), stdin);
	printf("\ngood job, ");
        puts(buffer);
}
int main(int argc, char *argv[])
{
	char buffer[16];
	ready();
	puts("== Let's do bss fms 2 ==");

	vul2();
}

/*
 * gcc -o bss_fms bss_fms.c -no-pie
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

void vul(char *string)
{
	printf(string);
	if(target) {
		system("/bin/sh");
	}
}
int main(int argc, char *argv[])
{
	char buffer[255];
	ready();
	puts("== Let's do bss fms ==");

	read(0,buffer,sizeof(buffer));
	vul(buffer);
}

/*
 * gcc -o start_fms start_fms.c
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
void leak(char *string)
{
	printf(string);
}
void shell()
{
	system("/bin/sh");
}
void vul(char *string,int read_len)
{
	char buffer[64];
	memcpy(buffer, string,read_len);
}
int main(int argc, char *argv[])
{
	char buffer[128];
	int read_len;
	ready();
	puts("Let's start format string bug !!");

	puts("phase1:leak");
	read(0,buffer,128);
	leak(buffer);
	puts("phase2:get shell");
	read_len = read(0,buffer,128);
	vul(buffer,read_len);
	printf("Your Data :%s\n", buffer);
}

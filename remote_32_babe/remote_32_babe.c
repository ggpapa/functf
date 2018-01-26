/*
 *  gcc -o remote_32_babe remote_32_babe.c -m32 -fno-stack-protector -no-pie
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
void vul_32bit_babe()
{
	char buffer[128];
	puts("== 32bit babe ==\n");
	printf("Input :", buffer);
	gets(buffer);
	printf("Your Data :%s\n", buffer);
}
int main(int argc, char *argv[])
{
	ready();
	vul_32bit_babe();
}

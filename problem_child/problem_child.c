/*
 *     gcc -o problem_child problem_child.c -fno-stack-protector -no-pie
 *
 *     */

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
void problem_child(char *src)
{
	char buffer[40];
	strncpy(buffer, src, 41);
	printf("%s\n", buffer);
}

main(int argc, char *argv[])
{
	char buf[100];
	ready();
	puts("Let's try, use FSP\n");
	read(0,buf,41);
	problem_child(buf);
}

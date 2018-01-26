/*
 * gcc -o test_your_name test_your_name.c -fno-stack-protector -no-pie
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
char *get_username()
{
	char buffer[512];
	char *q;
	int i;

	memset(buffer, 0, sizeof(buffer));
	gets(buffer);

	/* Strip off trailing new line characters */
	q = strchr(buffer, '\n');
	if(q) *q = 0;
	q = strchr(buffer, '\r');
	if(q) *q = 0;

	/* Convert to lower case */
	for(i = 0; i < strlen(buffer); i++) {
		buffer[i] = toupper(buffer[i]);
	}

	/* Duplicate the string and return it */
	return strdup(buffer);
}
int main(int argc, char *argv[])
{
	char * name;
	ready();
	name = get_username();
	printf("Your Name :%s\n", name);
}

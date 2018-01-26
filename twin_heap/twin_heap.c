/*
 * gcc -o twin_heap twin_heap.c -no-pie
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

struct internet {
	int priority;
	char *name;
	char *address;
};

int main(int argc, char **argv)
{
	struct internet *i1, *i2, *i3;

	ready();

	i1 = malloc(sizeof(struct internet));
	i1->priority = 1;
	i1->name = malloc(0x20);
	i1->address = malloc(0x20);

	i2 = malloc(sizeof(struct internet));
	i2->priority = 2;
	i2->name = malloc(0x20);
	i2->address = malloc(0x20);

	printf("name:");
	gets(i1->name);
	printf("address:");
	gets(i1->address);
	printf("name:");
	gets(i2->name);
	printf("address:");
	gets(i2->address);

	printf("(1) name : ");
	write(1,i1->name,0x20);
	printf(", address : ");
	write(1,i1->address,0x20);
	printf("\n(2) name : ");
	write(1,i2->name,0x20);
	printf(", address : ");
	write(1,i2->address,0x20);
	printf("\nbye, ");
	puts(i1->name);
}

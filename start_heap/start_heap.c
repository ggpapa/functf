/*
 * gcc -o start_heap start_heap.c -fno-stack-protector
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
struct data {
	  char name[64];
};

struct fp {
	  int (*fp)();
};

void winner()
{
	  printf("level passed\n");
	  system("/bin/sh");
}

void nowinner()
{
	  printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
	struct data *d;
	struct fp *f;

	ready();
	puts("start heap\n");
	d = malloc(sizeof(struct data));
	f = malloc(sizeof(struct fp));
	f->fp = nowinner;

	printf("data is at %p, fp is at %p, nowinner at %p\n", d, f, f->fp);

	gets(d->name);
		        
	f->fp();
}

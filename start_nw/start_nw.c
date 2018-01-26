/*
 * gcc -o start_nw start_nw.c -fno-stack-protector -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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
void puts_time()
{
        time_t timer;
	char buffer[26];
	struct tm* tm_info;

	time(&timer);
	tm_info = localtime(&timer);

	strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);
	puts(buffer);
}
void run()
{
	long long int i;
	long long int wanted;

	wanted = random();

	printf("Get the next '%lld' value and get back after shifting\n", wanted);

	if(fread(&i, sizeof(i), 1, stdin) == NULL) {
		exit(0);
	}

	wanted <<= 32;
	wanted += random();

	if(i == wanted) {
		printf("Thank you sir/madam\n");
		system("/bin/sh");
	} else {
		printf("I'm sorry wrong int instead\n");
	}
}
int main(int argc, char *argv[])
{
	char buffer[16];
	ready();
	puts("do you know Indian?");
	puts_time();
	puts("challenge more diffent one");

	  /* Don't do this :> */
	srandom(time(NULL));
	run();
}

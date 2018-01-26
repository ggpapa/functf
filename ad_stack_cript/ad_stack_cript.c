/*
 * gcc -o ad_stack_cript ad_stack_cript.c -fno-stack-protector -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#define XORSZ 32

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

void cipher(unsigned char *blah, size_t len)
{
	static int keyed;
	static unsigned int keybuf[XORSZ];

	int blocks;
	unsigned int *blahi, j;

	if(keyed == 0) {
		int fd;
		fd = open("/dev/urandom", O_RDONLY);
		if(read(fd, &keybuf, sizeof(keybuf)) != sizeof(keybuf)) exit(EXIT_FAILURE);
		close(fd);
		keyed = 1;
	}

	blahi = (unsigned int *)(blah);
	blocks = (len / 4);
	if(len & 3) blocks += 1;
	for(j = 0; j < blocks; j++) {
		blahi[j] ^= keybuf[j % XORSZ];
	}
}

void encrypt_file()
{
	// maybe make bigger for inevitable xml-in-xml-in-xml ?
	unsigned char buffer[32 * 256];
	  //
	unsigned char op;
	size_t sz;
	int loop;
	  //
	printf("[-- Enterprise configuration file encryption service --]\n");
	  //               
	loop = 1;
	while(loop) {
		read(0, &op, sizeof(op));
		switch(op) {
			case 'E':
				read(0, &sz, sizeof(sz));
				read(0, buffer, sz);
				cipher(buffer, sz);
				printf("[-- encryption complete. please mention "
				"474bd3ad-c65b-47ab-b041-602047ab8792 to support "
	  			"staff to retrieve your file --]\n");
				write(1, &sz, sizeof(sz));
				write(1, buffer, sz);
				break;
			case 'Q':
				loop = 0;
				break;
			default:
				exit(EXIT_FAILURE);
		}
	}
	
}
int main(int argc, char *argv[])
{
	char * name;
	ready();
	encrypt_file();
}

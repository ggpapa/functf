/*
 * gcc -o ad_stack_babe ad_stack_babe.c -fno-stack-protector -no-pie
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
int fix_path(char *path)
{
	char resolved[128];
	    
	// can't access path. will error trying to open
	if(realpath(path, resolved) == NULL) return 1; 
	    strcpy(path, resolved);
}

char *parse_http_request()
{
	char buffer[1024];
	char *path;
	char *q;

	//printf("[debug] buffer is at 0x%16p :-)\n", buffer);

	if(read(0, buffer, sizeof(buffer)) <= 0) errx(0, "Failed to read from remote host");
	if(memcmp(buffer, "GET ", 4) != 0) errx(0, "Not a GET request");

	path = &buffer[4];
	q = strchr(path, ' ');
	if(! q) errx(0, "No protocol version specified");
	*q++ = 0;
	if(strncmp(q, "HTTP/1.1", 8) != 0) errx(0, "Invalid protocol");

	fix_path(path);

	printf("trying to access %s\n", path);

	return path;
}
int main(int argc, char *argv[])
{
	char * name;
	ready();
	parse_http_request();
}

/*
 * gcc -o test_heap test_heap.c -fno-stack-protector -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define REQSZ 0x1000

char *destroylist[256];

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

void check_path(char *buf,int recvlen)
{
	char *start;
	char *p;

	/*
	*   * Work out old software bug
	*     */

	p = rindex(buf, '/');
	if(p) {
		start = strstr(buf, "ROOT");
		if(start) {
			while(*start != '/') start--;
			memmove(start, p, recvlen);
			printf("moving from %p to %p (exploit: %s / %d)\n", p, start, start < buf ?
			"yes" : "no", start - buf);
			printf("data: %s\n",start);
		}
	}
}

int get_requests(int fd)
{
	char *buf;
	int dll;
	int recvlen;
	int no;
	dll = 0;
	printf("input number(1,2,3,4)\n1:calloc\n2:FSRD\n3:puts\n4:free\n > ");
	scanf("%d",&no);
	if (no==1){
		printf("index?");
	    	scanf("%d",&dll);
		if ((dll < 0) || (dll >= 255)) return(0);
		buf = calloc(REQSZ, 1);
		destroylist[dll]=buf;
	}
	if (no==2){
		printf("index?");
	    	scanf("%d",&dll);
		if ((dll < 0) || (dll >= 255)) return(0);
		buf=destroylist[dll];
		recvlen = read(fd, buf, REQSZ);
		if(recvlen != REQSZ) return(0);
		if(strncmp(buf, "FSRD", 4) != 0) return(0);
		check_path(buf + 4,recvlen);     
	}
	if (no==3){
		printf("index?");
	    	scanf("%d",&dll);
		if ((dll < 0) || (dll >= 255)) return(0);
		write(fd, "puts OK\n", strlen("puts OK\n"));
		puts(destroylist[dll]);
	}

	if (no==4){
		printf("index?");
	    	scanf("%d",&dll);
		if ((dll < 0) || (dll >= 255)) return(0);
		write(fd, "free OK\n", strlen("free OK\n"));
		free(destroylist[dll]);
	}
}

int main(int argc, char *argv[])
{
	char * name;
	ready();
	while(1)
	{
		puts("== test heap ==");
		get_requests(0);
	}
	puts("bye~~");
}

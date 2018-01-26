/*
 * gcc -o triple_heap triple_heap.c -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

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
	setvbuf(stdin, 0LL, 2, 0LL);
}
void menu()
{
	puts("0:malloc");
	puts("1:add menu");
	puts("2:puts menu");
	puts("3:del menu");
	puts("4:list menu");
	puts("5:exit");
}
char *arr[16];
int main(int argc, char **argv)
{
	int n,i;
	ready();

	puts("start triple heap");
	menu();

	while(1){
		printf("menu>");
		scanf("%d",&n);
		switch(n){
		case 0:
		    printf("idx>");
		    scanf("%d",&i);
		    arr[i]=malloc(32);
		    break;

		case 1:
		    printf("idx>");
		    scanf("%d",&i);
		    printf("data>");
		    read(0,arr[i],32);
		    break;

		case 2:
		    printf("idx>");
		    scanf("%d",&i);
		    puts(arr[i]);
		    break;

		case 3:
		    printf("idx>");
		    scanf("%d",&i);
		    free(arr[i]);
		    break;

		case 4:
		    for (int j=0;j<16;j++)
		        if (arr[j])
				printf("%d:%s\n",j,arr[j]);
		    break;
		case 5:
		    exit(0);
		    break;

		}
	}

	puts("dynamite failed?\n");
}

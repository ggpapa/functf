/*
 * gcc -o test_blind_fms test_blind_fms.c -fno-stack-protector -no-pie
 * 
 * 			*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char username[128];

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

void ctflog(char *buffer)
{
	FILE * pFile;
	pFile = fopen ("/home/test_blind_fms/ctf.log","a+");
	if (pFile!=NULL)
	{
		fprintf (pFile,buffer);
		fclose (pFile);
	}
}

void trim(char *str)
{
	char *q;
	q = strchr(str, '\r');
	if(q) *q = 0;
	q = strchr(str, '\n');
	if(q) *q = 0;
}

void parser()
{
        char logbuf[0x200];
	char line[0x100];
	char *pw;

	printf("[final1] $ ");

	while(fgets(line, sizeof(line)-1, stdin)) {
		trim(line);
		if(strncmp(line, "username ", 9) == 0) {
			strcpy(username, line+9);
		} else if(strncmp(line, "login ", 6) == 0) {
			if(username[0] == 0) {
				printf("invalid protocol\n");
			} else {
				pw=line + 6;
	                        snprintf(logbuf, sizeof(logbuf), "\nLogin :%s, with password :%s", username, pw);
	                        ctflog(logbuf);
				printf("login failed\n");
			}
		}
		printf("[final1] $ ");
	}
}

int main(int argc, char *argv[])
{
	char * name;
	ready();
	parser();
}

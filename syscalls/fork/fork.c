#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
int main(){
    pid_t p = fork();
    if(p==-1) printf("failed process %d\n",getpid());
    else if(p==0) printf("child process %d\n",getpid());
    // any positive values
    else printf("parent process %d\n",getpid());
    return 0;
}
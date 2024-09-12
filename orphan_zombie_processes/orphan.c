#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(){
    pid_t pid = fork();
    
    if(pid<0){
        printf("error");
        exit(1);
    }
    if(pid==0){
        // child
        printf("Child process (PID: %d) is running\n", getpid());
        sleep(2);
        printf("Child process (PID: %d) is exiting\n", getpid());
        exit(0);
    }
    else{
        // parent
        printf("Parent process (PID: %d) created child (PID: %d)\n", getpid(), pid);
        sleep(5);

        int status;
        pid_t child_pid = wait(&status);
        if(child_pid>0){
            printf("Child's PID is now removed from the process table\n");
        }
    }

    return 0;
}
// inter process communication
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <unistd.h>

int main(){
    int pipefds[2];
    char *pin;
    char buffer[5];
    if(pipe(pipefds) == -1){
        perror("pipe");
        exit(EXIT_FAILURE);
    }
    pid_t pid = fork();
    if(pid == 0){
        pin = "12345\0";
        write(pipefds[1],pin,5);
        printf("Writing in child and sending to parent\n");
        sleep(3); // intentional delay
        exit(EXIT_SUCCESS);
    }
    else if(pid>0){
        wait(NULL); // waiting for child to finish
        read(pipefds[0],buffer,5); // reading from pipe and storing it in buffer

        printf("Received PIN %s\n",buffer);
    }
    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){
    // file descriptor array
    // read and write
    int pipefds[2];
    int status = pipe(pipefds);
    if(status == -1){
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    printf("Read file descriptor value, %d\n",pipefds[0]);
    printf("Write file descriptor value, %d\n",pipefds[1]);
}

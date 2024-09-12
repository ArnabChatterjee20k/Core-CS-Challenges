#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void handleSignal(int signal)
{
    if (signal == SIGINT)
    {
        printf("exiting...");
        // now we will not able to exit the program as we are not exiting
        // exit(0); // enable it to exit
    }
}

int main()
{
    signal(SIGINT, handleSignal);
    while (1)
    {
        printf("Program running. Press Ctrl+C to stop.\n");
        sleep(1); // Sleep for a second
    }
    return 0;
}
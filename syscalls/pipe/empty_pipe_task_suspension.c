#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    int pipefds[2];
    char buffer[6]; // 5 bytes + 1 null terminator

    // Create the pipe
    if (pipe(pipefds) == -1)
    {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    pid_t pid = fork();
    if (pid == -1)
    {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0)
    {                      // Child process
        close(pipefds[1]); // Close unused write end

        // Attempt to read from the pipe before the parent writes anything
        printf("Child: Attempting to read from the pipe...\n");
        ssize_t bytesRead = read(pipefds[0], buffer, 5);
        if (bytesRead > 0)
        {
            buffer[bytesRead] = '\0'; // Null terminate the string
            printf("Child: Received '%s'\n", buffer);
        }
        else
        {
            printf("Child: No data received or error occurred\n");
        }

        close(pipefds[0]); // Close read end after reading
        exit(EXIT_SUCCESS);
    }
    else
    {                      // Parent process
        close(pipefds[0]); // Close unused read end

        // Sleep for 5 seconds to simulate delayed writing
        sleep(5);

        // Write data to the pipe
        const char *message = "Hello";
        write(pipefds[1], message, 5);

        printf("Parent: Data written to the pipe\n");

        close(pipefds[1]); // Close write end after writing
        wait(NULL);        // Wait for the child process to finish
    }

    return 0;
}
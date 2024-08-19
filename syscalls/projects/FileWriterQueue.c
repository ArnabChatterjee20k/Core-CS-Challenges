// inter process communication
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

void set_nonblocking(int fd)
{
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

void writeToFile(char *data)
{
    FILE *f = fopen("output.txt", "a");
    fputs(data, f);
    fclose(f);
}

// publisher -> publising the user input to pipe
void input_reader(int write_pipe)
{
    set_nonblocking(write_pipe);
    while (1)
    {
        char input[100];
        printf("Enter some text: ");
        fflush(stdout);

        if (fgets(input, sizeof(input), stdin) != NULL)
        {
            // Remove newline character if present
            size_t len = strlen(input);
            if (len > 0 && input[len - 1] == '\n')
            {
                input[len - 1] = '\0';
            }

            // Write the input to the pipe
            write(write_pipe, input, strlen(input) + 1);
        }
    }
}

// subscriber -> reads the user input from pipe and write it to the file
void file_writer(int read_pipe)
{
    char buffer[100];
    while (1)
    {
        while (read(read_pipe, buffer, sizeof(buffer)) > 0)
        {
            printf("\nreading%s\n", buffer);
            writeToFile(buffer);
        }
    }
}

int main()
{
    // read and write pipe
    int pipe_fds[2];
    pipe(pipe_fds);
    for (int i = 0; i < 2; i++)
    {

        pid_t pid = fork();

        if (pid == -1)
        {
            perror("fork");
            exit(EXIT_FAILURE);
        }

        if (pid > 0)
        {
            // parent (input reader)
            close(pipe_fds[0]); // Close unused read end
            input_reader(pipe_fds[1]);
            close(pipe_fds[1]); // Close the write end after done
            wait(NULL);         // Wait for child to finish
        }
    }
    // child (writer)
    close(pipe_fds[1]); // Close unused write end
    file_writer(pipe_fds[0]);
    close(pipe_fds[0]); // Close the read end after done
    return 0;
}
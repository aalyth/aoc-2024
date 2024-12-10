

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include <err.h>

char **get_input(const char *filename)
{
        int fd;
        size_t result_len = 0, line_len;
        char *line_start, *line_end, *file_raw;
        char **result;
        struct stat stat;

        if ((fd = open(filename, O_RDONLY)) < 0) {
                return NULL;
        }

        if (fstat(fd, &stat) < 0) {
                close(fd);
                return NULL;
        }

        file_raw = (char *)mmap(0, stat.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
        close(fd);
        if (file_raw == (void *)-1) {
                return NULL;
        }

        line_start = file_raw;
        line_end = strchr(file_raw, '\n');
        if (NULL == line_end) {
                return NULL;
        }

        line_len = line_end - file_raw;
        result_len = stat.st_size / line_len;

        /* an extra NULL pointer is allocated to the end */
        result = calloc(result_len + 1, sizeof(char *));
        if (NULL == result) {
                return NULL;
        }

        for (int i = 0; line_end != NULL; ++i) {
                result[i] = strndup(line_start, line_len + 1);
                result[i][line_len + (i > 0)] = '\0';
                line_start = line_end;
                line_end = strchr(line_end + 1, '\n');
        }

        return result;
}

typedef struct dll_node {
        void *value;
        struct dll_node *next, *prev;
} DllNode; /* doubly linked list*/

DllNode *dll_node_init(void *value)
{
        DllNode *res = malloc(sizeof(DllNode));
        if (NULL == res)
                return NULL;
        res->value = value;
        res->prev = NULL;
        res->next = NULL;
        return res;
}

typedef struct {
        DllNode *head, *tail;
} Queue;

int main()
{
        printf("hello\n");
        char **input = get_input("input.txt");
        if (NULL == input) {
                err(1, "could not get input");
        }
        return 0;
}

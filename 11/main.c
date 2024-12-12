
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include <err.h>
#include <stdbool.h>

#include "list.c"

char **get_input(const char *filename)
{
        int fd;
        size_t result_len = 0, line_len;
        char *line_start, *line_end, *file_raw;
        char **result;
        struct stat file_stat;

        if ((fd = open(filename, O_RDONLY)) < 0) {
                return NULL;
        }

        if (fstat(fd, &file_stat) < 0) {
                close(fd);
                return NULL;
        }

        file_raw = (char *)mmap(0, file_stat.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
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
        result_len = file_stat.st_size / line_len;

        /* an extra NULL pointer is allocated to the end */
        result = calloc(result_len + 1, sizeof(char *));
        if (NULL == result) {
                return NULL;
        }

        for (int i = 0; line_end != NULL; ++i) {
                result[i] = strndup(line_start, line_len + 1);
                result[i][line_len] = '\0';
                /* jump over the current newline */
                line_start = line_end + 1;
                line_end = strchr(line_start, '\n');
        }

        munmap(file_raw, file_stat.st_size);
        return result;
}

struct dll *parse_input(const char *input)
{
        struct dll *result = dll_alloc();
        char *line_start = (char *)input;
        char *line_end = strchr(line_start, ' ');

        while (line_end != NULL) {
                char *tmp = strndup(line_start, line_end - line_start);
                uint64_t stone = atoll(tmp);
                dll_push_back(result, (void *)stone);

                line_start = line_end + 1;
                line_end = strchr(line_start, ' ');
        }

        char *tmp = strdup(line_start);
        uint64_t stone = atoll(tmp);
        dll_push_back(result, (void *)stone);
        return result;
}

size_t numlen(long long n)
{
        size_t result = 0;
        for (; n > 0; n /= 10)
                result += 1;
        return result;
}

void split_num(long long n, size_t len, long long *a, long long *b)
{
        *b = 0;
        long long exp = 1;
        for (int i = 0; i < len / 2; ++i) {
                *b += exp * (n % 10);
                exp *= 10;
                n /= 10;
        }
        *a = n;
}

void blink(struct dll *stones)
{
        for (struct dll_node *iter = stones->head; iter != NULL; iter = iter->next) {
                if ((long long)iter->value == 0) {
                        iter->value = (void *)1;
                        continue;
                }

                size_t len = numlen((long long)iter->value);
                if (len % 2 == 0) {
                        long long a, b;
                        split_num((long long)iter->value, len, &a, &b);
                        iter->value = (void *)a;

                        struct dll_node *next = iter->next;
                        struct dll_node *new = dll_node_alloc((void *)b);
                        iter->next = new;
                        new->prev = iter;
                        new->next = next;
                        iter = new;
                        continue;
                }

                iter->value = (void *)(((long long)iter->value) * 2024);
        }
}

long long stone_splits(long long n, unsigned depth)
{
        if (depth == 0) {
                return 1;
        }

        if (n == 0) {
                return stone_splits(1, depth - 1);
        }

        size_t len = numlen(n);
        if (len % 2 == 0) {
                long long a, b;
                split_num(n, len, &a, &b);
                return stone_splits(a, depth - 1) + stone_splits(b, depth - 1);
        }

        return stone_splits(n * 2024, depth - 1);
}

size_t stone_count_after_25_blinks(struct dll *stones)
{
        for (int i = 0; i < 75; ++i)
                blink(stones);
        size_t result = 0;
        for (struct dll_node *iter = stones->head; iter != NULL; iter = iter->next) {
                result += 1;
        }
        return result;
}

long long stone_count_ext(struct dll *stones)
{
        long long result = 0;
        for (struct dll_node *iter = stones->head; iter != NULL; iter = iter->next) {
                printf("%lld\n", (long long)iter->value);
                result += stone_splits((long long)iter->value, 75);
        }
        return result;
}

int main()
{
        char **input = get_input("input.txt");
        struct dll *stones = parse_input(input[0]);
        printf("result: %lu\n", stone_count_after_25_blinks(stones));
        // printf("%lld\n", stone_splits(7725, 50));
        // printf("result ext: %lld\n", stone_count_ext(stones));
        return 0;
}

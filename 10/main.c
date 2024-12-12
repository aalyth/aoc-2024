

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include <err.h>
#include <stdbool.h>

#include "queue.c"

struct coords {
        int x, y;
};

struct coords coords_new(int x, int y)
{
        return (struct coords){
                .x = x,
                .y = y,
        };
}

bool coords_valid(const struct coords c, size_t width, size_t height)
{
        return c.x >= 0 && c.x < width && c.y >= 0 && c.y < height;
}

bool coords_eq(const struct coords left, const struct coords right)
{
        return left.x == right.x && left.y == right.y;
}

struct coords coords_added(const struct coords a, const struct coords b)
{
        return coords_new(a.x + b.x, a.y + b.y);
}

/* a += b */
void coords_add(struct coords *a, const struct coords b)
{
        a->x += b.x;
        a->y += b.y;
}

char coords_idx(const char **input, const struct coords c)
{
        return input[c.y][c.x];
}

struct trail {
        struct coords start;
        struct coords current;
};

struct trail *trail_alloc(struct coords start, struct coords current)
{
        struct trail *result = (struct trail *)malloc(sizeof(struct trail));
        result->start = start;
        result->current = current;
        return result;
}

bool trail_eq(void *left, void *right)
{
        struct trail *l = left;
        struct trail *r = right;
        return coords_eq(l->start, r->start) && coords_eq(l->current, r->current);
}

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

void get_input_dimensions(const char **input, unsigned *width, unsigned *height)
{
        *width = strlen(input[0]);
        *height = 0;
        for (const char **line = input; *line != NULL; line += 1)
                *height += 1;
}

int get_trail_scores_sum(const char **input)
{
        unsigned width, height;
        struct queue bfs_queue = queue_init();

        get_input_dimensions(input, &width, &height);
        for (int y = 0; y < height; ++y) {
                for (int x = 0; x < width; ++x) {
                        if (input[y][x] == '0') {
                                struct coords origin = coords_new(x, y);
                                queue_push(&bfs_queue, trail_alloc(origin, origin));
                        }
                }
        }

        struct coords directions[4] = {
                coords_new(-1, 0),
                coords_new(1, 0),
                coords_new(0, -1),
                coords_new(0, 1),
        };

        struct dll traversed_trails = dll_new();
        struct trail *iter = queue_pop(&bfs_queue);

        unsigned int trails_count = 0;
        for (; iter != NULL; iter = queue_pop(&bfs_queue)) {
                if (coords_idx(input, iter->current) == '9') {
                        /*
                        if (!dll_contains(&traversed_trails, iter, trail_eq)) {
                                dll_push_back(&traversed_trails, iter);
                                trails_count += 1;
                        }
                        */
                        trails_count += 1;
                        continue;
                }
                for (int i = 0; i < 4; ++i) {
                        struct coords current = coords_added(iter->current, directions[i]);
                        if (coords_valid(current, width, height) &&
                            coords_idx(input, current) == coords_idx(input, iter->current) + 1)
                                queue_push(&bfs_queue, trail_alloc(iter->start, current));
                }
                free(iter);
        }

        /* free the traversed_trails DLL */
        return trails_count;
}

int main()
{
        printf("hello\n");
        char **input = get_input("input.txt");
        for (char **line = input; *line; line++) {
                printf("%s\n", *line);
        }
        if (NULL == input) {
                err(1, "could not get input");
        }
        printf("%d\n", get_trail_scores_sum((const char **)input));
        return 0;
}

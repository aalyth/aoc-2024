
#ifndef AALYTH_QUEUE_H
#define AALYTH_QUEUE_H

#include "list.c"

struct queue {
        struct dll_node *head, *tail;
};

struct queue queue_init()
{
        return (struct queue){
                .head = NULL,
                .tail = NULL,
        };
}

int queue_push(struct queue *queue, void *value)
{
        if (NULL == queue)
                return -1;
        struct dll_node *node = dll_node_alloc(value);
        if (NULL == queue->head) {
                queue->head = node;
                queue->tail = node;
        } else {
                node->next = queue->head;
                queue->head->prev = node;
                queue->head = node;
        }
        return 1;
}

void *queue_pop(struct queue *queue)
{
        if (NULL == queue || NULL == queue->tail)
                return NULL;
        void *res_value = NULL;
        if (queue->tail == queue->head) {
                res_value = queue->tail->value;
                free(queue->tail);
                queue->head = NULL;
                queue->tail = NULL;
        } else {
                res_value = queue->tail->value;
                struct dll_node *prev = queue->tail->prev;
                free(queue->tail);
                queue->tail = prev;
        }
        return res_value;
}

#endif

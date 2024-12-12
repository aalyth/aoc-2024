
#ifndef AALYTH_LIST_H
#define AALYTH_LIST_H

#include <stdlib.h>
#include <stdbool.h>

struct sll_node {
        void *value;
        struct sll_node *next;
};

struct dll_node {
        void *value;
        struct dll_node *next, *prev;
};

struct dll_node *dll_node_alloc(void *value)
{
        struct dll_node *res = (struct dll_node *)malloc(sizeof(struct dll_node));
        if (NULL == res) {
                return NULL;
        }
        res->value = value;
        res->next = NULL;
        res->prev = NULL;
        return res;
}

struct dll {
        struct dll_node *head;
        struct dll_node *tail;
};

struct dll dll_new()
{
        return (struct dll){
                .head = NULL,
                .tail = NULL,
        };
}

void dll_push_back(struct dll *dll, void *value)
{
        if (NULL == dll)
                return;
        struct dll_node *node = dll_node_alloc(value);
        if (NULL == dll->tail) {
                dll->head = node;
                dll->tail = node;
        } else {
                dll->tail->next = node;
                node->prev = dll->tail;
                dll->tail = node;
        }
}

bool dll_contains(struct dll *dll, void *value, bool (*eq_fn)(void *, void *))
{
        if (NULL == dll || NULL == dll->head)
                return false;

        struct dll_node *iter = dll->head;
        for (; iter != NULL; iter = iter->next) {
                if (eq_fn(iter->value, value))
                        return true;
        }
        return false;
}

#endif

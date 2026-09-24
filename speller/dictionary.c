/// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// intialising variable to count words
unsigned int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // initialise the word
    int word_length = strlen(word);

    // Convert it to lower case
    char lowercase[word_length + 1];

    // iterate through each character in the string

    for (int i = 0; i < word_length; i++)
    {
        lowercase[i] = tolower(word[i]);
    }

    lowercase[word_length] = '\0';

    // set cursor to linked list
    node *cursor = table[hash(lowercase)];

    // check if number of characters is 1
    if (word_length == 1)
    {
        return true;
    }
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }

        // point cursor to the next node
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    // iteriate through
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    FILE *dictionary_file = fopen(dictionary, "r");

    // reading strings from dictionary file
    while (fscanf(dictionary_file, "%s", word) != EOF)
    {
        node *word_node = malloc(sizeof(node));

        if (word_node == NULL)
        {
            // free the memory
            unload();

            // return false
            return false;
        }
        else
        {
            // copying word into the word node
            strcpy(word_node->word, word);

            int hashWord = hash(word_node->word);

            // Point the word node to the first element in the hash_table.
            word_node->next = table[hashWord];

            // Point the hash table to the new node
            table[hashWord] = word_node;
            word_count++;
        }
    }
    // close the file
    fclose(dictionary_file);

    // return true if successful operation
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // return wordcount
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // iterate through hashtable
    for (int i = 0; i < N; i++)
    {
        // set pointer to head of list
        node *cursor = table[i];

        // traverse list
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        // if cursor is at the end of the linked list, free cursor itself.
        free(cursor);
    }
    return true;
    // This function makes sure you aren't leaking any memory
}
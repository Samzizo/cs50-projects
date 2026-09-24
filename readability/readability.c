#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>


int count_words(string text);
int count_letters(string text);
int count_sentences(string text);

int main(void)
{
    // Global variables
    int words, letters, sentences;
    float L, S, test;

    // Prompt user
    string text = get_string("Text: ");

    // count words, letters, sentences
    words = count_words(text);
    letters = count_letters(text);
    sentences = count_sentences(text);

    // calculate index
    L = ((float)letters / (float)words) * 100;
    S = ((float)sentences / (float)words) * 100;
    test = 0.0588 * L - 0.296 * S - 15.8;
    int index = round(test);

    // Condition to define the grade
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}

// Define function to calculate words
int count_words(string text)
{
    int words = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // Check white space
        if (text[i] == ' ')
        {
            words++;
        }
    }
    // add one to calculate last word
    words = words + 1;
    return words;
}

// Define function to calculate letters
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        //Check alphabet
        if (isalpha(text[i]) != 0)
        {
            letters++;
        }
    }
    return letters;
}

// Define function to calculate sentences
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // Check the end of each sentence
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

// function’s prototype
bool only_digits(string argv[]);

int main(int argc, string argv[])
{


    // check if user input a valid key
    if (!(argc == 2 && only_digits(argv)))
    {
        // Print out the exact format
        printf("Usage: ./caesar key \n");
        return 1;
    }


    if (argc == 2)
    {
        //convert key to int
        int key = atoi(argv[1]);

        //Get the plain text from user
        string text = get_string("plaintext: ");

        //print ciphertext
        printf("ciphertext: ");

        // loop over the text entred
        for (int i = 0 ; i < strlen(text); i++)
        {
            // Check if alphabet
            if (isalpha(text[i]))
            {

                // Check if uppercase
                if (isupper(text[i]))
                {
                    // Get the number of alpha
                    int position = (int)text[i] - 65;
                    // Use the formula to compute the letter
                    int computeLetter = (position + key) % 26;
                    // Convert to new letter
                    int ciphertext = (65 + computeLetter);
                    // Print ciphertext
                    printf("%c", ciphertext);
                }

                else
                {
                    // Check if lowercase
                    if (islower(text[i]))
                    {
                        //Get the number of alpha
                        int position = (int)text[i] - 97;
                        //Use the formula to compute the letter
                        int computeLetter = (position + key) % 26;
                        //Convert to new letter
                        int ciphertext = (97 + computeLetter);
                        //Print ciphertext
                        printf("%c", ciphertext);
                    }
                }
            }
            else
            {
                printf("%c", text[i]);
            }
        }

        //print new line at the end
        printf("\n");
    }

    // Hundle error
    else
    {
        printf("Error\n");
        return 1;
    }
    return 0;
}

// Define function to check if the key is digit
bool only_digits(string argv[])
{
    // loop over key entred
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        // Check if not digit
        if (!isdigit(argv[1][i]))
        {
            return false;
        }
    }
    //else return true
    return true;
}
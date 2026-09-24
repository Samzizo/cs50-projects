#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get Name from user
    string name = get_string("what is your name? ");
    // Print out Hello name using place
    printf("hello, %s\n", name);
}
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // open file
    FILE *inFile = fopen(argv[1], "r");

    // if file fail to open
    if (inFile == NULL)
    {
        fprintf(inFile, "Could not open file\n");
        return 2;
    }

    //set out file pointer to NULL
    FILE *outFile = NULL;

    //create an array to store 512 bytes
    BYTE buffer[512];

    //count jpeg files found
    int countJpeg = 0;

    //string to hold a filename
    char *filename = malloc(8 * sizeof(char));

    //Read 512 bytes into a buffer
    while (fread(buffer, sizeof(BYTE) * 512, 1, inFile) == 1)
    {
        //check if jpeg is found
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xE0)
        {
            //close outptr if jpeg was found before and written into ###.jpg
            if (outFile != NULL)
            {
                fclose(outFile);
            }
            sprintf(filename, "%03d.jpg", countJpeg++);
            //open filename for writing
            outFile = fopen(filename, "w");
        }

        // Writing into the new file
        if (outFile != NULL)
        {
            fwrite(buffer, sizeof(BYTE) * 512, 1, outFile);
        }
    }

    // Closing any remaining file
    if (outFile != NULL)
    {
        fclose(outFile);
    }
    fclose(inFile);

    // free malloc memory
    free(filename);

    return 0;
}
#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // iterating over rows
    for (int i = 0; i < height; i++)
    {
        // iterating over columns
        for (int j = 0; j < width; j++)
        {
            // Get the colors values
            int originalRed = image[i][j].rgbtRed;
            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;

            //calculate the rounded average value of each pixel
            int avg = round(((float)originalRed + (float)originalBlue + (float)originalGreen) / 3);

            //set the avg to be the new value of each pixel
            image[i][j].rgbtRed = image[i][j].rgbtBlue = image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // iterating over rows
    for (int i = 0; i < height; i++)
    {
        // iterating over columns
        for (int j = 0; j < width; j++)
        {
            // Get the colors values
            int originalRed = image[i][j].rgbtRed;
            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;

            // Calculate the sepia color values
            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }

            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // iterate through the array until the mid-point
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE temp = image[i][j];

            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // copy of original image
    RGBTRIPLE temp[height][width];

    // iterating over rows
    for (int i = 0; i < height; i++)
    {
        // iterating over columns
        for (int j = 0; j < width; j++)
        {
            // declare variables to calculate the sum of each color
            int sum_Red, sum_Blue, sum_Green;
            sum_Red = sum_Blue = sum_Green = 0;
            float counter = 0.0;

            //Get the contiguous pexels
            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    // current row
                    int row = i + x;
                    // current column
                    int column = j + y;

                    //check for valid contiguous pexels
                    // if it does skip that
                    if (row < 0 || row > (height - 1) || column < 0 || column > (width - 1))
                    {
                        continue;
                    }

                    //Get the image value
                    sum_Red += image[row][column].rgbtRed;
                    sum_Green += image[row][column].rgbtGreen;
                    sum_Blue += image[row][column].rgbtBlue;

                    counter++;
                }

                //do the average of contiguous pexels
                temp[i][j].rgbtRed = round(sum_Red / counter);
                temp[i][j].rgbtGreen = round(sum_Green / counter);
                temp[i][j].rgbtBlue = round(sum_Blue / counter);
            }
        }

    }

    // updating values in the original image.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}

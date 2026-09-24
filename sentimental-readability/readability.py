# TODO

from cs50 import get_string

text = get_string("Text: ")

# declar global variables
words = 0
letters = 0
sentences = 0


for i in range(len(text)):
    # count letters
    if (text[i].isalpha()):
        letters += 1
    # count words
    if (text[i].isspace()):
        words += 1
    # count sentences
    if (text[i] == '.' or text[i] == '?' or text[i] == '!'):
        sentences += 1

# add one to calculate last word
words = words + 1

# average of letters per 100 words
L = (letters / words) * 100
# average of sentences per 100 words
S = (sentences / words) * 100

count = 0.0588 * L - 0.296 * S - 15.8

# round the results
index = round(count)

# check the grade
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
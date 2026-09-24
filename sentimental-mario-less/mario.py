# TODO

from cs50 import get_int

# rejects a height < 0 and >9
while True:
    # get the height from user
    height = get_int("Height: ")
    # if the height between
    if height > 0 and height < 9:
        break

# loop over height and print #
for i in range(height):
    # declare space variable
    space = " "
    print(space * (height-i - 1), end="")
    print("#" * (i+1))

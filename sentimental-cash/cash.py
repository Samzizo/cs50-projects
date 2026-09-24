# TODO
from cs50 import get_float

# Verify that the user entered valid numbers
while True:
    cent = get_float("Change Owed: ")
    if cent > 0:
        break

# initialize number of coins variable
coins = 0

# convert dollars to cents
cents = cent * 100

# calculate quarters
while cents >= 25:
    cents = cents - 25
    coins = coins + 1

# calculate dimes
while cents >= 10:
    cents = cents - 10
    coins = coins + 1

# calculate nickels
while cents >= 5:
    cents = cents - 5
    coins = coins + 1

# calculate pennies
while cents >= 1:
    cents = cents - 1
    coins = coins + 1

print(coins)
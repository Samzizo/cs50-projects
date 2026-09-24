-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Check the description of crime scence
SELECT description FROM crime_scene_reports
WHERE day = 28
    AND month = 7
    AND year = 2021
    AND street = 'Humphrey Street';

'''
Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
Interviews were conducted today with three witnesses who were present at the time
each of their interview transcripts mentions the bakery.
Littering took place at 16:36. No known witnesses.
'''

-- three witnesses who were present at the time at 10:15am their interview transcripts mentions the bakery
SELECT name, transcript FROM interviews
WHERE day = 28
    AND month = 7
    AND year = 2021
    AND transcript LIKE '%bakery%';

"""
Eugene:
    I don't know the thief's name, but it was someone I recognized.
    Earlier this morning, before I arrived at Emma's bakery,
    I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
"""
-- According to Eugene transcript locking for people name who withdrw money that day

SELECT name FROM people WHERE id IN
(
    SELECT person_id FROM bank_accounts WHERE account_number IN
    (
        SELECT account_number FROM atm_transactions
        WHERE day = 28
        AND month = 7
        AND year = 2021
        AND transaction_type = 'withdraw'
        AND atm_location = 'Leggett Street'
    )
);


"""
Raymond:
    As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
    I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
    The thief then asked the person on the other end of the phone to purchase the flight ticket.
"""
-- CHECK phone caller

SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE day = 28
AND month = 7
AND year = 2021
AND duration < 60;

-- check for phone reciever
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE day = 28
AND month = 7
AND year = 2021
AND duration < 60;

-- CHECK the flight next day
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id =
(
    SELECT id FROM flights
    WHERE day = 29
    AND month = 7
    AND year = 2021
    ORDER BY hour,minute LIMIT 1
);


"""
Ruth:
    Sometime within ten minutes of the theft,
    I saw the thief get into a car in the bakery parking lot and drive away.
    If you have security footage from the bakery parking lot, you might want to
    look for cars that left the parking lot in that time frame.
"""
-- Check names who is take a car that day after 10 min
SELECT name FROM people WHERE license_plate IN
(
    SELECT license_plate FROM bakery_security_logs
    WHERE day = 28
    AND month = 7
    AND year = 2021
    AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity = 'exit'
);




-- COLLECT all the informations goted
SELECT name FROM people WHERE id IN
(
    SELECT person_id FROM bank_accounts WHERE account_number IN
    (
        SELECT account_number FROM atm_transactions
        WHERE day = 28
        AND month = 7
        AND year = 2021
        AND transaction_type = 'withdraw'
        AND atm_location = 'Leggett Street'
    )
)
INTERSECT

SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE day = 28
AND month = 7
AND year = 2021
AND duration < 60

INTERSECT

SELECT name FROM people WHERE license_plate IN
(
    SELECT license_plate FROM bakery_security_logs
    WHERE day = 28
    AND month = 7
    AND year = 2021
    AND hour = 10
    AND minute >=15 AND minute <=25
    AND activity = 'exit'
)
INTERSECT

SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id =(
    SELECT id FROM flights
    WHERE day = 29
    AND month = 7
    AND year = 2021
    ORDER BY hour,minute LIMIT 1
);
'''
The thief is :
+-------+
| name  |
+-------+
| Bruce |
+-------+
'''
-- DIstination the theif escaped to

SELECT city FROM airports WHERE id =(
    SELECT origin_airport_id FROM flights WHERE day = 29
    AND month = 7
    AND year = 2021 AND id = (
        SELECT flight_id FROM passengers WHERE passport_number = (
            SELECT passport_number FROM people WHERE name = 'Bruce'
        )
    )
);

'''THE DISTINATION city is New York City '''

-- find accomplice
SELECT * FROM people WHERE phone_number IN
(
    SELECT receiver FROM phone_calls WHERE year=2021 AND month=7 AND day=28 AND duration < 60 AND caller IN
    (
        SELECT phone_number FROM people WHERE name = 'Bruce'
    )
);

''' Robin is the accomplice '''




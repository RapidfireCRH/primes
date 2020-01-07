import sqlite3
from sqlite3 import Error
import math


def isdiv(div, dvd):
    """
    :param div: divisor
    :param dvd: dividend
    :return: bool: if the divisor is a prime factor of the dividend
    """
    return dvd % div == 0


def isprime(db_file, num):
    """
    :param db_file: name (and path) of db to read divisors from
    :param num: number to check (dividend)
    :return: bool: true if num is prime (no common factors)
    """
    sqrt_num = math.floor(math.sqrt(num))
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute("SELECT prime FROM pri WHERE prime<={0}".format(sqrt_num))

    rows = cur.fetchall()
    for row in rows:
        if isdiv(row[0], num):
            conn.close()
            return False
    conn.close()
    return True


def isprimectl(db_file, begin, end):
    """
    :param db_file: name (and path) of db to read divisors from
    :param begin: beginning prime number check
    :param end: end prime number check
    :return: list: list of numbers that are prime
    """
    ret = []
    for x in range(begin, end + 1):
        if isprime(db_file, x):
            ret.append(x)

    return ret


def writeback(db_file, lst):
    """
    :param db_file: File to write to
    :param lst: list to import
    :return: int:
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        for x in lst:
            cur.execute("insert into pri (prime) ({0})".format(x))

        cur.execute("commit")
    except Error as e:
        print(e)

    cur.close()
    return

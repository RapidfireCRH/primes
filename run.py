import sys
import db
import primes


def main(db_file, begin, end):
    """
    :param db_file: File to use as a database
    :param begin: Number to start prime checks on
    :param end: Number to end prime checks on
    :return: list of primes found
    """
    db.init(db_file)
    return primes.isprimectl(db_file, begin, end)


if len(sys.argv) != 3:
    print("Use: run.py db_name begin_num end_num")
main(sys.argv[1], sys.argv[2], sys.argv[3])

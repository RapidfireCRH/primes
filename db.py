import sqlite3
from urllib import request
from os import path

con = 0
_init = False


def createdb(db_file):
    """
    :param db_file: location of dbfile to create
    :return: null
    """
    global con, _init
    if not _init:
        init(db_file)
        return

    cur = con.cursor()
    cur.execute("Create table pri (prime INTEGER);")
    cur.execute("Create unique index p on pri(prime);")
    cur.execute("Create table pri_notes (dldfile INTEGER, large_prime INTEGER);")
    con.execute("Insert into pri_notes (dldfile, large_prime) values (0,0);")
    con.commit()
    return


def init(db_file):
    global con, _init
    if _init:
        return
    _init = True

    if path.exists(db_file):
        con = sqlite3.connect(db_file)
    else:
        con = sqlite3.connect(db_file)
        createdb(db_file)

    return


def populatenextset(db_file):
    """
    This method loads the next set of 1 million primes from http://crh.dyndns-server.com/primes
    :return:
    """
    if not _init:
        init(db_file)
    cur = con.cursor()
    cur.execute("select * from pri_notes")
    row = cur.fetchall()
    filenum, _nul = row[0]
    resp = request.urlopen('http://crh.dyndns-server.com/primes/{0}.txt'.format(filenum + 1))
    lines = resp.readlines();
    for line in lines:
        line = line.replace(b'\r\n', b'').decode('ASCII')
        cur.execute("insert into pri (prime) values({0})".format(line))

    con.commit()

    cur.execute("select max(prime) from pri")
    maxpri = cur.fetchall()[0][0]

    cur.execute("delete from pri_notes where dldfile={0}".format(filenum))
    filenum += 1
    cur.execute("insert into pri_notes (dldfile, large_prime) values({0},{1});".format(filenum, maxpri))

    con.commit()

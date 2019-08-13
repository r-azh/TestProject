import sys
from bson import ObjectId

__author__ = 'R.Azh'

import psycopg2
import psycopg2.extensions
import psycopg2.extras


# $ sudo -u postgres psql postgres
print('############################## connect ##############################')

try:
    conn = psycopg2.connect(database='test', user='postgres', host='localhost', password='123456')
    # if db don't exist it wont connect
    print('connected')
except psycopg2.DatabaseError:
    # You can connect to the default system database postgres and then issue your query to create the new database.
    conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='123456')
    # conn.set_isolation_level(psycopg2._ext.ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    dbname = 'test'
    cur.execute('CREATE DATABASE ' + dbname)
    cur.close()


print('############################## get version ##############################')

# The next step is to define a cursor to work with. It is important to note that Python/Psycopg cursors are not
# cursors as defined by PostgreSQL.
try:
    cur = conn.cursor()
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    print(ver)


    rows = cur.fetchall()
    print(rows)
    for row in rows:
        print("   ", row[0])

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)


finally:

    if conn:
        conn.close()

print('############################## insert query ##############################')
try:
    conn = psycopg2.connect(database='test', user='postgres', host='localhost', password='123456')
    cur = conn.cursor()

    #  The psycopg2 adapter also has the ability to deal with some of the special data types that PostgreSQL has available.
    #  One such example is arrays. Let's review the table below:
    cur.execute('CREATE TABLE IF NOT EXISTS bar(Id VARCHAR(24) PRIMARY KEY, "Name" VARCHAR(20), Notes TEXT[], Price INT)')

    # correct way
    # Note that you have to use %s no matter what type you actually have.

    cur.execute('INSERT INTO bar(Id, "Name", Price) VALUES(%s, %s, %s)',
                ('{}'.format(str(ObjectId())), "Audi", 52642))
    cur.execute('INSERT INTO bar VALUES(%s,%s,%s,%s)', ('%s' % (str(ObjectId())), "Mercedes", "{sample note}", 57127))

    # sql injection prone
    # You really, really shouldn't use python string formatting to build queries - they are prone to SQL injection. And
    # your actual problem is that you use " for quoting while you have to use ' for quoting
    # (" quotes table/column names etc, ' quotes strings).
    # http://initd.org/psycopg/docs/usage.html#query-parameters

    cur.execute('''INSERT INTO bar(Id, "Name", Price) VALUES(3,'Skoda',9000)''')
    cur.execute('''INSERT INTO bar(Id, "Name", Price) VALUES(4,'Volvo',29000)''')
    cur.execute('''INSERT INTO bar(Id, "Name", Price) VALUES(5,'Bentley',350000)''')
    cur.execute('''INSERT INTO bar(Id, "Name", Price) VALUES(6,'Citroen',21000)''')
    cur.execute('''INSERT INTO bar(Id, "Name", Price) VALUES(7,'Hummer',41400)''')
    cur.execute('''INSERT INTO bar(Id, "Name", Price) VALUES(8,'Volkswagen',21600)''')
    cur.execute('''insert into bar(Id, Notes) values(9, '{An array of text, Another array of text}')''')
    conn.commit()

    # list1 = [(None,) if str(x)=='nan' else (x,) for x in list1]
    # cursor.executemany("""INSERT INTO table VALUES %s""", list1)

except psycopg2.DatabaseError as e:
    if conn:
        conn.rollback()

    print('Error %s' % e)
    sys.exit(1)

print('############################## select query ##############################')
try:
    cur.execute("SELECT * FROM bar")

    rows = cur.fetchall()

    for row in rows:
        print(row)

# The default cursor returns the data in a tuple of tuples. When we use a dictionary cursor, the data is sent in a
# form of Python dictionaries. This way we can refer to the data by their column names.
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM bar")

    rows2 = cursor.fetchall()   # makes res a list of psycopg2.extras.DictRows

    for row in cursor:
        print(row)
        print("%s %s %s" % (row["Id"], row["Name"], row["Price"]))
# The Python psycopg2 module supports two types of placeholders: ANSI C printf format and the Python extended format.
    uid = str(ObjectId())
    #  parameterized statements with Python extended format.
    cur.execute('INSERT INTO bar(Id, "Name", Price) VALUES(%s, %s, %s)', ('{}'.format(uid), "Tiba", 520002))
    cur.execute("SELECT * FROM bar WHERE Id=%(id)s", {'id': uid})

    print(cur.fetchone())

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)

print('############################## update query ##############################')
uid = str(ObjectId())
cur.execute('INSERT INTO bar(Id, "Name", Price) VALUES(%s, %s, %s)', ('{}'.format(uid), "Pride", 52642))
uPrice = 77665544
# ANSI C printf format
cur.execute('UPDATE bar SET Price=%s WHERE Id=%s', (uPrice, uid))
conn.commit()

print('############################## Delete query ##############################')
uid = str(ObjectId())
cur.execute('INSERT INTO bar(Id, "Name", Price) VALUES(%s, %s, %s)', ('{}'.format(uid), "Pride", 756982))
cur.execute('DELETE FROM bar WHERE Id=%(id)s', {'id': uid})
# check Passing parameters to SQL queries
cur.execute('DELETE FROM bar WHERE Id=%s', (uid,))
cur.execute('DELETE FROM bar WHERE Id=%s', [uid])
conn.commit()
print(uid)

print('############################## DROP Table ###########################')
# cur.execute('''DROP TABLE bar''')
# conn.commit()
# conn.close()

print('############################## DROP DB ##############################')

# PostgreSQL can not drop databases within a transaction, it is an all or nothing command. If you want to drop the
#  database you would need to change the isolation level of the database this is done using the following.
# should be connected to another (default) db other than the one being removed

# con = psycopg2.connect(database='template1', user='postgres', host='localhost', password='123456')
# con.set_isolation_level(0)
# cur = con.cursor()
# cur.execute('''DROP DATABASE test''')
# con.commit()


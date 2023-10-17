# connect to the database
import sqlite3

conn = sqlite3.connect('Resources/database.db')
# create a cursor
c = conn.cursor()

# select from players table
c.execute("SELECT count(*) FROM players")

# print the results
print(c.fetchall())

# # delete table
# c.execute("DROP TABLE IF EXISTS test")
# # commit the changes
# conn.commit()
# # close the connection

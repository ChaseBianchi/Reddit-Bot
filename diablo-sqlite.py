import sqlite3

conn = sqlite3.connect('diablo.db')

c = conn.cursor()

# c.execute("""CREATE TABLE post (
#             id text,
#             author text,
#             keywords text
#             )""")

# c.execute("INSERT INTO post VALUES ('esfl3','fakeauthor','pc, breakpoints')")

c.execute("SELECT * FROM post WHERE author='fakeauthor'")

print(c.fetchall())

conn.commit()

conn.close()





# class Comment:
    
#     def __init__(self, id, author, keywords, date):
#         self.id = id
#         self.author = author
#         self.keywords = keywords
#         self.date = date
        

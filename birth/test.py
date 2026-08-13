import sqlite3
db=sqlite3.connect('db/db.sqlite3')
cur=db.cursor()
cur.execute("select regno from birth_birth where regno like '%" + '1970' + "%' ")
rw=cur.fetchall()

for i in rw:
    try:
        cur.execute("UPDATE birth_birth set scandocs=file/B" + str(i[0]) + ".pdf where regno=" + str(i[0]))
        db.commit()
        print(i)
    except:
        db.rollback()
import sqlite3


sqlite_file = 'my_db.sqlite'

class Db_Interface:
    #{id},{title},{company},{url},{salary}
    def init_tables(self):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        c.execute('CREATE TABLE listings(\
                                       ID CHAR(32) PRIMARY KEY     NOT NULL,\
                                       TITLE           TEXT    NOT NULL,\
                                       COMPANY            TEXT     NOT NULL,\
                                       SALARY            TEXT     NOT NULL,\
                                       URL        TEXT);')
        conn.commit()
        conn.close()

    def drop_tables(self):
        try:
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute('DROP TABLE listings;')
            conn.commit()
            conn.close()
        except:
            #TODO return something
            pass


    #id,url,company,link,salary,description

    def persist_listing(self,listing):
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        base_string = "INSERT INTO listings (ID,TITLE,COMPANY,SALARY,URL) VALUES ('{id}','{title}','{company}','{salary}','{url}');"
        query = base_string.format(id=listing.id,
                                   title=listing.title,
                                   company=listing.company,
                                   salary=listing.salary,
                                   url=listing.url
                                   )
        #print(query)
        try:
            conn.execute(query)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            print('an object with same id already exists in the DB')
            #TODO RETURN SOMETHING
            pass


if __name__ == "__main__":
    pass
    #drop_tables()
    init_tables()
    #persist_listing(None)
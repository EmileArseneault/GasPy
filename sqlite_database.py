import sqlite3

DEFAULT_DATABASE_PATH = "./GasPyDb"

CREATE_GASPOINT_TABLE = """CREATE TABLE IF NOT EXISTS gaspoint(
                               id integer PRIMARY KEY,
                               date integer NOT NULL,
                               liters real NOT NULL,
                               price real NOT NULL,
                               location text);"""

class GasPyDatabase():

    def __init__(self, path):
        self.database_path = path
        self.conn = None
        self.cur = None

        try:
            self.conn = sqlite3.connect(path)
        except Error as e:
            print("Could not connect to database {} : {}".format(self.database_path, e))

        try:
            self.cur = self.conn.cursor()
        except Error as e:
            print("Could not create cursor : {}".format(e))

    def close(self):
        self.cur = None

        if self.conn:
            self.conn.commit()
            self.conn.close()

        self.conn = None

    def generate_db(self):
        if self.cur is not None:
            self.cur.execute(CREATE_GASPOINT_TABLE)

    def add_data_point(self, date, liters, price, location=None):
        if self.cur is not None:
            self.cur.execute("""INSERT INTO gaspoint(date, liters, price, location)
                                    VALUES(date(?),?,?,?)""", (date, liters, price, location))
            return self.cur.lastrowid

def main():
    print(sqlite3.version)
    db = GasPyDatabase(DEFAULT_DATABASE_PATH)
    db.generate_db()
    db.add_data_point("2020-03-01", 38.192, 1.129, "costco")
    db.close()

if __name__ == "__main__":
    main()

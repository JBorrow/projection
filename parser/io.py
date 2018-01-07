import sqlite3

class Database(object):
    """
    Database writer object.
    """
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)

        if not self.check_tables_exist():
            self.create_tables()


    def check_tables_exist(self):
        """
        Checks if tables exist.

        TODO: Implement this.
        """

        return False


    def create_tables(self):
        """
        Create the tables in the sqlite3 database.
        """
        

        c = self.conn.cursor()

        c.execute("""
            create table collectors
            (input text, line real, regex text, uid text, text text,
             temporary_replacement text, output_text text, id real)"""
        )

        c.execute("""
            create table sections
            (input text, regex text, uid text, text text,
             temporary_replacement text, output_text text,
             startline real, endline real, id real)"""
        )
                
        self.conn.commit()

        c.close()

        return




import sqlite3
from .generators import Collector, Section

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

    
    def insert_collectors(self, collectors):
        """
        Insert an item into the collectors table.
        """

        c = self.conn.cursor()

        c.execute("insert into collectors values (?,?,?,?,?,?,?,?)", collector)

        self.conn.commit()

        c.close()

        return


    def insert_sections(self, section):
        """
        Insert an item into the sections table.
        """

        c = self.conn.cursor()

        c.execute("insert into sections values (?,?,?,?,?,?,?,?,?)", section)

        self.conn.commit()

        c.close()

        return

    
    def grab_collectors(self):
        """
        Grab a list of all collectors as collector objects.
        """

        c = self.conn.cursor()

        db_output = c.execute("select * from collectors")

        c.close()

        keys = [
            "input",
            "line",
            "regex",
            "uid",
            "text",
            "temporary_replacement",
            "output_text",
            "id",
        ]

        collectors = [Collector(dict(zip(keys, values))) for values in db_output]

        return collectors


    def grab_sections(self):
        """
        Grab a list of all sections as section objects.
        """

        c = self.conn.cursor()

        db_output = c.execute("select * from sections")

        c.close()

        keys = [
            "input",
            "regex",
            "uid",
            "text",
            "temporary_replacement",
            "output_text",
            "startline",
            "endline",
            "id",
        ]

        sections = [Section(dict(zip(keys, values))) for values in db_output]

        return sections


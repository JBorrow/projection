import sqlite3

from .generators import Collector, Section


class Database(object):
    """
    Database writer object.
    """
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)

        try:
            self.create_tables()
        except sqlite3.OperationalError:
            # Tables already created
            pass



    def __del__(self):
        self.close_connection()

        return


    def create_tables(self):
        """
        Create the tables in the sqlite3 database.
        """
        
        c = self.conn.cursor()

        c.execute("""
            create table collectors
            (input text, line int, capture int, 
             regex text, uid text, text text,
             temporary_replacement text, output_text text, id text)"""
        )

        c.execute("""
            create table sections
            (input text, line int, level int, capture int, 
             regex text, uid text, text text,
             temporary_replacement text, output_text text,
             startline int, endline int, id text)"""
        )

        c.execute("""
            create table removals
            (input text, regex text, uid text, id text, line int,
             text text, temporary_replacement text, output_text text,
             startline int, endline int, se text)"""
        )
                
        self.conn.commit()

        c.close()

        return

    
    def insert_collector(self, collector):
        """
        Insert an item into the collectors table.
        """

        c = self.conn.cursor()

        c.execute("insert into collectors values (?,?,?,?,?,?,?,?,?)", collector)

        self.conn.commit()

        c.close()

        return


    def insert_section(self, section):
        """
        Insert an item into the sections table.
        """

        c = self.conn.cursor()

        c.execute("insert into sections values (?,?,?,?,?,?,?,?,?,?,?,?)", section)

        self.conn.commit()

        c.close()

        return


    def insert_removal(self, removal):
        """
        Insert a removal into the removals table.
        """
        
        c = self.conn.cursor()

        c.execute("insert into removals values(?,?,?,?,?,?,?,?,?,?,?)", removal)

        self.conn.commit()

        c.close()

    
    def grab_collectors(self):
        """
        Grab a list of all collectors as collector objects.
        """

        c = self.conn.cursor()

        db_output = c.execute("select * from collectors")

        keys = [
            "input",
            "line",
            "capture",
            "regex",
            "uid",
            "text",
            "temporary_replacement",
            "output_text",
            "id",
        ]

        collectors = [Collector(dict(zip(keys, values))) for values in db_output]

        c.close()

        return collectors


    def grab_sections(self):
        """
        Grab a list of all sections as section objects.
        """

        c = self.conn.cursor()

        db_output = c.execute("select * from sections")

        keys = [
            "input",
            "line",
            "level",
            "capture",
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

        c.close()

        return sections


    def grab_removals(self):
        """
        Grab a list of all removals as removal objects.
        """

        c = self.conn.cursor()

        db_output = c.execute("select * from removals")

        keys = [
            "input",
            "regex",
            "uid",
            "id",
            "line",
            "text",
            "temporary_replacement",
            "output_text",
            "startline",
            "endline",
            "se",
        ]

        removals = [Removal(dict(zip(keys, values))) for values in db_output]

        c.close()

        return removals


    def close_connection(self):
        """
        Closes the connection.
        """
        self.conn.close()

        return


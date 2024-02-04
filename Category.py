import mysql.connector

class Category:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_categories(self):
        self.cursor.execute("SELECT name FROM category")
        return [category[0] for category in self.cursor.fetchall()]
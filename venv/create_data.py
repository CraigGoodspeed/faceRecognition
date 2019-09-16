import mysql.connector as db


class DataHelper:

    @staticmethod
    def get_connection():
        return db.Connect(
            host="localhost",
            user="root",
            passwd="root01",
            db="faces"
        )

    @staticmethod
    def execute(statement):
        db = DataHelper.get_connection()
        return db.cursor().execute(statement)

    @staticmethod
    def select(statement):
        connection = DataHelper.get_connection()
        cursor = connection.cursor()
        cursor.execute(statement)
        return cursor.fetchall()

    @staticmethod
    def get_cursor():
        return DataHelper.get_connection().cursor()
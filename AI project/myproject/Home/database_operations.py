from django.db import connection

def fetch_data_from_database():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Home_cartitem')
        rows = cursor.fetchall()

    return rows

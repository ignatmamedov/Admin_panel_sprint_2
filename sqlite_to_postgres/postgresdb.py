import os
import psycopg2


class PostgresDB:

    @staticmethod
    def copy_db_from_csv(table_name):
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            options=os.environ.get('DB_OPTIONS'),
            password=os.environ.get('DB_PASSWORD')
        )
        cur = conn.cursor()
        with open('{}.csv'.format(table_name), newline='', encoding='utf-8') as file:
            next(file)
            cur.copy_from(file, table_name, sep='|')
        conn.commit()
        cur.close()
        conn.close()






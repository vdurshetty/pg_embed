import psycopg2
import os
from dotenv import load_dotenv  # only needed locally

load_dotenv()
pgvector_key = os.environ.get("pg_password")


# Connect to your database
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password=pgvector_key,
#     host="db.hjutiuttzsdrzoyzuzmx.supabase.co",
#     port=5432
# )

connection_str = "postgresql://postgres:" + pgvector_key + "@db.hjutiuttzsdrzoyzuzmx.supabase.co:5432/postgres"

conn = psycopg2.connect(
    connection_str,
    sslmode="require"
)



def pg_create_table_index(script):
    # Create a table with a vector column
    cursor = conn.cursor()
    try:
        with cursor as cur:
            cur.execute(script)
            conn.commit()
        if "table" in script.lower():
            print("Table successfully created...")
        elif "index" in script.lower():
            print("Index successfully created...")
        cursor.close()
    except Exception as e:
        # code that runs if an error occurs
        print("Error occurred:", e)


def pg_drop_table_index(table_name, object_type="TABLE"):
    cursor = conn.cursor()
    sql = "DROP ".join(object_type).join(" IF EXISTS ").join(table_name).join(";")
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def pg_get_connection():
    return conn


def pg_insert_image(sql, filename, filepath, embedding):
    cursor = conn.cursor()
    cursor.execute(sql, (filename, filepath, embedding))
    conn.commit()
    cursor.close()


def pg_insert(sql, text, embedding):
    cursor = conn.cursor()
    cursor.execute(sql, (text, embedding))
    conn.commit()
    cursor.close()


def pg_execute(sql, embedding):
    cursor = conn.cursor()
    cursor.execute(sql, (embedding,))
    return cursor.fetchall()


def pg_execute_many(sql, data):
    cursor = conn.cursor()
    cursor.executemany(sql, data)
    conn.commit()
    print("Multiple Records Inserted")
    cursor.close()


def pg_sql_execute(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def close_connection(cursor):
    cursor.close()
    conn.close()

# create vector extension in postgresql database
# pg_create_table("CREATE EXTENSION vector;")

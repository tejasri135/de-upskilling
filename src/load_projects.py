import os
import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="de_upskilling",
    user="postgres",
    password="devpassword"
)
cur = conn.cursor()
cur.execute("""Create table if not exists projects
                ( project_id int primary key,
                  project_name varchar, 
                  client varchar,
                  status varchar)""")
conn.commit()
with open("data/projects.csv","r")as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(""" INSERT INTO PROJECTS (project_id,project_name,client,status) values
                    (%s,%s,%s,%s)
                    on conflict(project_id)
                    do update 
                    set project_name = excluded.project_name,
                     client = excluded.client,
                     status = excluded.status 
                    """,row)
        conn.commit()
cur.close()    
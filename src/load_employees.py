import csv
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="de_upskilling",
    user="postgres",
    password="devpassword"
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INT PRIMARY KEY,
        name TEXT,
        department TEXT
    )
""")
cur.execute("truncate table employees;")

# open data/employees.csv

with open("data/employees.csv","r",newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute("INSERT INTO employees VALUES (%s, %s, %s)", row)
        ## upsert is other option instead of truncate. 
        # upsert (ON CONFLICT DO UPDATE) is the alternative to truncate.
        # truncate = full refresh, handles deletes, rewrites everything.
        # upsert = incremental, cheaper on large tables, won't remove deleted rows.
#       cur.execute("INSERT INTO employees (employee_id, name, department)
#       VALUES (%s, %s, %s)
#       ON CONFLICT (employee_id) DO UPDATE
#       SET name = EXCLUDED.name,  
#       department = EXCLUDED.department 
#       """, row)
     

conn.commit()
cur.close()
conn.close()
print("Done")
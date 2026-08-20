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

# Load employee data from the CSV into the database
with open("data/employees.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            """
            INSERT INTO employees (employee_id, name, department)
            VALUES (%s, %s, %s)
            ON CONFLICT (employee_id) DO NOTHING
            """,
            (int(row["employee_id"]), row["name"], row["department"]),
        )

conn.commit()
cur.close()
conn.close()
print("Done")
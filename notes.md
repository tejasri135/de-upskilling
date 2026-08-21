## Noting down all the learnings
## setup postgres Connection: 

Commands:
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="de_upskilling",
    user="postgres",
    password="devpassword"
)
cur = conn.cursor()

Start Postgres:
    docker compose up -d

Connect to it:
    docker exec -it de-postgres psql -U postgres -d de_upskilling

Activate venv:
    source .venv/bin/activate

    open file "r" - read mode ; "w" = write mode, "a" = append


Upsert: Below is the postgres example for SCD type 1
on conflict with EXCLUDED.
cur.execute("""
    INSERT INTO employees (employee_id, name, department)
    VALUES (%s, %s, %s)
    ON CONFLICT (employee_id) DO UPDATE
    SET name = EXCLUDED.name,  --updating the postgres row with the new value as per the csv so that row is uptodate
        department = EXCLUDED.department -- updating the postgres row with the new value as per the csv so that row is uptodate
""", row)

DO NOTHING ---> retain the old row.

        # upsert (ON CONFLICT DO UPDATE) is the alternative to truncate.
        # truncate = full refresh, handles deletes, rewrites everything.
        # upsert = incremental, cheaper on large tables, won't remove deleted rows.
#       cur.execute("INSERT INTO employees (employee_id, name, department)

## Encountered Issues:
Port 5432 conflict: a Homebrew Postgres was already listening and
winning over the container. Fixed with launchctl unload -w.

## Questions:
#insert query
%s is place holder not a string 
alternative way .. %s row by row is slow for larger data .. we can check copy command in postgres .psycopg2 exposes it as copy_expert

1. execute_batch — sends many rows in fewer round trips:
## python
from psycopg2.extras import execute_batch
execute_batch(cur, "INSERT INTO employees VALUES (%s, %s, %s)", all_rows, page_size=1000)

2. COPY — Postgres streams the file directly:

## python
with open("data/employees.csv") as f:
    cur.copy_expert("COPY employees FROM STDIN WITH CSV HEADER", f)

****
 COPY is fastest but it's a raw insert. No ON CONFLICT, no upsert. So the real production pattern is COPY into a staging table, then MERGE from staging into the target. Fast load, plus idempotency.
****

#alternative to psycopg2(gpt ans).. Layers built on top of a driver:
SQLAlchemy — You write Python objects, it generates SQL. Still uses psycopg2 underneath.
pandas — df.to_sql(...) loads a DataFrame straight into a table. Also uses SQLAlchemy, which uses psycopg2.

what if we need to load 2B rows or 2TB file??
2TB data to a row-store OLTP database is usually the wrong architecture.
first of all 2TB is not for a transactional database and postgres is row-store rite we might need a columnar store db for it  .. either u need to partition the file and load it by removing all the indexes using copy commnad and add all the necessary indexes later  .
what we should do in that case:
What you'd actually do:

Convert to Parquet, partitioned by a sensible key. Columnar, compressed — 2TB of CSV often becomes 200–400GB of Parquet.
Query it in place with Athena, DuckDB, or Spark. No load step at all.
Load only the aggregates into Postgres — the summary tables people actually query.
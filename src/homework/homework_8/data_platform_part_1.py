import os
import snowflake.connector

conn = snowflake.connector.connect(
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASSWORD'],
    account=os.environ['SNOWFLAKE_ACCOUNT'],
    warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
    database=os.environ['SNOWFLAKE_DATABASE'],
    schema=os.environ['SNOWFLAKE_SCHEMA'],
    role=os.environ['SNOWFLAKE_ROLE']
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_VERSION()")
print(cur.fetchone())
cur.close()
conn.close()

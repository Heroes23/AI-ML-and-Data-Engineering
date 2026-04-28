import pandas as pd

# custom modules
from engine import engine

try:
    # Connection
    cursor = engine.connect()

    print("Connection to Snowflake is successful.")

except Exception as e:
    print(f"Error occurred: {e}")

try: 
    df=pd.read_sql_table(table_name="breast_cancer", con=cursor) 
    print(df.head(10))
    print("Table from Snowflake loaded successfully.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the connection
    cursor.close()



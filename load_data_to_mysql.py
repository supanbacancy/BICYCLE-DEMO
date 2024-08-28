import dask.dataframe as dd
import mysql.connector

def load_parquet_to_mysql(parquet_file_path, mysql_host, mysql_user, mysql_password, mysql_database):
    df = dd.read_parquet(parquet_file_path)
    pandas_df = df.compute()

    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = conn.cursor()

        # Confirming database connection
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name[0]}")

        # Creating the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS bicycle_location (
            id INT AUTO_INCREMENT PRIMARY KEY,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            bicycle_id VARCHAR(36)
        )
        """
        cursor.execute(create_table_query)
        print("Table created successfully")

        # Inserting data
        insert_query = "INSERT INTO bicycle_location (latitude, longitude, bicycle_id) VALUES (%s, %s, %s)"
        values = [tuple(row) for row in pandas_df[['Latitude', 'Longitude', 'BicycleID']].values.tolist()]
        cursor.executemany(insert_query, values)
        conn.commit()
        print("Data inserted successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

if __name__ == "__main__":
    parquet_file_path = "bicycle_data.parquet"
    mysql_host = "mysql"
    mysql_user = "root"
    mysql_password = "my-secret-pw"
    mysql_database = "bicycle_data"

    load_parquet_to_mysql(parquet_file_path, mysql_host, mysql_user, mysql_password, mysql_database)

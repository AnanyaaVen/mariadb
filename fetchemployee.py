import sys
import csv  # Fixed: Imported the csv module
import mariadb

config = {
    "host": "serverless-europe-west4.sysp0000.db2.skysql.com",
    "port": 4020,
    "user": "dbpgf33691976",
    "password": "WJ*51zwohsDJLAI33Fluja0",
    "ssl_ca": "globalsignrootca.pem",
    "database": "threadnet",
    "ssl_verify_cert": True
}

def fetch_all_employees():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**config)
        print(" Successfully connected to MariaDB SkySQL database!")
        
        cursor = conn.cursor()
        
        query = """
        SELECT 
            e.id, 
            e.first_name, 
            e.last_name, 
            e.salary, 
            d.department_name, 
            d.location
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.id;
        """
        
        cursor.execute(query)
        
        # Exporting to csv 
        # Fixed: Changed 'cur' to 'cursor' to match variable name above
        headers = [column[0] for column in cursor.description]
        
        # Fixed: Changed 'cur' to 'cursor'
        rows = cursor.fetchall()
    
        # Write to CSV file (Ensured all inner blocks use clean 4-space alignment)
        with open("employees_export.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)  # Write the header row
            writer.writerows(rows)    # Write all data rows
        
        print(f"Success! Exported {len(rows)} rows to employees_export.csv")

    except Exception as e:
        print(f"❌ Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("\n Database connection closed safely.")

if __name__ == "__main__":
    fetch_all_employees()
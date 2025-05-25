import os
import pandas as pd
from snowflake.connector import connect
import snowflake.connector.errors

# Snowflake credentials
SNOWFLAKE_ACCOUNT = "SYVEUEV-DQ70641"
SNOWFLAKE_USER = "YOURSTORYHACKATHON"
SNOWFLAKE_PASSWORD = "Hsy$20305@Ravi"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE = "YOURSTORYHACKATHON"
SNOWFLAKE_SCHEMA = "PUBLIC"

def test_connection():
    """Test connection to Snowflake"""
    try:
        conn = connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            role=SNOWFLAKE_ROLE,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        print("✅ Connected to Snowflake")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Snowflake: {str(e)}")
        return None

def test_query(conn):
    """Test a simple query"""
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        
        # List tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\n🔍 Tables in the database:")
        for table in tables:
            print(f"  - {table[1]}")
        
        # Test specific tables and columns
        print("\n📊 Testing specific columns:")
        
        # Test STATES table for HDI column
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'STATES' AND COLUMN_NAME = 'HDI'")
        hdi_exists = cursor.fetchone()[0] > 0
        print(f"  - HDI column in STATES table: {'✅ EXISTS' if hdi_exists else '❌ MISSING'}")
        
        # Test CULTURAL_HERITAGE table for UNESCO_STATUS column
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'CULTURAL_HERITAGE' AND COLUMN_NAME = 'UNESCO_STATUS'")
        unesco_exists = cursor.fetchone()[0] > 0
        print(f"  - UNESCO_STATUS column in CULTURAL_HERITAGE table: {'✅ EXISTS' if unesco_exists else '❌ MISSING'}")
        
        # Test CULTURAL_HERITAGE table for CULTURAL_CONTRIBUTIONS column
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'CULTURAL_HERITAGE' AND COLUMN_NAME = 'CULTURAL_CONTRIBUTIONS'")
        contributions_exists = cursor.fetchone()[0] > 0
        print(f"  - CULTURAL_CONTRIBUTIONS column in CULTURAL_HERITAGE table: {'✅ EXISTS' if contributions_exists else '❌ MISSING'}")
        
        # Test FESTIVALS table for RELIGION_TYPE column
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'FESTIVALS' AND COLUMN_NAME = 'RELIGION_TYPE'")
        religion_type_exists = cursor.fetchone()[0] > 0
        print(f"  - RELIGION_TYPE column in FESTIVALS table: {'✅ EXISTS' if religion_type_exists else '❌ MISSING'}")
        
        # Test POPULATION_GROWTH table for Urban/Rural population columns
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'POPULATION_GROWTH' AND COLUMN_NAME = 'URBAN_POPULATION_PCT'")
        urban_exists = cursor.fetchone()[0] > 0
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'POPULATION_GROWTH' AND COLUMN_NAME = 'RURAL_POPULATION_PCT'")
        rural_exists = cursor.fetchone()[0] > 0
        print(f"  - Urban/Rural population columns in POPULATION_GROWTH table: {'✅ BOTH EXIST' if urban_exists and rural_exists else '❌ MISSING ONE OR BOTH'}")
        
        # Test FESTIVALS table for column data types
        cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'FESTIVALS' 
        AND COLUMN_NAME IN ('ECONOMIC_IMPACT_MILLIONS_USD', 'PARTICIPANTS_MILLIONS', 'DURATION_DAYS')
        """)
        
        festival_column_types = cursor.fetchall()
        print("\n📊 Testing FESTIVALS table column data types:")
        
        for column in festival_column_types:
            column_name = column[0]
            data_type = column[1]
            
            if column_name == 'ECONOMIC_IMPACT_MILLIONS_USD':
                is_correct = data_type.upper() in ('FLOAT', 'DOUBLE', 'REAL', 'NUMBER')
                print(f"  - ECONOMIC_IMPACT_MILLIONS_USD data type: {data_type} {'✅ CORRECT' if is_correct else '❌ SHOULD BE FLOAT'}")
            
            if column_name == 'PARTICIPANTS_MILLIONS':
                is_correct = data_type.upper() in ('FLOAT', 'DOUBLE', 'REAL', 'NUMBER')
                print(f"  - PARTICIPANTS_MILLIONS data type: {data_type} {'✅ CORRECT' if is_correct else '❌ SHOULD BE FLOAT'}")
            
            if column_name == 'DURATION_DAYS':
                is_correct = data_type.upper() in ('INT', 'INTEGER', 'NUMBER')
                print(f"  - DURATION_DAYS data type: {data_type} {'✅ CORRECT' if is_correct else '❌ SHOULD BE INT'}")
        
        # Sample data from each table
        print("\n🔍 Sample data from tables:")
        
        # STATES with HDI
        cursor.execute("SELECT STATE, POPULATION_MILLIONS, LITERACY_RATE_PCT, HDI FROM STATES LIMIT 3")
        states = cursor.fetchall()
        print("\nSTATES sample (with HDI):")
        for state in states:
            print(f"  - {state[0]}: Population={state[1]}M, Literacy={state[2]}%, HDI={state[3]}")
        
        # CULTURAL_HERITAGE with UNESCO_STATUS and CULTURAL_CONTRIBUTIONS
        cursor.execute("SELECT CULTURAL_ELEMENT, COUNT, UNESCO_STATUS, CULTURAL_CONTRIBUTIONS FROM CULTURAL_HERITAGE LIMIT 3")
        heritage = cursor.fetchall()
        print("\nCULTURAL_HERITAGE sample (with UNESCO_STATUS and CULTURAL_CONTRIBUTIONS):")
        for item in heritage:
            print(f"  - {item[0]}: Count={item[1]}, UNESCO Status={item[2] or 'Not Listed'}, Contributions={item[3] or 'Various'}")
        
        # FESTIVALS with RELIGION_TYPE and numeric columns
        cursor.execute("""
        SELECT FESTIVAL, RELIGION_TYPE, ECONOMIC_IMPACT_MILLIONS_USD, PARTICIPANTS_MILLIONS, DURATION_DAYS 
        FROM FESTIVALS 
        LIMIT 3
        """)
        festivals = cursor.fetchall()
        print("\nFESTIVALS sample (with RELIGION_TYPE and numeric columns):")
        for festival in festivals:
            print(f"  - {festival[0]}: Type={festival[1]}, Economic Impact=${festival[2]}M, Participants={festival[3]}M, Duration={festival[4]} days")
        
        # POPULATION_GROWTH with Urban/Rural percentages
        cursor.execute("SELECT YEAR, POPULATION_MILLIONS, URBAN_POPULATION_PCT, RURAL_POPULATION_PCT FROM POPULATION_GROWTH LIMIT 3")
        population = cursor.fetchall()
        print("\nPOPULATION_GROWTH sample (with Urban/Rural percentages):")
        for year in population:
            print(f"  - Year {year[0]}: Population={year[1]}M, Urban={year[2]}%, Rural={year[3]}%")
        
        # Test image table
        cursor.execute("SELECT COUNT(*) FROM IMAGES")
        count = cursor.fetchone()[0]
        print(f"\n🖼️ Images in database: {count}")
        
        cursor.close()
    except Exception as e:
        print(f"❌ Error querying Snowflake: {str(e)}")

def main():
    """Main function to test Snowflake connection"""
    print("🚀 Testing Snowflake connection...")
    
    # Test connection
    conn = test_connection()
    if conn:
        # Test query
        test_query(conn)
        
        # Close connection
        conn.close()
        print("\n✅ Snowflake test completed!")

if __name__ == "__main__":
    main() 
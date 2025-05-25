import os
import pandas as pd
from snowflake.connector import connect
import sys
import snowflake.connector.errors
from snowflake.connector.pandas_tools import write_pandas

# Add your Snowflake credentials here or use environment variables
SNOWFLAKE_ACCOUNT = os.environ.get("SNOWFLAKE_ACCOUNT", "SYVEUEV-DQ70641")
SNOWFLAKE_USER = os.environ.get("SNOWFLAKE_USER", "YOURSTORYHACKATHON")
SNOWFLAKE_PASSWORD = os.environ.get("SNOWFLAKE_PASSWORD", "Hsy$20305@Ravi")
SNOWFLAKE_ROLE = os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")

# Define database and schema names
DATABASE_NAME = "YOURSTORYHACKATHON"
SCHEMA_NAME = "PUBLIC"

def create_connection():
    """Create a connection to Snowflake"""
    try:
        conn = connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            role=SNOWFLAKE_ROLE,
            warehouse=SNOWFLAKE_WAREHOUSE
        )
        print("✅ Connected to Snowflake")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Snowflake: {str(e)}")
        sys.exit(1)

def setup_database(conn):
    """Set up the database and schema"""
    try:
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"✅ Database {DATABASE_NAME} created or already exists")
        
        # Use the database
        cursor.execute(f"USE DATABASE {DATABASE_NAME}")
        
        # Create schema if it doesn't exist
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
        print(f"✅ Schema {SCHEMA_NAME} created or already exists")
        
        # Use the schema
        cursor.execute(f"USE SCHEMA {SCHEMA_NAME}")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def standardize_column_names(df, csv_path):
    """
    Standardize column names for consistency between local files and Snowflake
    
    This function ensures that column names follow a consistent convention:
    1. Replace problematic characters like '/', '(', ')', etc.
    2. Handle special cases like 'Religion/Type' which becomes 'RELIGION_TYPE' in Snowflake
    3. Add missing columns needed by the application
    """
    # Make a copy to avoid modifying the original
    df_copy = df.copy()
    
    # Define comprehensive column mappings for different data types
    column_mappings = {
        # Economic data column mapping
        'economic': {
            'Year': 'YEAR',
            'GDP (billion USD)': 'GDP_BILLION_USD',
            'GDP Growth Rate (%)': 'GDP_GROWTH_RATE_PCT',
            'Per Capita Income (USD)': 'PER_CAPITA_INCOME_USD',
            'Agriculture': 'AGRICULTURE',
            'Industry': 'INDUSTRY',
            'Services': 'SERVICES',
            'Exports (billion USD)': 'EXPORTS_BILLION_USD',
            'Imports (billion USD)': 'IMPORTS_BILLION_USD',
            'Unemployment Rate (%)': 'UNEMPLOYMENT_RATE_PCT'
        },
        
        # Education data column mapping
        'education': {
            'Level': 'LEVEL',
            'Enrollment (millions)': 'ENROLLMENT_MILLIONS',
            'Male (%)': 'MALE_PCT',
            'Female (%)': 'FEMALE_PCT',
            'Literacy Rate (%)': 'LITERACY_RATE_PCT',
            'National Literacy Rate (%)': 'NATIONAL_LITERACY_RATE_PCT',
            'Primary Enrollment Rate (%)': 'PRIMARY_ENROLLMENT_RATE_PCT',
            'Institutions': 'INSTITUTIONS',
            'State Names': 'STATE_NAMES',
            'State Literacy Rates (%)': 'STATE_LITERACY_RATES_PCT',
            'State Primary Enrollment (%)': 'STATE_PRIMARY_ENROLLMENT_PCT',
            'State Secondary Enrollment (%)': 'STATE_SECONDARY_ENROLLMENT_PCT',
            'State Higher Ed Enrollment (%)': 'STATE_HIGHER_ED_ENROLLMENT_PCT',
            'Male Literacy (%)': 'MALE_LITERACY_PCT',
            'Female Literacy (%)': 'FEMALE_LITERACY_PCT',
            'Literacy Gap': 'LITERACY_GAP',
            'Number of Primary Schools': 'NUMBER_OF_PRIMARY_SCHOOLS',
            'Number of Secondary Schools': 'NUMBER_OF_SECONDARY_SCHOOLS',
            'Number of Colleges': 'NUMBER_OF_COLLEGES',
            'Number of Universities': 'NUMBER_OF_UNIVERSITIES',
            'Number of Technical Institutions': 'NUMBER_OF_TECHNICAL_INSTITUTIONS',
            'Higher Education Enrollment (millions)': 'HIGHER_EDUCATION_ENROLLMENT_MILLIONS',
            'PISA Score': 'PISA_SCORE',
            'Global Rank': 'GLOBAL_RANK',
            'University Ranking': 'UNIVERSITY_RANKING',
            'Teacher-Student Ratio Primary': 'TEACHER_STUDENT_RATIO_PRIMARY',
            'Teacher-Student Ratio Secondary': 'TEACHER_STUDENT_RATIO_SECONDARY',
            'Teacher-Student Ratio Higher Ed': 'TEACHER_STUDENT_RATIO_HIGHER_ED',
            'Gender Parity Primary': 'GENDER_PARITY_PRIMARY',
            'Gender Parity Secondary': 'GENDER_PARITY_SECONDARY',
            'Gender Parity Higher Ed': 'GENDER_PARITY_HIGHER_ED',
            'Literacy Rate Years': 'LITERACY_RATE_YEARS',
            'Literacy Rate History': 'LITERACY_RATE_HISTORY'
        },
        
        # Festival data column mapping
        'festivals': {
            'Festival': 'FESTIVAL',
            'Religion/Type': 'RELIGION_TYPE',
            'Primary States': 'PRIMARY_STATES',
            'Month': 'MONTH',
            'Season': 'SEASON',
            'Description': 'DESCRIPTION',
            'Cultural Significance': 'CULTURAL_SIGNIFICANCE',
            'Regional Variations': 'REGIONAL_VARIATIONS',
            'Global Celebrations': 'GLOBAL_CELEBRATIONS',
            'Participants (millions)': 'PARTICIPANTS_MILLIONS',
            'Economic Impact (Millions USD)': 'ECONOMIC_IMPACT_MILLIONS_USD',
            'Economic Impact (USD millions)': 'ECONOMIC_IMPACT_MILLIONS_USD',
            'Tourist Attraction Level': 'TOURIST_ATTRACTION_LEVEL',
            'Environmental Impact': 'ENVIRONMENTAL_IMPACT',
            'Duration (days)': 'DURATION_DAYS'
        },
        
        # Historical timeline data column mapping
        'historical': {
            'Period': 'PERIOD',
            'Start Year': 'START_YEAR',
            'End Year': 'END_YEAR',
            'Era': 'ERA',
            'Major Events': 'MAJOR_EVENTS',
            'Significance': 'SIGNIFICANCE',
            'Time Period': 'TIME_PERIOD',
            'Cultural Developments': 'CULTURAL_DEVELOPMENTS',
            'Religious Trends': 'RELIGIOUS_TRENDS',
            'Art & Architecture': 'ART_ARCHITECTURE',
            'Economic Systems': 'ECONOMIC_SYSTEMS',
            'Scientific Advances': 'SCIENTIFIC_ADVANCES',
            'Historical Legacy': 'HISTORICAL_LEGACY'
        }
    }
    
    # Determine which mapping to use based on file path
    data_type = None
    if 'economic_data.csv' in csv_path.lower() or 'economic_sectors.csv' in csv_path.lower():
        data_type = 'economic'
    elif 'education.csv' in csv_path.lower():
        data_type = 'education'
    elif 'festivals.csv' in csv_path.lower():
        data_type = 'festivals'
    elif 'historical_timeline.csv' in csv_path.lower():
        data_type = 'historical'
    
    # Apply specific mapping if available
    if data_type and data_type in column_mappings:
        mapping = column_mappings[data_type]
        rename_cols = {}
        
        for app_col, snowflake_col in mapping.items():
            if app_col in df_copy.columns:
                rename_cols[app_col] = snowflake_col
        
        if rename_cols:
            df_copy = df_copy.rename(columns=rename_cols)
    else:
        # Default transformation for other files
        clean_columns = []
        for col in df_copy.columns:
            # Clean and uppercase the column name
            col_name = col.upper().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "PCT")
            col_name = col_name.replace("/", "_").replace(",", "_").replace("-", "_")
            clean_columns.append(col_name)
        
        df_copy.columns = clean_columns
    
    # Add special columns based on file type
    if 'states.csv' in csv_path.lower():
        if 'HDI' not in df_copy.columns:
            # HDI values by state (approximations based on 2021-22 data)
            hdi_values = {
                'Kerala': 0.782,
                'Delhi': 0.746,
                'Goa': 0.761,
                'Punjab': 0.723,
                'Tamil Nadu': 0.708,
                'Himachal Pradesh': 0.725,
                'Maharashtra': 0.696,
                'Karnataka': 0.682,
                'Telangana': 0.669,
                'Gujarat': 0.672,
                'Haryana': 0.708,
                'Uttarakhand': 0.684,
                'West Bengal': 0.641,
                'Andhra Pradesh': 0.649,
                'Rajasthan': 0.629,
                'Odisha': 0.606,
                'Assam': 0.613,
                'Jharkhand': 0.599,
                'Chhattisgarh': 0.613,
                'Madhya Pradesh': 0.603,
                'Uttar Pradesh': 0.596,
                'Bihar': 0.574,
                'Manipur': 0.697,
                'Tripura': 0.658,
                'Meghalaya': 0.636,
                'Nagaland': 0.679,
                'Sikkim': 0.716,
                'Mizoram': 0.705,
                'Arunachal Pradesh': 0.662,
                'Jammu and Kashmir': 0.688,
                'Chandigarh': 0.775,
                'Puducherry': 0.738,
                'Andaman and Nicobar Islands': 0.74,
                'Lakshadweep': 0.712,
                'Dadra and Nagar Haveli and Daman and Diu': 0.663,
                'Ladakh': 0.674
            }
            
            # Apply HDI values based on state name
            if 'STATE' in df_copy.columns:
                df_copy['HDI'] = df_copy['STATE'].map(lambda x: hdi_values.get(x, 0.65))
    
    elif 'population_growth.csv' in csv_path.lower():
        if 'URBAN_POPULATION_PCT' not in df_copy.columns and 'Urban Population (%)' not in df_copy.columns:
            df_copy['URBAN_POPULATION_PCT'] = 35.0
        if 'RURAL_POPULATION_PCT' not in df_copy.columns and 'Rural Population (%)' not in df_copy.columns:
            df_copy['RURAL_POPULATION_PCT'] = 65.0
    
    elif 'education.csv' in csv_path.lower():
        # Add education-specific columns
        if 'PRIMARY_ENROLLMENT_RATE_PCT' not in df_copy.columns:
            df_copy['PRIMARY_ENROLLMENT_RATE_PCT'] = 95.0
        if 'STATE_LITERACY_RATES_PCT' not in df_copy.columns:
            df_copy['STATE_LITERACY_RATES_PCT'] = '94.0, 93.7, 92.5, 90.0, 89.8, 89.1, 89.0, 84.6, 82.8, 81.3'
    
    elif 'cultural_heritage.csv' in csv_path.lower():
        if 'UNESCO_STATUS' not in df_copy.columns:
            df_copy['UNESCO_STATUS'] = "Not Listed"
        if 'CULTURAL_CONTRIBUTIONS' not in df_copy.columns:
            df_copy['CULTURAL_CONTRIBUTIONS'] = "Various cultural contributions"
    
    elif 'festivals.csv' in csv_path.lower():
        # Make sure special columns exist
        if 'RELIGION_TYPE' not in df_copy.columns:
            df_copy['RELIGION_TYPE'] = "Cultural"
            
        # Add other required columns
        if 'PARTICIPANTS_MILLIONS' not in df_copy.columns:
            df_copy['PARTICIPANTS_MILLIONS'] = 5.0  # Default value
            
        if 'ECONOMIC_IMPACT_MILLIONS_USD' not in df_copy.columns:
            df_copy['ECONOMIC_IMPACT_MILLIONS_USD'] = 250.0  # Default value
            
        if 'TOURIST_ATTRACTION_LEVEL' not in df_copy.columns:
            df_copy['TOURIST_ATTRACTION_LEVEL'] = "Medium"  # Default value
            
        if 'GLOBAL_CELEBRATIONS' not in df_copy.columns:
            df_copy['GLOBAL_CELEBRATIONS'] = "10+ countries"  # Default value
            
        if 'ENVIRONMENTAL_IMPACT' not in df_copy.columns:
            df_copy['ENVIRONMENTAL_IMPACT'] = "Moderate"  # Default value
            
        if 'DURATION_DAYS' not in df_copy.columns:
            df_copy['DURATION_DAYS'] = 1  # Default value
    
    elif 'religions.csv' in csv_path.lower():
        if 'CULTURAL_CONTRIBUTIONS' not in df_copy.columns:
            df_copy['CULTURAL_CONTRIBUTIONS'] = "Various cultural contributions"
            
        if 'UNIQUE_PRACTICES' not in df_copy.columns:
            df_copy['UNIQUE_PRACTICES'] = "Various religious practices"
            
        if 'HISTORICAL_SIGNIFICANCE' not in df_copy.columns:
            df_copy['HISTORICAL_SIGNIFICANCE'] = "Significant historical impact"
    
    return df_copy

def create_tables(conn):
    """Create tables for CSV data"""
    try:
        cursor = conn.cursor()
        
        # List of CSV files and their table names
        csv_tables = [
            ("LANGUAGES", "data/languages.csv"),
            ("RELIGIONS", "data/religions.csv"),
            ("STATES", "data/states.csv"),
            ("CULTURAL_HERITAGE", "data/cultural_heritage.csv"),
            ("POPULATION_GROWTH", "data/population_growth.csv"),
            ("ECONOMIC_SECTORS", "data/economic_sectors.csv"),
            ("HISTORICAL_TIMELINE", "data/historical_timeline.csv"),
            ("FESTIVALS", "data/festivals.csv"),
            ("TOURISM", "data/tourism.csv"),
            ("EDUCATION", "data/education.csv"),
            ("GEOGRAPHY", "data/geography.csv")
        ]
        
        # Create image table for storing images
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS IMAGES (
            IMAGE_ID NUMBER AUTOINCREMENT,
            IMAGE_NAME VARCHAR(255) NOT NULL UNIQUE,
            IMAGE_TYPE VARCHAR(10) NOT NULL,
            IMAGE_DATA BINARY,
            UPLOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (IMAGE_ID)
        )
        """)
        print("✅ IMAGES table created or already exists")
        
        for table_name, csv_path in csv_tables:
            # Read CSV to get column names and types
            try:
                df = pd.read_csv(csv_path)
                
                # Standardize column names and add missing columns
                df = standardize_column_names(df, csv_path)
                
                # Start creating table SQL
                create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
                
                # Add columns with appropriate types
                columns = []
                for col in df.columns:
                    # Clean and uppercase the column name
                    col_name = col.upper().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "PCT")
                    col_name = col_name.replace("/", "_").replace(",", "_").replace("-", "_")
                    
                    # Determine column type based on data
                    if df[col].dtype == 'int64':
                        col_type = "NUMBER"
                    elif df[col].dtype == 'float64':
                        col_type = "FLOAT"
                    else:
                        col_type = "VARCHAR(1000)"
                    
                    columns.append(f"{col_name} {col_type}")
                
                create_table_sql += ",\n".join(columns)
                create_table_sql += "\n)"
                
                # Execute table creation
                cursor.execute(create_table_sql)
                print(f"✅ Table {table_name} created or already exists")
                
            except Exception as e:
                print(f"❌ Error creating table {table_name}: {str(e)}")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

def upload_csv_data(conn):
    """Upload CSV data to Snowflake tables"""
    try:
        # List of CSV files and their table names
        csv_tables = [
            ("LANGUAGES", "data/languages.csv"),
            ("RELIGIONS", "data/religions.csv"),
            ("STATES", "data/states.csv"),
            ("CULTURAL_HERITAGE", "data/cultural_heritage.csv"),
            ("POPULATION_GROWTH", "data/population_growth.csv"),
            ("ECONOMIC_SECTORS", "data/economic_sectors.csv"),
            ("HISTORICAL_TIMELINE", "data/historical_timeline.csv"),
            ("FESTIVALS", "data/festivals.csv"),
            ("TOURISM", "data/tourism.csv"),
            ("EDUCATION", "data/education.csv"),
            ("GEOGRAPHY", "data/geography.csv")
        ]
        
        cursor = conn.cursor()
        
        for table_name, csv_path in csv_tables:
            try:
                # First, truncate the table to avoid duplicates
                cursor.execute(f"TRUNCATE TABLE IF EXISTS {table_name}")
                
                # Read CSV data
                df = pd.read_csv(csv_path)
                
                # Standardize column names and add missing columns
                df = standardize_column_names(df, csv_path)
                
                # Clean column names - must match exactly what was done in create_tables
                df.columns = [col.upper().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "PCT").replace("/", "_").replace(",", "_").replace("-", "_") for col in df.columns]
                
                # Write data to Snowflake
                success, num_chunks, num_rows, output = write_pandas(
                    conn=conn,
                    df=df,
                    table_name=table_name,
                    database=DATABASE_NAME,
                    schema=SCHEMA_NAME
                )
                
                if success:
                    print(f"✅ Uploaded {num_rows} rows to {table_name}")
                else:
                    print(f"❌ Failed to upload data to {table_name}")
                
            except Exception as e:
                print(f"❌ Error uploading data to {table_name}: {str(e)}")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error uploading CSV data: {str(e)}")
        return False

def upload_images(conn):
    """Upload images to Snowflake"""
    try:
        cursor = conn.cursor()
        
        # List of image files and their names
        images = [
            ("emblem.png", "data/images/emblem.png", "PNG"),
            ("flambeau.svg", "data/images/flambeau.svg", "SVG"),
            ("tajmahal.svg", "data/images/tajmahal.svg", "SVG")
        ]
        
        for image_name, image_path, image_type in images:
            try:
                # Check if image already exists
                cursor.execute(f"SELECT COUNT(*) FROM IMAGES WHERE IMAGE_NAME = '{image_name}'")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    # Delete existing image
                    cursor.execute(f"DELETE FROM IMAGES WHERE IMAGE_NAME = '{image_name}'")
                
                # Read image data
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                
                # Insert image data
                cursor.execute(
                    "INSERT INTO IMAGES (IMAGE_NAME, IMAGE_TYPE, IMAGE_DATA) VALUES (%s, %s, %s)",
                    (image_name, image_type, image_data)
                )
                
                print(f"✅ Uploaded image {image_name}")
                
            except Exception as e:
                print(f"❌ Error uploading image {image_name}: {str(e)}")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error uploading images: {str(e)}")
        return False

def alter_tables(conn):
    """Add missing columns to existing tables for consistency"""
    try:
        cursor = conn.cursor()
        
        # Add missing columns for STATES table
        cursor.execute("SHOW COLUMNS IN TABLE STATES")
        existing_columns = [row[2] for row in cursor.fetchall()]
        
        if 'HDI' not in existing_columns:
            cursor.execute("ALTER TABLE STATES ADD COLUMN HDI FLOAT")
            print("Added HDI column to STATES table")
        
        # Add missing columns for CULTURAL_HERITAGE table
        cursor.execute("SHOW COLUMNS IN TABLE CULTURAL_HERITAGE")
        existing_columns = [row[2] for row in cursor.fetchall()]
        
        if 'UNESCO_STATUS' not in existing_columns:
            cursor.execute("ALTER TABLE CULTURAL_HERITAGE ADD COLUMN UNESCO_STATUS VARCHAR(100)")
            print("Added UNESCO_STATUS column to CULTURAL_HERITAGE table")
        
        if 'CULTURAL_CONTRIBUTIONS' not in existing_columns:
            cursor.execute("ALTER TABLE CULTURAL_HERITAGE ADD COLUMN CULTURAL_CONTRIBUTIONS VARCHAR(500)")
            print("Added CULTURAL_CONTRIBUTIONS column to CULTURAL_HERITAGE table")
        
        # Add missing columns for POPULATION_GROWTH table
        cursor.execute("SHOW COLUMNS IN TABLE POPULATION_GROWTH")
        existing_columns = [row[2] for row in cursor.fetchall()]
        
        if 'URBAN_POPULATION_PCT' not in existing_columns:
            cursor.execute("ALTER TABLE POPULATION_GROWTH ADD COLUMN URBAN_POPULATION_PCT FLOAT")
            print("Added URBAN_POPULATION_PCT column to POPULATION_GROWTH table")
        
        if 'RURAL_POPULATION_PCT' not in existing_columns:
            cursor.execute("ALTER TABLE POPULATION_GROWTH ADD COLUMN RURAL_POPULATION_PCT FLOAT")
            print("Added RURAL_POPULATION_PCT column to POPULATION_GROWTH table")
        
        if 'AGE_0_14_PCT' not in existing_columns:
            cursor.execute("ALTER TABLE POPULATION_GROWTH ADD COLUMN AGE_0_14_PCT FLOAT")
            print("Added AGE_0_14_PCT column to POPULATION_GROWTH table")
        
        if 'AGE_15_64_PCT' not in existing_columns:
            cursor.execute("ALTER TABLE POPULATION_GROWTH ADD COLUMN AGE_15_64_PCT FLOAT")
            print("Added AGE_15_64_PCT column to POPULATION_GROWTH table")
        
        if 'AGE_65_PLUS_PCT' not in existing_columns:
            cursor.execute("ALTER TABLE POPULATION_GROWTH ADD COLUMN AGE_65_PLUS_PCT FLOAT")
            print("Added AGE_65_PLUS_PCT column to POPULATION_GROWTH table")
        
        # Add missing columns for FESTIVALS table
        cursor.execute("SHOW COLUMNS IN TABLE FESTIVALS")
        existing_columns = [row[2] for row in cursor.fetchall()]
        
        if 'RELIGION_TYPE' not in existing_columns:
            cursor.execute("ALTER TABLE FESTIVALS ADD COLUMN RELIGION_TYPE VARCHAR(50)")
            print("Added RELIGION_TYPE column to FESTIVALS table")
        
        if 'ENVIRONMENTAL_IMPACT' not in existing_columns:
            cursor.execute("ALTER TABLE FESTIVALS ADD COLUMN ENVIRONMENTAL_IMPACT VARCHAR(100)")
            print("Added ENVIRONMENTAL_IMPACT column to FESTIVALS table")
        
        if 'ECONOMIC_IMPACT_MILLIONS_USD' not in existing_columns:
            cursor.execute("ALTER TABLE FESTIVALS ADD COLUMN ECONOMIC_IMPACT_MILLIONS_USD FLOAT")
            print("Added ECONOMIC_IMPACT_MILLIONS_USD column to FESTIVALS table")
        else:
            # Ensure the column is FLOAT type
            cursor.execute("ALTER TABLE FESTIVALS MODIFY COLUMN ECONOMIC_IMPACT_MILLIONS_USD FLOAT")
            print("Modified ECONOMIC_IMPACT_MILLIONS_USD column to FLOAT type")
        
        if 'PARTICIPANTS_MILLIONS' not in existing_columns:
            cursor.execute("ALTER TABLE FESTIVALS ADD COLUMN PARTICIPANTS_MILLIONS FLOAT")
            print("Added PARTICIPANTS_MILLIONS column to FESTIVALS table")
        else:
            # Ensure the column is FLOAT type
            cursor.execute("ALTER TABLE FESTIVALS MODIFY COLUMN PARTICIPANTS_MILLIONS FLOAT")
            print("Modified PARTICIPANTS_MILLIONS column to FLOAT type")
        
        if 'DURATION_DAYS' not in existing_columns:
            cursor.execute("ALTER TABLE FESTIVALS ADD COLUMN DURATION_DAYS INT")
            print("Added DURATION_DAYS column to FESTIVALS table")
        else:
            # Ensure the column is INT type
            cursor.execute("ALTER TABLE FESTIVALS MODIFY COLUMN DURATION_DAYS INT")
            print("Modified DURATION_DAYS column to INT type")
        
        if 'GLOBAL_CELEBRATIONS' not in existing_columns:
            cursor.execute("ALTER TABLE FESTIVALS ADD COLUMN GLOBAL_CELEBRATIONS VARCHAR(100)")
            print("Added GLOBAL_CELEBRATIONS column to FESTIVALS table")
            
        # Add missing columns for TOURISM table
        cursor.execute("SHOW COLUMNS IN TABLE TOURISM")
        existing_columns = [row[2] for row in cursor.fetchall()]
        
        if 'DOMESTIC_TOURISM_MILLIONS' not in existing_columns:
            cursor.execute("ALTER TABLE TOURISM ADD COLUMN DOMESTIC_TOURISM_MILLIONS FLOAT")
            print("Added DOMESTIC_TOURISM_MILLIONS column to TOURISM table")
        
        if 'FOREIGN_TOURISM_MILLIONS' not in existing_columns:
            cursor.execute("ALTER TABLE TOURISM ADD COLUMN FOREIGN_TOURISM_MILLIONS FLOAT")
            print("Added FOREIGN_TOURISM_MILLIONS column to TOURISM table")
        
        if 'TOURISM_REVENUE_BILLION_USD' not in existing_columns:
            cursor.execute("ALTER TABLE TOURISM ADD COLUMN TOURISM_REVENUE_BILLION_USD FLOAT")
            print("Added TOURISM_REVENUE_BILLION_USD column to TOURISM table")
        
        # Update SNOWFLAKE_ERROR_FIXES.md file to document changes
        try:
            with open('SNOWFLAKE_ERROR_FIXES.md', 'a') as f:
                f.write("\n\n## Column Type Fixes (Added on Update)\n\n")
                f.write("Fixed the data types for the following columns in Snowflake:\n\n")
                f.write("- `ECONOMIC_IMPACT_MILLIONS_USD` changed to FLOAT type\n")
                f.write("- `PARTICIPANTS_MILLIONS` changed to FLOAT type\n")
                f.write("- `DURATION_DAYS` changed to INT type\n")
                f.write("\nThese changes ensure that numeric calculations work correctly in visualizations.")
            print("Updated SNOWFLAKE_ERROR_FIXES.md with data type changes")
        except Exception as e:
            print(f"Warning: Could not update SNOWFLAKE_ERROR_FIXES.md: {str(e)}")
        
        # Commit the changes
        conn.commit()
        print("✅ Successfully altered tables to add missing columns")
    except Exception as e:
        print(f"❌ Error altering tables: {str(e)}")
        conn.rollback()

def main():
    """Main function to set up Snowflake and upload data"""
    print("🚀 Starting Snowflake setup...")
    
    if not SNOWFLAKE_ACCOUNT or not SNOWFLAKE_USER or not SNOWFLAKE_PASSWORD:
        print("❌ Snowflake credentials not provided. Please set environment variables or update the script.")
        sys.exit(1)
    
    # Create connection
    conn = create_connection()
    
    # Setup database and schema
    if setup_database(conn):
        # Create tables
        if create_tables(conn):
            # Alter tables to add missing columns
            alter_tables(conn)
            
            # Upload CSV data
            upload_csv_data(conn)
            
            # Upload images
            upload_images(conn)
    
    # Close connection
    conn.close()
    print("✅ Snowflake setup completed!")

if __name__ == "__main__":
    main() 
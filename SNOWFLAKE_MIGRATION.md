# Snowflake Migration Guide

## Overview

We've successfully migrated the application data from local files to Snowflake Cloud! This enhances our application in several ways:

1. **Centralized Data Storage**: All data is now stored in Snowflake, making it accessible from anywhere
2. **Improved Scalability**: Snowflake can handle much larger datasets efficiently
3. **Better Collaboration**: Multiple team members can access and update the data
4. **Enhanced Security**: Data is securely stored with proper access controls

## Current Setup

The application is configured to:

1. First try to fetch data from Snowflake Cloud
2. Fall back to local CSV files if the Snowflake connection fails
3. Use the same data schema regardless of the source

## Recent Updates

We've made several important updates to improve data consistency and error handling:

1. **Column Standardization**: Added missing columns to Snowflake tables (HDI, UNESCO Status, Urban/Rural population)
2. **Error Handling**: Improved error tracking and graceful fallback to local files
3. **Data Validation**: Added validation for required columns with appropriate warnings
4. **Testing**: Enhanced test scripts to verify data integrity

For details on error fixes, see `SNOWFLAKE_ERROR_FIXES.md`.

## How to Use

### Running the Application

Simply run the application as before:

```bash
streamlit run app.py
```

The application will automatically connect to Snowflake using the credentials in `.streamlit/secrets.toml`.

### Troubleshooting

If you encounter any issues with Snowflake connectivity:

1. Check your Snowflake credentials in `.streamlit/secrets.toml`
2. Run the test script to verify the connection: `python test_snowflake.py`
3. If errors persist, the application will automatically fall back to local files

## Tables in Snowflake

The following tables have been created in Snowflake:

- `LANGUAGES`
- `RELIGIONS`
- `STATES` (with HDI column)
- `CULTURAL_HERITAGE` (with UNESCO_STATUS column)
- `POPULATION_GROWTH` (with urban/rural percentages)
- `ECONOMIC_SECTORS`
- `HISTORICAL_TIMELINE`
- `FESTIVALS`
- `TOURISM`
- `EDUCATION`
- `GEOGRAPHY`
- `IMAGES` (for storing image files)

## Technical Details

### Modified Files

- `snowflake_setup.py`: Script to set up Snowflake database and upload data
- `modules/snowflake_connector.py`: Module to handle Snowflake connections
- `modules/utils.py`: Updated data loading functions to use Snowflake
- `.streamlit/secrets.toml`: Configuration file for Snowflake credentials
- `test_snowflake.py`: Script to test Snowflake connectivity and data

### Error Handling

The application implements robust error handling:

1. Tracks Snowflake errors in the session state
2. Automatically falls back to local files if too many errors occur
3. Provides helpful error messages to users

## For Developers

### Adding New Data

To add new data to Snowflake:

1. Add your CSV file to the `data` directory
2. Update the `snowflake_setup.py` script to include your new table
3. Run the setup script to create the table and upload data
4. Update the relevant data loading function in `modules/utils.py`

### Testing Snowflake Connection

Use the provided test script to verify the Snowflake connection:

```bash
python test_snowflake.py
```

This will show all available tables and confirm that the connection is working properly, as well as verify that all required columns exist. 
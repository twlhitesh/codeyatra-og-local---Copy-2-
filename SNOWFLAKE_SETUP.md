
# Snowflake Integration Setup Guide

This guide will help you migrate your local data to Snowflake Cloud and connect your Streamlit application to it.

## Prerequisites

- A Snowflake account with appropriate permissions (ACCOUNTADMIN role or similar)
- Python 3.8+ installed on your local machine
- Required Python packages installed (`snowflake-connector-python` and `snowflake-snowpark-python`)

## Step 1: Set Up Snowflake Credentials

1. Set up your Snowflake credentials as environment variables:

```bash
export SNOWFLAKE_ACCOUNT="your-account-identifier"
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password"
export SNOWFLAKE_ROLE="ACCOUNTADMIN"  # or your preferred role
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"  # or your preferred warehouse
```

Alternatively, you can directly edit the `snowflake_setup.py` script and add your credentials there.

## Step 2: Run the Setup Script

Run the setup script to create the database, tables, and upload data to Snowflake:

```bash
python snowflake_setup.py
```

This script will:
- Create a database named `INDIA_DATA`
- Create tables for all CSV files in the `data` directory
- Create a table for storing images
- Upload all CSV data to the corresponding tables
- Upload images to the `IMAGES` table

## Step 3: Configure Streamlit Secrets

1. Copy the secrets template:

```bash
cp .streamlit/secrets_template.toml .streamlit/secrets.toml
```

2. Edit `.streamlit/secrets.toml` to add your Snowflake credentials:

```toml
[snowflake]
account = "your-snowflake-account"
user = "your-snowflake-username"
password = "your-snowflake-password"
role = "ACCOUNTADMIN"  # or your preferred role
warehouse = "COMPUTE_WH"  # or your preferred warehouse
database = "INDIA_DATA"
schema = "PUBLIC"
```

## Step 4: Run Your Streamlit App

Now that everything is set up, you can run your Streamlit app, which will automatically use Snowflake data:

```bash
streamlit run app.py
```

## How It Works

The application has been modified to:

1. First attempt to fetch data from Snowflake
2. Fall back to local CSV files if the Snowflake connection fails
3. Use the same data schema regardless of the source

This ensures smooth operation even if there are temporary issues with Snowflake connectivity.

## Data in Snowflake

The following tables are created in Snowflake:

- `LANGUAGES`
- `RELIGIONS`
- `STATES`
- `CULTURAL_HERITAGE`
- `POPULATION_GROWTH`
- `ECONOMIC_SECTORS`
- `HISTORICAL_TIMELINE`
- `FESTIVALS`
- `TOURISM`
- `EDUCATION`
- `GEOGRAPHY`
- `IMAGES` (for storing image files)

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Verify your Snowflake credentials
2. Check that your Snowflake account is active
3. Ensure your IP address is allowed to connect to Snowflake

### Data Loading Issues

If you encounter data loading issues:

1. Check the Snowflake web interface to verify tables were created correctly
2. Verify that data was uploaded successfully
3. Check error messages in the Streamlit app for specific issues

### Image Loading Issues

If images don't display:

1. Verify that images were uploaded to the `IMAGES` table in Snowflake
2. Check the image names match what the application is looking for 
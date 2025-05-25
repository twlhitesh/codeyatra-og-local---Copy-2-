import streamlit as st
from snowflake.connector import connect
from snowflake.snowpark.session import Session
import pandas as pd
import os
from io import BytesIO
from PIL import Image
import base64

# Caching Snowflake session to avoid multiple connections
@st.cache_resource
def get_snowflake_session():
    """Create and return a Snowflake session"""
    try:
        # Get credentials from Streamlit secrets
        snowflake_credentials = st.secrets["snowflake"]
        
        # Create a Snowflake session
        session = Session.builder.configs({
            "account": snowflake_credentials["account"],
            "user": snowflake_credentials["user"],
            "password": snowflake_credentials["password"],
            "role": snowflake_credentials["role"],
            "warehouse": snowflake_credentials["warehouse"],
            "database": snowflake_credentials["database"],
            "schema": snowflake_credentials["schema"]
        }).create()
        
        return session
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        raise e

# Function to get a direct connector for specific operations
@st.cache_resource
def get_snowflake_connector():
    """Create and return a Snowflake connector"""
    try:
        # Get credentials from Streamlit secrets
        snowflake_credentials = st.secrets["snowflake"]
        
        # Create a Snowflake connector
        conn = connect(
            account=snowflake_credentials["account"],
            user=snowflake_credentials["user"],
            password=snowflake_credentials["password"],
            role=snowflake_credentials["role"],
            warehouse=snowflake_credentials["warehouse"],
            database=snowflake_credentials["database"],
            schema=snowflake_credentials["schema"]
        )
        
        return conn
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        raise e

# Function to query Snowflake and return a pandas DataFrame
@st.cache_data
def query_snowflake(query):
    """Execute a query on Snowflake and return results as a DataFrame"""
    # Skip Snowflake if disabled
    if not st.session_state.get('use_snowflake', True):
        return None
        
    try:
        session = get_snowflake_session()
        df = session.sql(query).to_pandas()
        return df
    except Exception as e:
        # Track errors
        if 'snowflake_errors' in st.session_state:
            st.session_state.snowflake_errors += 1
        print(f"Error querying Snowflake: {str(e)}")
        return None

# Function to get image from Snowflake
@st.cache_data
def get_image_from_snowflake(image_name):
    """Retrieve an image from Snowflake storage"""
    # Skip Snowflake if disabled
    if not st.session_state.get('use_snowflake', True):
        return None
        
    try:
        # Query to get the image data
        query = f"SELECT IMAGE_DATA FROM IMAGES WHERE IMAGE_NAME = '{image_name}'"
        session = get_snowflake_session()
        result = session.sql(query).collect()
        
        if result and len(result) > 0:
            # Get the image data
            image_data = result[0]["IMAGE_DATA"]
            
            # Convert binary data to Image
            img = Image.open(BytesIO(image_data))
            return img
        else:
            print(f"Image {image_name} not found in Snowflake")
            return None
    except Exception as e:
        # Track errors
        if 'snowflake_errors' in st.session_state:
            st.session_state.snowflake_errors += 1
        print(f"Error retrieving image from Snowflake: {str(e)}")
        return None

# Function to get SVG from Snowflake as base64
@st.cache_data
def get_svg_from_snowflake(svg_name):
    """Retrieve an SVG from Snowflake and return as base64 data URL"""
    # Skip Snowflake if disabled
    if not st.session_state.get('use_snowflake', True):
        return None
        
    try:
        # Query to get the SVG data
        query = f"SELECT IMAGE_DATA FROM IMAGES WHERE IMAGE_NAME = '{svg_name}'"
        session = get_snowflake_session()
        result = session.sql(query).collect()
        
        if result and len(result) > 0:
            # Get the SVG data
            svg_data = result[0]["IMAGE_DATA"]
            
            # Convert to base64
            b64 = base64.b64encode(svg_data).decode("utf-8")
            return f"data:image/svg+xml;base64,{b64}"
        else:
            print(f"SVG {svg_name} not found in Snowflake")
            return None
    except Exception as e:
        # Track errors
        if 'snowflake_errors' in st.session_state:
            st.session_state.snowflake_errors += 1
        print(f"Error retrieving SVG from Snowflake: {str(e)}")
        return None 
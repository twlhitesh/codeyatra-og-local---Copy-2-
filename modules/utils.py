import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
import requests
from io import BytesIO
import re
import numpy as np
from modules.snowflake_connector import query_snowflake, get_image_from_snowflake, get_svg_from_snowflake

# Function to style Matplotlib figures for dark theme
def style_matplotlib_for_dark(fig, ax):
    # Set figure facecolor
    fig.patch.set_facecolor('#1E2129')
    
    # Set axes facecolor
    ax.set_facecolor('#0E1117')
    
    # Set grid color
    ax.grid(True, linestyle='--', alpha=0.3, color='#CCCCCC')
    
    # Set spine colors
    for spine in ax.spines.values():
        spine.set_color('#555555')
    
    # Set title and label colors
    ax.title.set_color('#FF9933')
    ax.xaxis.label.set_color('#FAFAFA')
    ax.yaxis.label.set_color('#FAFAFA')
    
    # Set tick colors
    ax.tick_params(axis='x', colors='#FAFAFA')
    ax.tick_params(axis='y', colors='#FAFAFA')
    
    return fig, ax

# Function to apply consistent dark mode styling to Plotly charts
def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(30, 33, 41, 0.7)',
        paper_bgcolor='rgba(30, 33, 41, 0.0)',
        font_color='#FAFAFA',
        title_font_color='#FF9933',
        legend_title_font_color='#FAFAFA',
        legend_font_color='#FAFAFA',
        hoverlabel=dict(
            bgcolor='#1E2129',
            font_color='white',
            font_size=14
        )
    )
    # Add grid lines for better readability
    if 'xaxis' in fig.layout:
        fig.update_xaxes(
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='rgba(255, 255, 255, 0.2)'
        )
    if 'yaxis' in fig.layout:
        fig.update_yaxes(
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='rgba(255, 255, 255, 0.2)'
        )
    return fig

# Function to preload common datasets to avoid redundancy
@st.cache_data
def preload_data(datasets=None):
    """
    Preload and cache datasets for faster access across different chapters
    
    Args:
        datasets (list): List of dataset names to load. If None, loads all datasets.
                        Options: 'linguistic', 'religious', 'state', 'cultural', 
                                'population', 'economic', 'historical', 'festivals',
                                'tourism', 'education', 'geography'
    
    Returns:
        dict: Dictionary containing all loaded datasets
    """
    all_datasets = [
        'linguistic', 'religious', 'state', 'cultural', 'population', 
        'economic', 'historical', 'festivals', 'tourism', 'education', 'geography'
    ]
    
    # If no specific datasets are requested, load all of them
    if datasets is None:
        datasets = all_datasets
    
    # Initialize data container
    data = {}
    
    # Load requested datasets
    with st.spinner("Preloading data for faster navigation..."):
        for dataset in datasets:
            if dataset == 'linguistic':
                data['linguistic'] = load_linguistic_data()
            elif dataset == 'religious':
                data['religious'] = load_religious_data()
            elif dataset == 'state':
                data['state'] = load_state_data()
            elif dataset == 'cultural':
                data['cultural'] = load_cultural_data()
            elif dataset == 'population':
                data['population'] = load_population_data()
            elif dataset == 'economic':
                data['economic'] = load_economic_data()
            elif dataset == 'historical':
                data['historical'] = load_historical_data()
            elif dataset == 'festivals':
                data['festivals'] = load_festivals_data()
            elif dataset == 'tourism':
                data['tourism'] = load_tourism_data()
            elif dataset == 'education':
                data['education'] = load_education_data()
            elif dataset == 'geography':
                data['geography'] = load_geography_data()
    
    return data

# Function to load image from URL with caching
@st.cache_data
def load_image_from_url(url):
    try:
        with st.spinner(f"Loading image..."):
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Function to load local SVG image as base64 data URL
@st.cache_data
def load_svg_as_base64(file_path):
    """Load an SVG file and return it as a base64 data URL for embedding in HTML"""
    try:
        # First try to get from Snowflake
        svg_name = os.path.basename(file_path)
        svg_data = get_svg_from_snowflake(svg_name)
        if svg_data:
            return svg_data
            
        # If not found in Snowflake, fall back to local file
        full_path = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(full_path):
            st.error(f"SVG file not found: {full_path}")
            return None
            
        import base64
        with open(full_path, "rb") as f:
            svg_data = f.read()
            b64 = base64.b64encode(svg_data).decode("utf-8")
            return f"data:image/svg+xml;base64,{b64}"
    except Exception as e:
        st.error(f"Error loading SVG: {e}")
        return None

# Helper function to safely read CSV files with various encodings
def safe_read_csv(file_path):
    """Safely read a CSV file with encoding fallbacks"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            st.error(f"Error reading file {file_path}: {str(e)}")
            return None
    
    st.error(f"Failed to read {file_path} with any encoding.")
    return None

# Improved data loading functions with better error handling
@st.cache_data
def load_linguistic_data():
    try:
        with st.spinner("Loading linguistic data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM LANGUAGES"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Convert all columns to expected format
                    column_map = {}
                    for col in df.columns:
                        # Map to expected column names (case-sensitive)
                        if col == 'LANGUAGE':
                            column_map[col] = 'Language'
                        elif col == 'SPEAKERS':
                            column_map[col] = 'Speakers'
                        elif col == 'PERCENTAGE':
                            column_map[col] = 'Percentage'
                        elif col == 'UNESCO_STATUS':
                            column_map[col] = 'UNESCO Status'
                        elif col == 'ANCIENT_TEXTS':
                            column_map[col] = 'Ancient Texts'
                        elif col == 'CULTURAL_SIGNIFICANCE':
                            column_map[col] = 'Cultural Significance'
                        elif col == 'GLOBAL_REACH':
                            column_map[col] = 'Global Reach'
                    
                    # Only rename columns that exist in the mapping
                    if column_map:
                        df = df.rename(columns=column_map)
                    
                    # Add UNESCO Status if missing
                    if 'UNESCO Status' not in df.columns:
                        df['UNESCO Status'] = "Not Listed"
                        # Add Classical status for known classical languages
                        classical_languages = ['Sanskrit', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Odia']
                        df.loc[df['Language'].isin(classical_languages), 'UNESCO Status'] = "Classical Language"
                    
                    # Add other required columns with default values if missing
                    if 'Ancient Texts' not in df.columns:
                        df['Ancient Texts'] = "Various ancient literary works"
                    
                    if 'Cultural Significance' not in df.columns:
                        df['Cultural Significance'] = "Significant cultural contributions"
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/languages.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Add UNESCO Status if missing
            if 'UNESCO Status' not in df.columns:
                df['UNESCO Status'] = "Not Listed"
                # Add Classical status for known classical languages
                classical_languages = ['Sanskrit', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Odia']
                df.loc[df['Language'].isin(classical_languages), 'UNESCO Status'] = "Classical Language"
            
            # Add other required columns with default values if missing
            if 'Ancient Texts' not in df.columns:
                df['Ancient Texts'] = "Various ancient literary works"
            
            if 'Cultural Significance' not in df.columns:
                df['Cultural Significance'] = "Significant cultural contributions"
            
            return df
    except Exception as e:
        st.error(f"Error loading linguistic data: {e}")
        # Return minimal valid dataframe to prevent app crashes
        return pd.DataFrame({
            'Language': ['Hindi', 'Bengali', 'Telugu', 'Marathi', 'Tamil', 'Urdu', 'Kannada', 'Gujarati', 'Malayalam', 'Sanskrit'],
            'Speakers': [600, 90, 80, 70, 60, 50, 40, 45, 35, 0.01],
            'Percentage': [43.6, 8.0, 6.9, 7.5, 5.9, 5.0, 3.7, 4.6, 2.9, 0.01],
            'UNESCO Status': ['Official Language', 'Official Language', 'Classical Language', 'Official Language', 'Classical Language', 'Official Language', 'Classical Language', 'Official Language', 'Classical Language', 'Classical Language'],
            'Ancient Texts': ['Various texts', 'Various texts', 'Various texts', 'Various texts', 'Sangam literature', 'Various texts', 'Various texts', 'Various texts', 'Various texts', 'Vedas, Upanishads'],
            'Cultural Significance': ['National language', 'Literature rich', 'Cinema, literature', 'Literature rich', 'Ancient literature', 'Poetry, ghazals', 'Literature rich', 'Literature rich', 'Literature rich', 'Religious texts']
        })

@st.cache_data
def load_religious_data():
    try:
        with st.spinner("Loading religious data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM RELIGIONS"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Convert all columns to expected format
                    column_map = {}
                    for col in df.columns:
                        # Map to expected column names (case-sensitive)
                        if col == 'RELIGION':
                            column_map[col] = 'Religion'
                        elif col == 'PERCENTAGE':
                            column_map[col] = 'Percentage'
                        elif col == 'POPULATION':
                            column_map[col] = 'Population'
                    
                    # Only rename columns that exist in the mapping
                    if column_map:
                        df = df.rename(columns=column_map)
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/religions.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Religion', 'Percentage', 'Population']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in religious data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Religion':
                        df[col] = [f"Religion {i+1}" for i in range(len(df))]
                    elif col == 'Percentage':
                        df[col] = 0.0
                    elif col == 'Population':
                        df[col] = 0
            
            return df
    except Exception as e:
        st.error(f"Error loading religious data: {e}")
        return None

@st.cache_data
def load_state_data():
    try:
        with st.spinner("Loading state data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM STATES"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Rename columns to match expected format if needed
                    column_mapping = {
                        'STATE': 'State',
                        'POPULATION_MILLIONS': 'Population (millions)',
                        'AREA_SQ_KM': 'Area (sq km)',
                        'LITERACY_RATE_PCT': 'Literacy Rate (%)',
                        'REGION': 'Region',
                        'CAPITAL': 'Capital',
                        'OFFICIAL_LANGUAGES': 'Official Languages',
                        'MAJOR_INDUSTRIES': 'Major Industries',
                        'GDP_BILLION_USD': 'GDP (billion USD)',
                        'HDI': 'HDI',
                        'URBANIZATION_PCT': 'Urbanization (%)',
                        'FAMOUS_DESTINATIONS': 'Famous Destinations',
                        'MAJOR_CROPS': 'Major Crops',
                        'KEY_INDUSTRIES': 'Key Industries'
                    }
                    
                    # Only rename columns that exist
                    rename_cols = {}
                    for snowflake_col, app_col in column_mapping.items():
                        if snowflake_col in df.columns:
                            rename_cols[snowflake_col] = app_col
                    
                    if rename_cols:
                        df = df.rename(columns=rename_cols)
                    
                    # Add HDI column if it doesn't exist
                    if 'HDI' not in df.columns:
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
                        df['HDI'] = df['State'].map(lambda x: hdi_values.get(x, 0.65))  # Default to 0.65 if state not found
                    
                    # Add Urbanization column if it doesn't exist
                    if 'Urbanization (%)' not in df.columns:
                        # Default urbanization data (approximations)
                        urbanization_values = {
                            'Delhi': 97.5,
                            'Chandigarh': 97.3,
                            'Goa': 62.2,
                            'Mizoram': 52.1,
                            'Tamil Nadu': 48.4,
                            'Kerala': 47.7,
                            'Maharashtra': 45.2,
                            'Gujarat': 42.6,
                            'Karnataka': 38.6,
                            'Punjab': 37.5,
                            'Haryana': 34.8,
                            'Andhra Pradesh': 29.6,
                            'West Bengal': 31.9,
                            'Uttarakhand': 30.6,
                            'Rajasthan': 24.9,
                            'Uttar Pradesh': 22.3,
                            'Jharkhand': 24.1,
                            'Chhattisgarh': 23.2,
                            'Madhya Pradesh': 27.6,
                            'Odisha': 16.7,
                            'Bihar': 11.3,
                            'Assam': 14.1,
                            'Himachal Pradesh': 10.0,
                            'Jammu and Kashmir': 27.4
                        }
                        
                        # Apply urbanization values based on state name
                        df['Urbanization (%)'] = df['State'].map(lambda x: urbanization_values.get(x, 30.0))  # Default to 30% if state not found
                    
                    # Add other missing columns
                    required_columns = ['Famous Destinations', 'Major Crops', 'Key Industries']
                    for col in required_columns:
                        if col not in df.columns:
                            df[col] = f"Various {col.lower()}"
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/states.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['State', 'Population (millions)', 'Area (sq km)', 'Literacy Rate (%)', 'Region']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in state data: {', '.join(missing_columns)}")
            
            # Add HDI column if it doesn't exist
            if 'HDI' not in df.columns:
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
                df['HDI'] = df['State'].map(lambda x: hdi_values.get(x, 0.65))  # Default to 0.65 if state not found
            
            # Add Urbanization column if it doesn't exist
            if 'Urbanization (%)' not in df.columns:
                # Default urbanization data (approximations)
                urbanization_values = {
                    'Delhi': 97.5,
                    'Chandigarh': 97.3,
                    'Goa': 62.2,
                    'Mizoram': 52.1,
                    'Tamil Nadu': 48.4,
                    'Kerala': 47.7,
                    'Maharashtra': 45.2,
                    'Gujarat': 42.6,
                    'Karnataka': 38.6,
                    'Punjab': 37.5,
                    'Haryana': 34.8,
                    'Andhra Pradesh': 29.6,
                    'West Bengal': 31.9,
                    'Uttarakhand': 30.6,
                    'Rajasthan': 24.9,
                    'Uttar Pradesh': 22.3,
                    'Jharkhand': 24.1,
                    'Chhattisgarh': 23.2,
                    'Madhya Pradesh': 27.6,
                    'Odisha': 16.7,
                    'Bihar': 11.3,
                    'Assam': 14.1,
                    'Himachal Pradesh': 10.0,
                    'Jammu and Kashmir': 27.4
                }
                
                # Apply urbanization values based on state name
                df['Urbanization (%)'] = df['State'].map(lambda x: urbanization_values.get(x, 30.0))  # Default to 30% if state not found
                
            # Add other missing columns
            additional_columns = ['Famous Destinations', 'Major Crops', 'Key Industries']
            for col in additional_columns:
                if col not in df.columns:
                    df[col] = f"Various {col.lower()}"
                
            return df
    except Exception as e:
        st.error(f"Error loading state data: {e}")
        # Return minimal valid dataframe to prevent app crashes
        return pd.DataFrame({
            'State': ['Kerala', 'Maharashtra', 'Tamil Nadu', 'Uttar Pradesh', 'Bihar'],
            'Population (millions)': [35.1, 112.4, 72.1, 199.8, 104.1],
            'Area (sq km)': [38863, 307713, 130058, 240928, 94163],
            'Literacy Rate (%)': [94.0, 82.3, 80.1, 67.7, 61.8],
            'HDI': [0.782, 0.696, 0.708, 0.596, 0.574],
            'Urbanization (%)': [47.7, 45.2, 48.4, 22.3, 11.3],
            'Region': ['South', 'West', 'South', 'North', 'East'],
            'Capital': ['Thiruvananthapuram', 'Mumbai', 'Chennai', 'Lucknow', 'Patna'],
            'Official Languages': ['Malayalam', 'Marathi', 'Tamil', 'Hindi', 'Hindi, Urdu'],
            'Famous Destinations': ['Backwaters, Munnar', 'Mumbai, Ajanta Caves', 'Chennai, Madurai', 'Agra, Varanasi', 'Bodh Gaya, Nalanda'],
            'Major Crops': ['Rice, Coconut', 'Cotton, Sugarcane', 'Rice, Sugarcane', 'Wheat, Sugarcane', 'Rice, Wheat'],
            'Key Industries': ['Tourism, IT', 'Manufacturing, Finance', 'Automobiles, Textiles', 'Agriculture, Handicrafts', 'Agriculture, Food processing']
        })

@st.cache_data
def load_cultural_data():
    try:
        with st.spinner("Loading cultural data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM CULTURAL_HERITAGE"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Define complete mapping of Snowflake column names to expected app column names
                    column_mapping = {
                        'NAME': 'Name',
                        'CULTURAL_ELEMENT': 'Cultural Element',
                        'COUNT': 'Count',
                        'TYPE': 'Type',
                        'LOCATION': 'Location',
                        'STATE': 'State',
                        'UNESCO_STATUS': 'UNESCO Status',
                        'YEAR_BUILT': 'Year Built',
                        'DESCRIPTION': 'Description',
                        'HISTORICAL_PERIOD': 'Historical Period',
                        'REGION_OF_ORIGIN': 'Region of Origin',
                        'ASSOCIATED_STATES': 'Associated States',
                        # Additional fields that might be needed for Cultural Contributions
                        'CULTURAL_CONTRIBUTIONS': 'Cultural Contributions'
                    }
                    
                    # Create a new DataFrame with properly mapped columns
                    new_df = pd.DataFrame()
                    
                    # For each expected column in the app
                    for snowflake_col, app_col in column_mapping.items():
                        # If the column exists in Snowflake result
                        if snowflake_col in df.columns:
                            new_df[app_col] = df[snowflake_col]
                        else:
                            # Add empty column with appropriate default values based on column name
                            if app_col == 'UNESCO Status':
                                new_df[app_col] = 'Not Listed'  # Default value
                            elif app_col == 'Cultural Contributions':
                                new_df[app_col] = 'Various cultural contributions'  # Default value
                            elif app_col == 'Type':
                                new_df[app_col] = 'Heritage Site'  # Default value
                            else:
                                new_df[app_col] = ''  # Empty string for other columns
                    
                    # If Name is missing but Cultural Element exists, use Cultural Element as Name
                    if 'Name' not in new_df.columns and 'Cultural Element' in new_df.columns:
                        new_df['Name'] = new_df['Cultural Element']
                    
                    # Return the properly mapped DataFrame
                    return new_df
            except Exception as snowflake_error:
                st.warning(f"Could not load cultural data from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/cultural_heritage.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Add the UNESCO Status column if missing
            if 'UNESCO Status' not in df.columns:
                df['UNESCO Status'] = "Not Listed"  # Default value
            
            # Add Cultural Contributions if missing
            if 'Cultural Contributions' not in df.columns:
                df['Cultural Contributions'] = "Various cultural contributions"  # Default value
                
            # Add Name column if it doesn't exist and Cultural Element does
            if 'Name' not in df.columns and 'Cultural Element' in df.columns:
                df['Name'] = df['Cultural Element']
                
            # Ensure required columns exist for the app to function
            required_columns = ['Name', 'Type', 'UNESCO Status', 'Description', 'Cultural Contributions']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in cultural data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values
                for col in missing_columns:
                    if col == 'Name' and 'Cultural Element' in df.columns:
                        df[col] = df['Cultural Element']
                    elif col == 'Type' and 'Historical Period' in df.columns:
                        df[col] = df['Historical Period']
                    elif col == 'UNESCO Status':
                        df[col] = "Not Listed"
                    elif col == 'Cultural Contributions':
                        df[col] = "Various cultural contributions"
                    elif col == 'Description' and 'Description' in df.columns:
                        df[col] = df['Description']
                    else:
                        df[col] = f"No {col} data available"
            
            return df
    except Exception as e:
        st.error(f"Error loading cultural data: {e}")
        # Return minimal valid dataframe to prevent app crashes
        return pd.DataFrame({
            'Name': ['Taj Mahal', 'Khajuraho Temples'],
            'Type': ['Monument', 'Temple Complex'],
            'UNESCO Status': ['World Heritage Site', 'World Heritage Site'],
            'Description': ['Iconic marble mausoleum', 'Famous temple complex'],
            'Cultural Contributions': ['Mughal architecture', 'Hindu temple art']
        })

@st.cache_data
def load_population_data():
    try:
        with st.spinner("Loading population data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM POPULATION_GROWTH"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Rename columns to match expected format if needed
                    column_mapping = {
                        'YEAR': 'Year',
                        'POPULATION_MILLIONS': 'Population (millions)',
                        'GROWTH_RATE_PCT': 'Growth Rate (%)',
                        'URBAN_POPULATION_PCT': 'Urban Population (%)',
                        'RURAL_POPULATION_PCT': 'Rural Population (%)',
                        'DENSITY': 'Density',
                        'MALE_POPULATION_PCT': 'Male Population (%)',
                        'FEMALE_POPULATION_PCT': 'Female Population (%)',
                        'AGE_0_14_PCT': 'Age 0-14 (%)',
                        'AGE_15_64_PCT': 'Age 15-64 (%)',
                        'AGE_65_PLUS_PCT': 'Age 65+ (%)'
                    }
                    
                    # Only rename columns that exist
                    rename_cols = {}
                    for snowflake_col, app_col in column_mapping.items():
                        if snowflake_col in df.columns:
                            rename_cols[snowflake_col] = app_col
                    
                    if rename_cols:
                        df = df.rename(columns=rename_cols)
                    
                    # Add missing demographic columns
                    add_demographic_default_columns(df)
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/population_growth.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                # Return default data instead of None
                return create_default_population_data()
            
            df = safe_read_csv(file_path)
            
            # Add missing demographic columns
            add_demographic_default_columns(df)
            
            return df
    except Exception as e:
        st.error(f"Error loading population data: {e}")
        return create_default_population_data()

# Helper function to add default demographic columns
def add_demographic_default_columns(df):
    """Add default demographic columns to population dataframe if missing"""
    # Add gender distribution if missing
    if 'Male Population (%)' not in df.columns:
        df['Male Population (%)'] = 51.5  # Approximate values
    
    if 'Female Population (%)' not in df.columns:
        df['Female Population (%)'] = 48.5  # Approximate values
    
    # Add age distribution if missing
    if 'Age 0-14 (%)' not in df.columns:
        df['Age 0-14 (%)'] = 26.2  # Based on 2021 estimates
    
    if 'Age 15-64 (%)' not in df.columns:
        df['Age 15-64 (%)'] = 67.0  # Based on 2021 estimates
    
    if 'Age 65+ (%)' not in df.columns:
        df['Age 65+ (%)'] = 6.8  # Based on 2021 estimates
    
    # Add urban/rural distribution if missing
    if 'Urban Population (%)' not in df.columns:
        df['Urban Population (%)'] = 35.0  # Approximate values
    
    if 'Rural Population (%)' not in df.columns:
        df['Rural Population (%)'] = 65.0  # Approximate values
    
    return df

# Helper function to create default population data
def create_default_population_data():
    """Create default population data to prevent app crashes"""
    return pd.DataFrame({
        'Year': [1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021],
        'Population (millions)': [361, 439, 548, 683, 846, 1029, 1211, 1380],
        'Growth Rate (%)': [1.25, 1.96, 2.22, 2.20, 2.14, 1.97, 1.64, 1.04],
        'Urban Population (%)': [17.3, 18.0, 19.9, 23.3, 25.7, 27.8, 31.2, 35.0],
        'Rural Population (%)': [82.7, 82.0, 80.1, 76.7, 74.3, 72.2, 68.8, 65.0],
        'Density': [117, 142, 177, 216, 267, 325, 382, 411],
        'Male Population (%)': [51.5, 51.5, 51.5, 51.5, 51.5, 51.5, 51.5, 51.5],
        'Female Population (%)': [48.5, 48.5, 48.5, 48.5, 48.5, 48.5, 48.5, 48.5],
        'Age 0-14 (%)': [39.0, 41.0, 42.0, 39.5, 37.8, 35.3, 30.8, 26.2],
        'Age 15-64 (%)': [57.0, 55.0, 54.0, 56.5, 58.0, 60.0, 63.4, 67.0],
        'Age 65+ (%)': [4.0, 4.0, 4.0, 4.0, 4.2, 4.7, 5.8, 6.8]
    })

@st.cache_data
def load_economic_data():
    try:
        with st.spinner("Loading economic data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM ECONOMIC_DATA"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Use consistent column mapping
                    df = map_columns(df, 'economic', 'snowflake_to_app')
                    
                    # Add missing columns if needed
                    if 'Year' not in df.columns:
                        # This shouldn't happen, but just in case
                        df['Year'] = range(1951, 1951 + len(df))
                    
                    # Add missing required columns with default values
                    required_columns = [
                        'GDP (billion USD)', 'GDP Growth Rate (%)', 'Per Capita Income (USD)',
                        'Agriculture', 'Industry', 'Services'
                    ]
                    
                    for column in required_columns:
                        if column not in df.columns:
                            if column == 'GDP (billion USD)':
                                # Generate reasonable GDP values
                                df[column] = [
                                    100 + (i * 150) for i in range(len(df))
                                ]
                            elif column == 'GDP Growth Rate (%)':
                                # Generate reasonable growth rates
                                df[column] = [4.0 + (i % 3) for i in range(len(df))]
                            elif column == 'Per Capita Income (USD)':
                                # Generate reasonable per capita income
                                df[column] = [
                                    500 + (i * 100) for i in range(len(df))
                                ]
                            elif column in ['Agriculture', 'Industry', 'Services']:
                                # Generate reasonable sector percentages
                                if column == 'Agriculture':
                                    df[column] = [
                                        max(10, 50 - (i * 0.5)) for i in range(len(df))
                                    ]
                                elif column == 'Industry':
                                    df[column] = [
                                        min(40, 20 + (i * 0.2)) for i in range(len(df))
                                    ]
                                elif column == 'Services':
                                    df[column] = [
                                        min(70, 30 + (i * 0.5)) for i in range(len(df))
                                    ]
                    
                    # Convert string values to appropriate numeric types
                    numeric_columns = ['GDP (billion USD)', 'GDP Growth Rate (%)', 'Per Capita Income (USD)',
                                       'Agriculture', 'Industry', 'Services']
                    for col in numeric_columns:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    
                    # Sort by year for consistent visualization
                    df = df.sort_values('Year')
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/economic_data.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return create_default_economic_data()
            
            df = safe_read_csv(file_path)
            
            # Check for required columns
            required_columns = [
                'Year', 'GDP (billion USD)', 'GDP Growth Rate (%)', 'Per Capita Income (USD)',
                'Agriculture', 'Industry', 'Services'
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in economic data: {', '.join(missing_columns)}")
                
                # Add Year if missing
                if 'Year' not in df.columns:
                    df['Year'] = range(1951, 1951 + len(df))
                
                # Add other missing columns with default values
                for column in missing_columns:
                    if column == 'GDP (billion USD)':
                        # Generate reasonable GDP values
                        df[column] = [
                            100 + (i * 150) for i in range(len(df))
                        ]
                    elif column == 'GDP Growth Rate (%)':
                        # Generate reasonable growth rates
                        df[column] = [4.0 + (i % 3) for i in range(len(df))]
                    elif column == 'Per Capita Income (USD)':
                        # Generate reasonable per capita income
                        df[column] = [
                            500 + (i * 100) for i in range(len(df))
                        ]
                    elif column in ['Agriculture', 'Industry', 'Services']:
                        # Generate reasonable sector percentages
                        if column == 'Agriculture':
                            df[column] = [
                                max(10, 50 - (i * 0.5)) for i in range(len(df))
                            ]
                        elif column == 'Industry':
                            df[column] = [
                                min(40, 20 + (i * 0.2)) for i in range(len(df))
                            ]
                        elif column == 'Services':
                            df[column] = [
                                min(70, 30 + (i * 0.5)) for i in range(len(df))
                            ]
            
            # Convert string values to appropriate numeric types
            numeric_columns = ['GDP (billion USD)', 'GDP Growth Rate (%)', 'Per Capita Income (USD)',
                               'Agriculture', 'Industry', 'Services']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Sort by year for consistent visualization
            df = df.sort_values('Year')
            return df
    except Exception as e:
        st.error(f"Error loading economic data: {e}")
        # Return minimal valid dataframe to prevent app crashes
        return create_default_economic_data()

# Helper function to create default economic data
def create_default_economic_data():
    """Create default economic data to prevent app crashes"""
    years = list(range(1951, 2024, 10))
    
    return pd.DataFrame({
        'Year': years,
        'GDP (billion USD)': [100, 200, 400, 800, 1600, 2200, 3200, 3730],
        'GDP Growth Rate (%)': [3.5, 4.0, 5.2, 6.7, 8.5, 6.2, 5.0, 7.2],
        'Per Capita Income (USD)': [500, 750, 1100, 1800, 3500, 5500, 8000, 9800],
        'Agriculture': [50, 45, 35, 30, 22, 18, 15, 14],
        'Industry': [20, 22, 25, 28, 30, 28, 26, 25],
        'Services': [30, 33, 40, 42, 48, 54, 59, 61],
        'Exports (billion USD)': [5, 10, 25, 75, 200, 350, 550, 775],
        'Imports (billion USD)': [7, 15, 30, 90, 250, 400, 600, 892],
        'Unemployment Rate (%)': [7.5, 6.8, 6.2, 5.8, 5.2, 5.7, 6.1, 7.5]
    })

@st.cache_data
def load_historical_data():
    try:
        with st.spinner("Loading historical timeline data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM HISTORICAL_TIMELINE"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Use consistent column mapping
                    df = map_columns(df, 'historical', 'snowflake_to_app')
                    
                    # Generate Time Period if missing
                    if 'Time Period' not in df.columns:
                        if 'Start Year' in df.columns and 'End Year' in df.columns:
                            # Create Time Period from Start Year and End Year - handle NaN values
                            df['Start Year'] = pd.to_numeric(df['Start Year'], errors='coerce').fillna(0).astype(int)
                            df['End Year'] = pd.to_numeric(df['End Year'], errors='coerce').fillna(0).astype(int)
                            
                            df['Time Period'] = df.apply(lambda x: 
                                f"{abs(x['Start Year'])} BCE - {abs(x['End Year'])} BCE" if x['Start Year'] < 0 and x['End Year'] < 0 else
                                f"{abs(x['Start Year'])} BCE - {x['End Year']} CE" if x['Start Year'] < 0 and x['End Year'] >= 0 else
                                f"{x['Start Year']} - {x['End Year']} CE", axis=1)
                        elif 'Period' in df.columns:
                            # Try to extract years from Period column
                            df['Time Period'] = df['Period']
                        else:
                            # Generate default time periods
                            df['Time Period'] = [f"Period {i+1}" for i in range(len(df))]
                    
                    # Add missing columns with default values
                    if 'Era' not in df.columns:
                        df['Era'] = df['Time Period'].apply(lambda x: x.split("-")[0].strip())
                    
                    # Ensure Start Year and End Year are numeric
                    if 'Start Year' in df.columns:
                        df['Start Year'] = pd.to_numeric(df['Start Year'], errors='coerce').fillna(0).astype(int)
                    else:
                        df['Start Year'] = 0
                        
                    if 'End Year' in df.columns:
                        df['End Year'] = pd.to_numeric(df['End Year'], errors='coerce').fillna(0).astype(int)
                    else:
                        df['End Year'] = 0
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/historical_timeline.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return create_default_historical_data()
            
            df = safe_read_csv(file_path)
            
            # Check for required columns
            if 'Time Period' not in df.columns:
                if 'Start Year' in df.columns and 'End Year' in df.columns:
                    # Create Time Period from Start Year and End Year - handle NaN values
                    df['Start Year'] = pd.to_numeric(df['Start Year'], errors='coerce').fillna(0).astype(int)
                    df['End Year'] = pd.to_numeric(df['End Year'], errors='coerce').fillna(0).astype(int)
                    
                    df['Time Period'] = df.apply(lambda x: 
                        f"{abs(x['Start Year'])} BCE - {abs(x['End Year'])} BCE" if x['Start Year'] < 0 and x['End Year'] < 0 else
                        f"{abs(x['Start Year'])} BCE - {x['End Year']} CE" if x['Start Year'] < 0 and x['End Year'] >= 0 else
                        f"{x['Start Year']} - {x['End Year']} CE", axis=1)
                elif 'Period' in df.columns:
                    # Try to extract years from Period column
                    df['Time Period'] = df['Period']
                else:
                    # Generate default time periods
                    df['Time Period'] = [f"Period {i+1}" for i in range(len(df))]
            
            # Add Era column if missing
            if 'Era' not in df.columns:
                df['Era'] = df['Time Period'].apply(lambda x: x.split("-")[0].strip())
            
            # Ensure Start Year and End Year are numeric
            if 'Start Year' in df.columns:
                df['Start Year'] = pd.to_numeric(df['Start Year'], errors='coerce').fillna(0).astype(int)
            else:
                df['Start Year'] = 0
                
            if 'End Year' in df.columns:
                df['End Year'] = pd.to_numeric(df['End Year'], errors='coerce').fillna(0).astype(int)
            else:
                df['End Year'] = 0
            
            return df
    except Exception as e:
        st.error(f"Error loading historical data: {e}")
        # Return minimal valid dataframe to prevent app crashes
        return create_default_historical_data()

# Helper function to create default historical data
def create_default_historical_data():
    """Create default historical data to prevent app crashes"""
    return pd.DataFrame({
        'Era': ['Indus Valley Civilization', 'Vedic Period', 'Mauryan Empire', 'Gupta Empire', 'Delhi Sultanate'],
        'Time Period': ['2600-1900 BCE', '1500-500 BCE', '322-185 BCE', '320-550 CE', '1206-1526 CE'],
        'Major Events': ['Urban planning and trade', 'Composition of Vedas', 'Ashoka\'s reign', 'Golden Age of India', 'Islamic rule in North India'],
        'Significance': ['Early civilization', 'Religious foundations', 'First major empire', 'Cultural and scientific achievements', 'Cultural synthesis'],
        'Start Year': [-2600, -1500, -322, 320, 1206],
        'End Year': [-1900, -500, -185, 550, 1526]
    })

@st.cache_data
def load_festivals_data():
    try:
        with st.spinner("Loading festivals data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM FESTIVALS"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Use consistent column mapping
                    df = map_columns(df, 'festivals', 'snowflake_to_app')
                    
                    # Add missing columns with default values
                    if 'Religion/Type' not in df.columns:
                        df['Religion/Type'] = 'Cultural'  # Default value
                        
                    if 'Primary States' not in df.columns:
                        df['Primary States'] = 'All India'  # Default value
                        
                    if 'Participants (millions)' not in df.columns:
                        df['Participants (millions)'] = 5.0  # Default value
                        
                    if 'Economic Impact (Millions USD)' not in df.columns:
                        df['Economic Impact (Millions USD)'] = 250.0  # Default value
                        
                    if 'Tourist Attraction Level' not in df.columns:
                        df['Tourist Attraction Level'] = 'Medium'  # Default value
                        
                    if 'Environmental Impact' not in df.columns:
                        df['Environmental Impact'] = 'Moderate'  # Default value
                        
                    if 'Duration (days)' not in df.columns:
                        df['Duration (days)'] = 1  # Default value
                        
                    if 'Global Celebrations' not in df.columns:
                        df['Global Celebrations'] = '10+ countries'  # Default value
                        
                    if 'Season' not in df.columns:
                        df['Season'] = 'Year-round'  # Default value
                    
                    # Convert numeric columns to appropriate types
                    if 'Participants (millions)' in df.columns:
                        df['Participants (millions)'] = pd.to_numeric(df['Participants (millions)'], errors='coerce').fillna(5.0)
                        
                    if 'Economic Impact (Millions USD)' in df.columns:
                        df['Economic Impact (Millions USD)'] = pd.to_numeric(df['Economic Impact (Millions USD)'], errors='coerce').fillna(250.0)
                        
                    if 'Duration (days)' in df.columns:
                        df['Duration (days)'] = pd.to_numeric(df['Duration (days)'], errors='coerce').fillna(1).astype(int)
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load festivals data from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/festivals.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return create_default_festivals_data()
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Festival', 'Religion/Type', 'Description']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in festivals data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values
                for col in missing_columns:
                    if col == 'Festival':
                        df[col] = [f"Festival {i+1}" for i in range(len(df))]
                    elif col == 'Religion/Type':
                        df[col] = 'Cultural'  # Default value
                    elif col == 'Description':
                        df[col] = 'No description available'  # Default value
            
            # Add additional required columns if missing
            if 'Participants (millions)' not in df.columns:
                df['Participants (millions)'] = 5.0  # Default value
                
            if 'Economic Impact (Millions USD)' not in df.columns and 'Economic Impact (USD millions)' not in df.columns:
                df['Economic Impact (Millions USD)'] = 250.0  # Default value
            elif 'Economic Impact (USD millions)' in df.columns and 'Economic Impact (Millions USD)' not in df.columns:
                df['Economic Impact (Millions USD)'] = df['Economic Impact (USD millions)']
                
            if 'Tourist Attraction Level' not in df.columns:
                df['Tourist Attraction Level'] = 'Medium'  # Default value
                
            if 'Environmental Impact' not in df.columns:
                df['Environmental Impact'] = 'Moderate'  # Default value
                
            if 'Duration (days)' not in df.columns:
                df['Duration (days)'] = 1  # Default value
                
            if 'Global Celebrations' not in df.columns:
                df['Global Celebrations'] = '10+ countries'  # Default value
                
            if 'Season' not in df.columns:
                df['Season'] = 'Year-round'  # Default value
            
            # Convert numeric columns to appropriate types
            if 'Participants (millions)' in df.columns:
                df['Participants (millions)'] = pd.to_numeric(df['Participants (millions)'], errors='coerce').fillna(5.0)
                
            if 'Economic Impact (Millions USD)' in df.columns:
                df['Economic Impact (Millions USD)'] = pd.to_numeric(df['Economic Impact (Millions USD)'], errors='coerce').fillna(250.0)
                
            if 'Duration (days)' in df.columns:
                df['Duration (days)'] = pd.to_numeric(df['Duration (days)'], errors='coerce').fillna(1).astype(int)
            
            return df
    except Exception as e:
        st.error(f"Error loading festivals data: {e}")
        # Return minimal valid dataframe to prevent app crashes
        return create_default_festivals_data()

# Create default festivals data function
def create_default_festivals_data():
    """Create default festivals data to prevent app crashes"""
    return pd.DataFrame({
        'Festival': ['Diwali', 'Holi', 'Eid-ul-Fitr', 'Christmas', 'Durga Puja'],
        'Religion/Type': ['Hindu', 'Hindu', 'Islamic', 'Christian', 'Hindu'],
        'Description': ['Festival of lights', 'Festival of colors', 'End of Ramadan', 'Birth of Jesus Christ', 'Worship of Goddess Durga'],
        'Season': ['October-November', 'March', 'Variable', 'December', 'September-October'],
        'Participants (millions)': [800, 600, 200, 30, 100],
        'Economic Impact (Millions USD)': [800, 500, 300, 200, 400],
        'Tourist Attraction Level': ['High', 'High', 'Medium', 'Medium', 'High'],
        'Environmental Impact': ['Moderate to High', 'Low to Moderate', 'Low', 'Low', 'Moderate'],
        'Duration (days)': [5, 2, 3, 1, 10],
        'Global Celebrations': ['30+ countries', '20+ countries', '50+ countries', '100+ countries', '10+ countries']
    })

@st.cache_data
def load_tourism_data():
    try:
        with st.spinner("Loading tourism data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM TOURISM"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Rename columns to match expected format if needed
                    column_mapping = {
                        'DESTINATION': 'Destination',
                        'STATE': 'State',
                        'TYPE': 'Type',
                        'TOURISM_TYPE': 'Tourism Type',
                        'VISITORS_ANNUAL': 'Annual Visitors (millions)',
                        'VISITORS_MILLIONS': 'Visitors (millions)',
                        'BEST_TIME': 'Best Time',
                        'BEST_SEASON': 'Peak Season',
                        'PEAK_SEASON': 'Peak Season',
                        'DESCRIPTION': 'Description',
                        'UNESCO_STATUS': 'UNESCO Status',
                        'YEAR_ESTABLISHED': 'Year Established',
                        'ENTRY_FEE_INR': 'Entry Fee (INR)'
                    }
                    
                    # Only rename columns that exist
                    rename_cols = {}
                    for snowflake_col, app_col in column_mapping.items():
                        if snowflake_col in df.columns:
                            rename_cols[snowflake_col] = app_col
                    
                    if rename_cols:
                        df = df.rename(columns=rename_cols)
                    
                    # Add any missing columns with default values
                    if 'UNESCO Status' not in df.columns:
                        df['UNESCO Status'] = 'Not Listed'
                        # Set some popular destinations as World Heritage Sites
                        world_heritage_sites = ['Taj Mahal', 'Qutub Minar', 'Red Fort', 'Ajanta Caves', 'Ellora Caves', 
                                               'Khajuraho', 'Hampi', 'Mahabodhi Temple', 'Sun Temple Konark', 'Fatehpur Sikri']
                        df.loc[df['Destination'].isin(world_heritage_sites), 'UNESCO Status'] = 'World Heritage Site'
                    
                    if 'Peak Season' not in df.columns and 'Best Time' in df.columns:
                        df['Peak Season'] = df['Best Time']
                    elif 'Peak Season' not in df.columns:
                        df['Peak Season'] = 'October-March'
                    
                    if 'Year Established' not in df.columns:
                        df['Year Established'] = 1900  # Default value
                        
                    if 'Entry Fee (INR)' not in df.columns:
                        df['Entry Fee (INR)'] = 50  # Default value
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/tourism.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                # Return default data instead of None
                return create_default_tourism_data()
            
            df = safe_read_csv(file_path)
            
            # Add any missing columns with default values
            if 'UNESCO Status' not in df.columns:
                df['UNESCO Status'] = 'Not Listed'
                # Set some popular destinations as World Heritage Sites
                world_heritage_sites = ['Taj Mahal', 'Qutub Minar', 'Red Fort', 'Ajanta Caves', 'Ellora Caves', 
                                       'Khajuraho', 'Hampi', 'Mahabodhi Temple', 'Sun Temple Konark', 'Fatehpur Sikri']
                if 'Destination' in df.columns:
                    df.loc[df['Destination'].isin(world_heritage_sites), 'UNESCO Status'] = 'World Heritage Site'
            
            if 'Peak Season' not in df.columns and 'Best Time' in df.columns:
                df['Peak Season'] = df['Best Time']
            elif 'Peak Season' not in df.columns:
                df['Peak Season'] = 'October-March'
            
            if 'Year Established' not in df.columns:
                df['Year Established'] = 1900  # Default value
                
            if 'Entry Fee (INR)' not in df.columns:
                df['Entry Fee (INR)'] = 50  # Default value
            
            # If Type column is missing but Tourism Type exists
            if 'Type' not in df.columns and 'Tourism Type' in df.columns:
                df['Type'] = df['Tourism Type']
            elif 'Type' not in df.columns:
                df['Type'] = 'Cultural'
                
            # If Tourism Type column is missing but Type exists
            if 'Tourism Type' not in df.columns and 'Type' in df.columns:
                df['Tourism Type'] = df['Type']
            elif 'Tourism Type' not in df.columns:
                df['Tourism Type'] = 'Cultural'
            
            return df
    except Exception as e:
        st.error(f"Error loading tourism data: {e}")
        return create_default_tourism_data()

# Helper function to create default tourism data
def create_default_tourism_data():
    """Create default tourism data to prevent app crashes"""
    return pd.DataFrame({
        'Destination': ['Taj Mahal', 'Jaipur City', 'Golden Temple', 'Varanasi', 'Goa Beaches'],
        'State': ['Uttar Pradesh', 'Rajasthan', 'Punjab', 'Uttar Pradesh', 'Goa'],
        'Type': ['Monument', 'Heritage City', 'Religious', 'Religious', 'Beach'],
        'Tourism Type': ['Heritage', 'Heritage', 'Religious', 'Religious', 'Nature'],
        'Annual Visitors (millions)': [7.0, 5.2, 6.0, 4.5, 8.0],
        'Peak Season': ['October-March', 'November-February', 'Year-round', 'October-March', 'November-February'],
        'UNESCO Status': ['World Heritage Site', 'Not Listed', 'Not Listed', 'Not Listed', 'Not Listed'],
        'Year Established': [1631, 1727, 1604, 1800, 1900],
        'Entry Fee (INR)': [1100, 200, 0, 200, 0],
        'Description': [
            'The iconic white marble mausoleum built by Emperor Shah Jahan in memory of his wife Mumtaz Mahal.',
            'Known as the Pink City, famous for its stunning palaces, forts, and vibrant culture.',
            'The holiest shrine of Sikhism, known for its golden dome and spiritual significance.',
            'One of the oldest continuously inhabited cities, known for its ghats along the Ganges River.',
            'Famous for pristine beaches, vibrant nightlife, and Portuguese colonial architecture.'
        ]
    })

@st.cache_data
def load_education_data():
    try:
        with st.spinner("Loading education data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM EDUCATION"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Use consistent column mapping
                    df = map_columns(df, 'education', 'snowflake_to_app')
                    
                    # Add missing columns with default values
                    df = add_education_default_columns(df)
                    
                    # Convert string values to appropriate numeric types
                    numeric_columns = [
                        'National Literacy Rate (%)', 'Primary Enrollment Rate (%)',
                        'Male Literacy (%)', 'Female Literacy (%)', 'Literacy Gap',
                        'Number of Primary Schools', 'Number of Secondary Schools',
                        'Number of Colleges', 'Number of Universities',
                        'Number of Technical Institutions', 'Higher Education Enrollment (millions)',
                        'Gender Parity Primary', 'Gender Parity Secondary', 'Gender Parity Higher Ed'
                    ]
                    
                    for col in numeric_columns:
                        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/education.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                # Return default data instead of None
                return create_default_education_data()
            
            df = safe_read_csv(file_path)
            
            # Add missing columns with default values
            df = add_education_default_columns(df)
            
            # Convert string values to appropriate numeric types
            numeric_columns = [
                'National Literacy Rate (%)', 'Primary Enrollment Rate (%)',
                'Male Literacy (%)', 'Female Literacy (%)', 'Literacy Gap',
                'Number of Primary Schools', 'Number of Secondary Schools',
                'Number of Colleges', 'Number of Universities',
                'Number of Technical Institutions', 'Higher Education Enrollment (millions)',
                'Gender Parity Primary', 'Gender Parity Secondary', 'Gender Parity Higher Ed'
            ]
            
            for col in numeric_columns:
                if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            return df
    except Exception as e:
        st.error(f"Error loading education data: {e}")
        return create_default_education_data()

# Helper function to add default education columns
def add_education_default_columns(df):
    """Add default columns to education dataframe if missing"""
    if 'National Literacy Rate (%)' not in df.columns:
        df['National Literacy Rate (%)'] = 74.4  # As per 2021 data
    
    if 'Primary Enrollment Rate (%)' not in df.columns:
        df['Primary Enrollment Rate (%)'] = 95.0  # Default value
    
    if 'State Names' not in df.columns:
        df['State Names'] = 'Kerala, Delhi, Himachal Pradesh, Uttarakhand, Maharashtra, Tamil Nadu, Gujarat, Punjab, Karnataka, Andhra Pradesh'
    
    if 'State Literacy Rates (%)' not in df.columns:
        df['State Literacy Rates (%)'] = '94.0, 93.7, 92.5, 90.0, 89.8, 89.1, 89.0, 84.6, 82.8, 81.3'
    
    if 'State Primary Enrollment (%)' not in df.columns:
        df['State Primary Enrollment (%)'] = '98.3, 97.8, 98.1, 97.5, 96.2, 95.8, 94.7, 95.6, 94.9, 94.1'
    
    if 'State Secondary Enrollment (%)' not in df.columns:
        df['State Secondary Enrollment (%)'] = '85.3, 84.2, 86.1, 83.7, 82.9, 81.8, 79.5, 83.2, 80.1, 79.8'
    
    if 'State Higher Ed Enrollment (%)' not in df.columns:
        df['State Higher Ed Enrollment (%)'] = '32.4, 30.5, 31.2, 29.8, 28.7, 27.9, 25.2, 28.6, 26.4, 25.8'
    
    if 'Male Literacy (%)' not in df.columns:
        df['Male Literacy (%)'] = [94.0, 93.7, 92.5, 90.0, 89.8, 89.1, 89.0, 84.6, 82.8, 81.3]
    
    if 'Female Literacy (%)' not in df.columns:
        df['Female Literacy (%)'] = [92.0, 82.4, 83.9, 76.5, 77.4, 76.8, 70.7, 76.0, 72.0, 67.4]
    
    if 'Literacy Gap' not in df.columns:
        # Calculate gap if both male and female literacy are available
        if all(col in df.columns for col in ['Male Literacy (%)', 'Female Literacy (%)']):
            df['Literacy Gap'] = df['Male Literacy (%)'] - df['Female Literacy (%)']
        else:
            df['Literacy Gap'] = [2.0, 11.3, 8.6, 13.5, 12.4, 12.3, 18.3, 8.6, 10.8, 13.9]
    
    if 'Number of Primary Schools' not in df.columns:
        df['Number of Primary Schools'] = 1500000  # Approximate value
        
    if 'Number of Secondary Schools' not in df.columns:
        df['Number of Secondary Schools'] = 230000  # Approximate value
        
    if 'Number of Colleges' not in df.columns:
        df['Number of Colleges'] = 40000  # Approximate value
        
    if 'Number of Universities' not in df.columns:
        df['Number of Universities'] = 1000  # Approximate value
        
    if 'Number of Technical Institutions' not in df.columns:
        df['Number of Technical Institutions'] = 12000  # Approximate value
    
    if 'Higher Education Enrollment (millions)' not in df.columns:
        df['Higher Education Enrollment (millions)'] = 38.5  # Approximate value
    
    if 'PISA Score' not in df.columns:
        df['PISA Score'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # India doesn't participate in PISA regularly
    
    if 'Global Rank' not in df.columns:
        df['Global Rank'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Placeholder ranks
    
    if 'University Ranking' not in df.columns:
        df['University Ranking'] = ['IIT Delhi (150-200)', 'IIT Bombay (150-200)', 'IISc Bangalore (200-250)', 
                                   'IIT Madras (250-300)', 'IIT Kharagpur (300-350)', 'Delhi University (500-550)',
                                   'JNU (550-600)', 'IIT Roorkee (600-650)', 'IIT Guwahati (700-750)', 'BHU (800-850)']
    
    if 'Teacher-Student Ratio Primary' not in df.columns:
        df['Teacher-Student Ratio Primary'] = '1:30'
        
    if 'Teacher-Student Ratio Secondary' not in df.columns:
        df['Teacher-Student Ratio Secondary'] = '1:25'
        
    if 'Teacher-Student Ratio Higher Ed' not in df.columns:
        df['Teacher-Student Ratio Higher Ed'] = '1:20'
        
    if 'Gender Parity Primary' not in df.columns:
        df['Gender Parity Primary'] = 0.98
        
    if 'Gender Parity Secondary' not in df.columns:
        df['Gender Parity Secondary'] = 0.95
        
    if 'Gender Parity Higher Ed' not in df.columns:
        df['Gender Parity Higher Ed'] = 0.92
        
    if 'Literacy Rate Years' not in df.columns:
        df['Literacy Rate Years'] = '1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021'
        
    if 'Literacy Rate History' not in df.columns:
        df['Literacy Rate History'] = '18.3, 28.3, 34.5, 43.6, 52.2, 64.8, 74.0, 77.7'
    
    return df

# Helper function to create default education data
def create_default_education_data():
    """Create default education data to prevent app crashes"""
    df = pd.DataFrame({
        'Level': ['Primary', 'Secondary', 'Higher Secondary', 'Undergraduate', 'Postgraduate'],
        'Enrollment (millions)': [130.0, 67.0, 37.0, 26.0, 4.2],
        'Male (%)': [52, 55, 53, 54, 55],
        'Female (%)': [48, 45, 47, 46, 45],
        'Literacy Rate (%)': [74.4, 0, 0, 0, 0],
        'National Literacy Rate (%)': [74.4, 74.4, 74.4, 74.4, 74.4],
        'Primary Enrollment Rate (%)': [95.0, 95.0, 95.0, 95.0, 95.0],
        'Institutions': [1500000, 230000, 150000, 40000, 12000],
        'State Names': ['Kerala, Delhi, Himachal Pradesh, Uttarakhand, Maharashtra', 
                        'Kerala, Delhi, Himachal Pradesh, Uttarakhand, Maharashtra',
                        'Kerala, Delhi, Himachal Pradesh, Uttarakhand, Maharashtra',
                        'Kerala, Delhi, Himachal Pradesh, Uttarakhand, Maharashtra',
                        'Kerala, Delhi, Himachal Pradesh, Uttarakhand, Maharashtra'],
        'State Literacy Rates (%)': ['94.0, 93.7, 92.5, 90.0, 89.8', 
                                    '94.0, 93.7, 92.5, 90.0, 89.8',
                                    '94.0, 93.7, 92.5, 90.0, 89.8',
                                    '94.0, 93.7, 92.5, 90.0, 89.8',
                                    '94.0, 93.7, 92.5, 90.0, 89.8'],
        'State Primary Enrollment (%)': ['98.3, 97.8, 98.1, 97.5, 96.2',
                                        '98.3, 97.8, 98.1, 97.5, 96.2',
                                        '98.3, 97.8, 98.1, 97.5, 96.2',
                                        '98.3, 97.8, 98.1, 97.5, 96.2',
                                        '98.3, 97.8, 98.1, 97.5, 96.2'],
        'State Secondary Enrollment (%)': ['85.3, 84.2, 86.1, 83.7, 82.9',
                                          '85.3, 84.2, 86.1, 83.7, 82.9',
                                          '85.3, 84.2, 86.1, 83.7, 82.9',
                                          '85.3, 84.2, 86.1, 83.7, 82.9',
                                          '85.3, 84.2, 86.1, 83.7, 82.9'],
        'State Higher Ed Enrollment (%)': ['32.4, 30.5, 31.2, 29.8, 28.7',
                                          '32.4, 30.5, 31.2, 29.8, 28.7',
                                          '32.4, 30.5, 31.2, 29.8, 28.7',
                                          '32.4, 30.5, 31.2, 29.8, 28.7',
                                          '32.4, 30.5, 31.2, 29.8, 28.7']
    })
    
    # Add other required columns
    return add_education_default_columns(df)

@st.cache_data
def load_geography_data():
    try:
        with st.spinner("Loading geography data..."):
            # Try to load from Snowflake first
            try:
                query = "SELECT * FROM GEOGRAPHY"
                df = query_snowflake(query)
                if df is not None and not df.empty:
                    # Rename columns to match expected format if needed
                    column_mapping = {
                        'REGION': 'Region',
                        'AREA_KM2': 'Area (km²)',
                        'CLIMATE': 'Climate',
                        'MAJOR_RIVERS': 'Major Rivers',
                        'MAJOR_MOUNTAINS': 'Major Mountains',
                        'BIODIVERSITY': 'Biodiversity',
                        'TERRAIN_TYPE': 'Terrain_Type',
                        'PERCENTAGE': 'Percentage'
                    }
                    
                    # Only rename columns that exist
                    rename_cols = {}
                    for snowflake_col, app_col in column_mapping.items():
                        if snowflake_col in df.columns:
                            rename_cols[snowflake_col] = app_col
                    
                    if rename_cols:
                        df = df.rename(columns=rename_cols)
                    
                    # Add missing columns if they don't exist
                    if 'Terrain_Type' not in df.columns:
                        # Create terrain data
                        terrain_data = {
                            'Terrain_Type': ['Mountains', 'Plains', 'Plateaus', 'Deserts', 'Coastal', 'Forest'],
                            'Percentage': [20.5, 43.3, 27.7, 4.6, 3.1, 0.8]
                        }
                        return pd.DataFrame(terrain_data)
                    
                    return df
            except Exception as snowflake_error:
                st.warning(f"Could not load from Snowflake: {snowflake_error}. Falling back to local file.")
            
            # Fall back to local file if Snowflake fails
            file_path = "data/geography.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                # Return default geography data instead of None to prevent app crashes
                terrain_data = {
                    'Terrain_Type': ['Mountains', 'Plains', 'Plateaus', 'Deserts', 'Coastal', 'Forest'],
                    'Percentage': [20.5, 43.3, 27.7, 4.6, 3.1, 0.8]
                }
                return pd.DataFrame(terrain_data)
            
            df = safe_read_csv(file_path)
            
            # If we have geography.csv but not the terrain data needed
            if 'Terrain_Type' not in df.columns:
                # Create terrain data
                terrain_data = {
                    'Terrain_Type': ['Mountains', 'Plains', 'Plateaus', 'Deserts', 'Coastal', 'Forest'],
                    'Percentage': [20.5, 43.3, 27.7, 4.6, 3.1, 0.8]
                }
                return pd.DataFrame(terrain_data)
            
            return df
    except Exception as e:
        st.error(f"Error loading geography data: {e}")
        # Return default geography data
        terrain_data = {
            'Terrain_Type': ['Mountains', 'Plains', 'Plateaus', 'Deserts', 'Coastal', 'Forest'],
            'Percentage': [20.5, 43.3, 27.7, 4.6, 3.1, 0.8]
        }
        return pd.DataFrame(terrain_data)

# Helper function to get a color palette
def get_color_palette(n, palette_type="qualitative"):
    """Generate a color palette with n colors"""
    if palette_type == "qualitative":
        if n <= 10:
            return px.colors.qualitative.Plotly[:n]
        else:
            return px.colors.qualitative.Alphabet[:n]
    elif palette_type == "sequential":
        return px.colors.sequential.Plasma[:n]
    else:
        return px.colors.sequential.Viridis[:n] 

# Column mapping dictionaries for consistent naming
# These dictionaries map between Snowflake column names (keys) and application column names (values)
COLUMN_MAPPINGS = {
    # Economic data column mapping
    'economic': {
        'YEAR': 'Year',
        'GDP_BILLION_USD': 'GDP (billion USD)',
        'GDP_GROWTH_RATE_PCT': 'GDP Growth Rate (%)',
        'GDP_GROWTH_RATE_PERCENT': 'GDP Growth Rate (%)',
        'PER_CAPITA_INCOME_USD': 'Per Capita Income (USD)',
        'AGRICULTURE': 'Agriculture',
        'INDUSTRY': 'Industry',
        'SERVICES': 'Services',
        'EXPORTS_BILLION_USD': 'Exports (billion USD)',
        'EXPORTS_USD_BILLIONS': 'Exports (billion USD)',
        'IMPORTS_BILLION_USD': 'Imports (billion USD)',
        'IMPORTS_USD_BILLIONS': 'Imports (billion USD)',
        'UNEMPLOYMENT_RATE_PCT': 'Unemployment Rate (%)',
        'UNEMPLOYMENT_RATE_PERCENT': 'Unemployment Rate (%)'
    },
    
    # Education data column mapping
    'education': {
        'LEVEL': 'Level',
        'ENROLLMENT_MILLIONS': 'Enrollment (millions)',
        'MALE_PCT': 'Male (%)',
        'FEMALE_PCT': 'Female (%)',
        'LITERACY_RATE_PCT': 'Literacy Rate (%)',
        'NATIONAL_LITERACY_RATE_PCT': 'National Literacy Rate (%)',
        'PRIMARY_ENROLLMENT_RATE_PCT': 'Primary Enrollment Rate (%)',
        'INSTITUTIONS': 'Institutions',
        'STATE_NAMES': 'State Names',
        'STATE_LITERACY_RATES_PCT': 'State Literacy Rates (%)',
        'STATE_PRIMARY_ENROLLMENT_PCT': 'State Primary Enrollment (%)',
        'STATE_SECONDARY_ENROLLMENT_PCT': 'State Secondary Enrollment (%)',
        'STATE_HIGHER_ED_ENROLLMENT_PCT': 'State Higher Ed Enrollment (%)',
        'MALE_LITERACY_PCT': 'Male Literacy (%)',
        'FEMALE_LITERACY_PCT': 'Female Literacy (%)',
        'LITERACY_GAP': 'Literacy Gap',
        'NUMBER_OF_PRIMARY_SCHOOLS': 'Number of Primary Schools',
        'NUMBER_OF_SECONDARY_SCHOOLS': 'Number of Secondary Schools',
        'NUMBER_OF_COLLEGES': 'Number of Colleges',
        'NUMBER_OF_UNIVERSITIES': 'Number of Universities',
        'NUMBER_OF_TECHNICAL_INSTITUTIONS': 'Number of Technical Institutions',
        'HIGHER_EDUCATION_ENROLLMENT_MILLIONS': 'Higher Education Enrollment (millions)',
        'PISA_SCORE': 'PISA Score',
        'GLOBAL_RANK': 'Global Rank',
        'UNIVERSITY_RANKING': 'University Ranking',
        'TEACHER_STUDENT_RATIO_PRIMARY': 'Teacher-Student Ratio Primary',
        'TEACHER_STUDENT_RATIO_SECONDARY': 'Teacher-Student Ratio Secondary',
        'TEACHER_STUDENT_RATIO_HIGHER_ED': 'Teacher-Student Ratio Higher Ed',
        'GENDER_PARITY_PRIMARY': 'Gender Parity Primary',
        'GENDER_PARITY_SECONDARY': 'Gender Parity Secondary',
        'GENDER_PARITY_HIGHER_ED': 'Gender Parity Higher Ed',
        'LITERACY_RATE_YEARS': 'Literacy Rate Years',
        'LITERACY_RATE_HISTORY': 'Literacy Rate History'
    },
    
    # Historical timeline data column mapping
    'historical': {
        'PERIOD': 'Period',
        'START_YEAR': 'Start Year',
        'END_YEAR': 'End Year',
        'ERA': 'Era',
        'MAJOR_EVENTS': 'Major Events',
        'SIGNIFICANCE': 'Significance',
        'TIME_PERIOD': 'Time Period',
        'CULTURAL_DEVELOPMENTS': 'Cultural Developments',
        'RELIGIOUS_TRENDS': 'Religious Trends',
        'ART_ARCHITECTURE': 'Art & Architecture',
        'ECONOMIC_SYSTEMS': 'Economic Systems',
        'SCIENTIFIC_ADVANCES': 'Scientific Advances',
        'HISTORICAL_LEGACY': 'Historical Legacy'
    },
    
    # Festival data column mapping
    'festivals': {
        'FESTIVAL': 'Festival',
        'RELIGION_TYPE': 'Religion/Type',
        'PRIMARY_STATES': 'Primary States',
        'MONTH': 'Month',
        'SEASON': 'Season',
        'DESCRIPTION': 'Description',
        'CULTURAL_SIGNIFICANCE': 'Cultural Significance',
        'REGIONAL_VARIATIONS': 'Regional Variations',
        'GLOBAL_CELEBRATIONS': 'Global Celebrations',
        'PARTICIPANTS_MILLIONS': 'Participants (millions)',
        'ECONOMIC_IMPACT_MILLIONS_USD': 'Economic Impact (Millions USD)',
        'TOURIST_ATTRACTION_LEVEL': 'Tourist Attraction Level',
        'ENVIRONMENTAL_IMPACT': 'Environmental Impact',
        'DURATION_DAYS': 'Duration (days)'
    },
    
    # State data column mapping
    'states': {
        'STATE': 'State',
        'POPULATION_MILLIONS': 'Population (millions)',
        'AREA_SQ_KM': 'Area (sq km)',
        'LITERACY_RATE_PCT': 'Literacy Rate (%)',
        'REGION': 'Region',
        'CAPITAL': 'Capital',
        'OFFICIAL_LANGUAGES': 'Official Languages',
        'MAJOR_INDUSTRIES': 'Major Industries',
        'GDP_BILLION_USD': 'GDP (billion USD)',
        'HDI': 'HDI',
        'URBANIZATION_PCT': 'Urbanization (%)',
        'FAMOUS_DESTINATIONS': 'Famous Destinations',
        'MAJOR_CROPS': 'Major Crops',
        'KEY_INDUSTRIES': 'Key Industries'
    }
}

# Utility function for standardized column mapping
def map_columns(df, data_type, direction='snowflake_to_app'):
    """
    Map column names between Snowflake and application formats
    
    Args:
        df (DataFrame): The dataframe to map columns for
        data_type (str): Type of data ('economic', 'education', 'historical', etc.)
        direction (str): Direction of mapping ('snowflake_to_app' or 'app_to_snowflake')
        
    Returns:
        DataFrame: DataFrame with mapped column names
    """
    if data_type not in COLUMN_MAPPINGS:
        return df  # No mapping available for this data type
    
    # Get mapping dictionary for this data type
    mapping = COLUMN_MAPPINGS[data_type]
    
    if direction == 'snowflake_to_app':
        # Convert from Snowflake column names to application column names
        rename_cols = {}
        for snowflake_col, app_col in mapping.items():
            if snowflake_col in df.columns:
                rename_cols[snowflake_col] = app_col
        
        if rename_cols:
            df = df.rename(columns=rename_cols)
    else:
        # Convert from application column names to Snowflake column names
        # Create reverse mapping
        reverse_mapping = {v: k for k, v in mapping.items()}
        
        rename_cols = {}
        for app_col, snowflake_col in reverse_mapping.items():
            if app_col in df.columns:
                rename_cols[app_col] = snowflake_col
        
        if rename_cols:
            df = df.rename(columns=rename_cols)
    
    return df
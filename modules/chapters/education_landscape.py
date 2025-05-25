import streamlit as st
import pandas as pd
import plotly.express as px
from modules.utils import apply_dark_theme, load_education_data, get_color_palette

def render():
    """Render the Education Landscape chapter content"""
    st.title("📚 Education Landscape of India")
    
    st.markdown("""
    <div class='story-text'>
    India's education system is one of the largest in the world, serving over 250 million students. 
    From ancient gurukuls to modern digital learning platforms, education in India has evolved significantly 
    while maintaining its core focus on knowledge and skill development. This data story explores the current 
    landscape of Indian education through key metrics and regional variations.
    </div>
    """, unsafe_allow_html=True)
    
    # Load and prepare data
    with st.spinner("Analyzing education data..."):
        try:
            df = load_education_data()
            
            if df is None or df.empty:
                st.error("Failed to load education data. Please check your data files.")
                return
                
        except Exception as e:
            st.error(f"Error loading education data: {e}")
            return
    
    # Overview section
    st.header("Educational Landscape Overview")
    
    # Key metrics with error handling
    try:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            try:
                literacy_rate = df['National Literacy Rate (%)'].iloc[0]
                if isinstance(literacy_rate, str):
                    literacy_rate = float(literacy_rate)
                if pd.isna(literacy_rate):
                    literacy_rate = 77.7  # Default value if NaN
                st.metric("Literacy Rate", f"{literacy_rate:.1f}%")
            except (ValueError, TypeError, IndexError, KeyError):
                # Use default if any error occurs
                literacy_rate = 77.7
                st.metric("Literacy Rate", f"{literacy_rate:.1f}%")
                
        with col2:
            try:
                enrollment_rate = df['Primary Enrollment Rate (%)'].iloc[0]
                if isinstance(enrollment_rate, str):
                    enrollment_rate = float(enrollment_rate)
                if pd.isna(enrollment_rate):
                    enrollment_rate = 96.2  # Default value if NaN
                st.metric("Primary Enrollment", f"{enrollment_rate:.1f}%")
            except (ValueError, TypeError, IndexError, KeyError):
                # Use default if any error occurs
                enrollment_rate = 96.2
                st.metric("Primary Enrollment", f"{enrollment_rate:.1f}%")
                
        with col3:
            try:
                universities = df['Number of Universities'].iloc[0]
                if isinstance(universities, str):
                    universities = universities.replace(',', '')
                if pd.isna(universities):
                    universities = 1043  # Default value if NaN
                st.metric("Universities", f"{universities}")
            except (ValueError, TypeError, IndexError, KeyError):
                # Use default if any error occurs
                universities = 1043
                st.metric("Universities", f"{universities}")
                
        with col4:
            try:
                higher_ed = df['Higher Education Enrollment (millions)'].iloc[0]
                if isinstance(higher_ed, str):
                    higher_ed = float(higher_ed)
                if pd.isna(higher_ed):
                    higher_ed = 38.5  # Default value if NaN
                st.metric("Students in Higher Ed", f"{higher_ed:.1f}M")
            except (ValueError, TypeError, IndexError, KeyError):
                # Use default if any error occurs
                higher_ed = 38.5
                st.metric("Students in Higher Ed", f"{higher_ed:.1f}M")
    except Exception as e:
        # Fallback to show all metrics with default values
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Literacy Rate", "77.7%")
        with col2:
            st.metric("Primary Enrollment", "96.2%")
        with col3:
            st.metric("Universities", "1,043")
        with col4:
            st.metric("Students in Higher Ed", "38.5M")
        st.info("Using default education metrics.")
    
    # Educational metrics tabs
    tabs = st.tabs(["Literacy & Enrollment", "Educational Infrastructure", "Quality Metrics", "Gender Parity"])
    
    # Tab 1: Literacy and Enrollment
    with tabs[0]:
        try:
            # Extract state-level data safely
            try:
                if 'State Names' in df.columns and 'State Literacy Rates (%)' in df.columns and 'State Primary Enrollment (%)' in df.columns and 'State Secondary Enrollment (%)' in df.columns and 'State Higher Ed Enrollment (%)' in df.columns:
                    state_names = df['State Names'].iloc[0].split(', ') if isinstance(df['State Names'].iloc[0], str) else []
                    literacy_rates = [float(x) for x in df['State Literacy Rates (%)'].iloc[0].split(', ')] if isinstance(df['State Literacy Rates (%)'].iloc[0], str) else []
                    primary_enrollment = [float(x) for x in df['State Primary Enrollment (%)'].iloc[0].split(', ')] if isinstance(df['State Primary Enrollment (%)'].iloc[0], str) else []
                    secondary_enrollment = [float(x) for x in df['State Secondary Enrollment (%)'].iloc[0].split(', ')] if isinstance(df['State Secondary Enrollment (%)'].iloc[0], str) else []
                    higher_ed_enrollment = [float(x) for x in df['State Higher Ed Enrollment (%)'].iloc[0].split(', ')] if isinstance(df['State Higher Ed Enrollment (%)'].iloc[0], str) else []
                    
                    # Ensure all lists have the same length
                    min_length = min(len(state_names), len(literacy_rates), len(primary_enrollment), 
                                    len(secondary_enrollment), len(higher_ed_enrollment))
                    
                    if min_length > 0:
                        states_df = pd.DataFrame({
                            'State': state_names[:min_length],
                            'Literacy Rate': literacy_rates[:min_length],
                            'Primary Enrollment': primary_enrollment[:min_length],
                            'Secondary Enrollment': secondary_enrollment[:min_length],
                            'Higher Ed Enrollment': higher_ed_enrollment[:min_length]
                        })
                        
                        # Sort by literacy rate
                        states_df = states_df.sort_values('Literacy Rate', ascending=False)
                        
                        # Create visualization
                        fig = px.bar(
                            states_df,
                            x='State',
                            y='Literacy Rate',
                            color='Literacy Rate',
                            title='Literacy Rates by State (%)',
                            color_continuous_scale='Viridis',
                            text='Literacy Rate'
                        )
                        fig = apply_dark_theme(fig)
                        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Enrollment rates comparison
                        enrollment_df = states_df.sort_values('Primary Enrollment', ascending=False).head(10)
                        
                        fig = px.bar(
                            enrollment_df,
                            x='State',
                            y=['Primary Enrollment', 'Secondary Enrollment', 'Higher Ed Enrollment'],
                            title='Education Enrollment by Level (%) - Top 10 States',
                            barmode='group',
                            labels={'value': 'Enrollment Rate (%)', 'variable': 'Education Level'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Use default state data
                        show_default_states_data()
                else:
                    # Required columns don't exist, use default data
                    show_default_states_data()
            except Exception as e:
                # Use default state data on exception
                show_default_states_data()
                
            # Educational progress metrics
            st.subheader("Education Progress Over Time")
            
            # Create years data safely
            try:
                if 'Literacy Rate Years' in df.columns and 'Literacy Rate History' in df.columns:
                    years_str = df['Literacy Rate Years'].iloc[0] 
                    rates_str = df['Literacy Rate History'].iloc[0]
                    
                    if isinstance(years_str, str) and isinstance(rates_str, str) and years_str and rates_str:
                        try:
                            years = [int(x) for x in years_str.split(', ')]
                            rates = [float(x) for x in rates_str.split(', ')]
                            
                            # Ensure both lists have the same length
                            min_length = min(len(years), len(rates))
                            
                            if min_length > 0:
                                # Create time series data
                                history_df = pd.DataFrame({
                                    'Year': years[:min_length],
                                    'Literacy Rate (%)': rates[:min_length]
                                })
                                
                                fig = px.line(
                                    history_df,
                                    x='Year',
                                    y='Literacy Rate (%)',
                                    title='National Literacy Rate Trend (%)',
                                    markers=True
                                )
                                fig = apply_dark_theme(fig)
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                # Use default historical data
                                show_default_historical_data()
                        except (ValueError, TypeError):
                            # Use default historical data on exception
                            show_default_historical_data()
                    else:
                        # Invalid data format
                        show_default_historical_data()
                else:
                    # Required columns don't exist
                    show_default_historical_data()
            except Exception:
                # Use default data on any error
                show_default_historical_data()
        except Exception as e:
            st.error(f"Error in literacy and enrollment visualization: {e}")
    
    # Tab 2: Educational Infrastructure
    with tabs[1]:
        try:
            # Extract infrastructure data safely
            primary_schools = df['Number of Primary Schools'].iloc[0] if 'Number of Primary Schools' in df.columns else 1500000
            secondary_schools = df['Number of Secondary Schools'].iloc[0] if 'Number of Secondary Schools' in df.columns else 230000
            colleges = df['Number of Colleges'].iloc[0] if 'Number of Colleges' in df.columns else 40000
            universities = df['Number of Universities'].iloc[0] if 'Number of Universities' in df.columns else 1000
            technical_institutions = df['Number of Technical Institutions'].iloc[0] if 'Number of Technical Institutions' in df.columns else 12000
            
            # Clean the data with proper error handling
            try:
                primary_schools = int(float(str(primary_schools).replace(',', ''))) if not pd.isna(primary_schools) else 1500000
                secondary_schools = int(float(str(secondary_schools).replace(',', ''))) if not pd.isna(secondary_schools) else 230000
                colleges = int(float(str(colleges).replace(',', ''))) if not pd.isna(colleges) else 40000
                universities = int(float(str(universities).replace(',', ''))) if not pd.isna(universities) else 1000
                technical_institutions = int(float(str(technical_institutions).replace(',', ''))) if not pd.isna(technical_institutions) else 12000
            except (ValueError, TypeError):
                # Set default values if conversion fails
                primary_schools = 1500000
                secondary_schools = 230000
                colleges = 40000
                universities = 1000
                technical_institutions = 12000
            
            infra_data = {
                'Category': ['Primary Schools', 'Secondary Schools', 'Colleges', 'Universities', 'Technical Institutions'],
                'Count': [primary_schools, secondary_schools, colleges, universities, technical_institutions]
            }
            
            infra_df = pd.DataFrame(infra_data)
            
            fig = px.bar(
                infra_df,
                x='Category',
                y='Count',
                color='Category',
                title='Educational Institutions in India',
                color_discrete_sequence=get_color_palette(len(infra_df)),
                text='Count',
                log_y=True
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(texttemplate='%{text:,}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # Infrastructure distribution by region - with error handling
            try:
                regions_str = df['Regional Names'].iloc[0] if 'Regional Names' in df.columns else ""
                primary_schools_str = df['Regional Primary Schools'].iloc[0] if 'Regional Primary Schools' in df.columns else ""
                secondary_schools_str = df['Regional Secondary Schools'].iloc[0] if 'Regional Secondary Schools' in df.columns else ""
                colleges_str = df['Regional Colleges'].iloc[0] if 'Regional Colleges' in df.columns else ""
                population_str = df['Regional Population (millions)'].iloc[0] if 'Regional Population (millions)' in df.columns else ""
                
                if all(isinstance(x, str) and x for x in [regions_str, primary_schools_str, secondary_schools_str, colleges_str, population_str]):
                    regions = regions_str.split(', ')
                    primary_schools_list = [int(x.replace(',', '')) for x in primary_schools_str.split(', ')]
                    secondary_schools_list = [int(x.replace(',', '')) for x in secondary_schools_str.split(', ')]
                    colleges_list = [int(x.replace(',', '')) for x in colleges_str.split(', ')]
                    population_list = [float(x) for x in population_str.split(', ')]
                    
                    # Ensure all lists have the same length
                    min_length = min(len(regions), len(primary_schools_list), len(secondary_schools_list), 
                                    len(colleges_list), len(population_list))
                    
                    if min_length > 0:
                        region_df = pd.DataFrame({
                            'Region': regions[:min_length],
                            'Primary Schools': primary_schools_list[:min_length],
                            'Secondary Schools': secondary_schools_list[:min_length],
                            'Colleges': colleges_list[:min_length],
                            'Population (millions)': population_list[:min_length]
                        })
                        
                        # Normalize data for better comparison
                        region_df['Primary per Million'] = region_df['Primary Schools'] / region_df['Population (millions)']
                        region_df['Secondary per Million'] = region_df['Secondary Schools'] / region_df['Population (millions)']
                        region_df['Colleges per Million'] = region_df['Colleges'] / region_df['Population (millions)']
                        
                        fig = px.bar(
                            region_df,
                            x='Region',
                            y=['Primary per Million', 'Secondary per Million', 'Colleges per Million'],
                            title='Educational Institutions per Million Population by Region',
                            barmode='group',
                            labels={'value': 'Institutions per Million', 'variable': 'Institution Type'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Use default regional data
                        show_default_regional_data()
                else:
                    # Use default regional data
                    show_default_regional_data()
            except Exception as e:
                # Use default regional data on exception
                st.info(f"Could not display regional infrastructure distribution: {e}")
                show_default_regional_data()
            
            # Teacher-student ratios - with error handling
            try:
                primary_ratio = df['Teacher-Student Ratio Primary'].iloc[0] if 'Teacher-Student Ratio Primary' in df.columns else "1:30"
                secondary_ratio = df['Teacher-Student Ratio Secondary'].iloc[0] if 'Teacher-Student Ratio Secondary' in df.columns else "1:25"
                higher_ed_ratio = df['Teacher-Student Ratio Higher Ed'].iloc[0] if 'Teacher-Student Ratio Higher Ed' in df.columns else "1:20"
                
                # Extract ratio values with better error handling
                try:
                    primary_ratio_val = float(primary_ratio.replace('1:', '')) if isinstance(primary_ratio, str) and ':' in primary_ratio else 30
                    secondary_ratio_val = float(secondary_ratio.replace('1:', '')) if isinstance(secondary_ratio, str) and ':' in secondary_ratio else 25
                    higher_ed_ratio_val = float(higher_ed_ratio.replace('1:', '')) if isinstance(higher_ed_ratio, str) and ':' in higher_ed_ratio else 20
                except (ValueError, TypeError, AttributeError):
                    # Default values if parsing fails
                    primary_ratio_val = 30
                    secondary_ratio_val = 25
                    higher_ed_ratio_val = 20
                
                st.subheader("Teacher-Student Ratios")
                
                ratio_data = {
                    'Level': ['Primary', 'Secondary', 'Higher Education'],
                    'Teacher-Student Ratio': [primary_ratio_val, secondary_ratio_val, higher_ed_ratio_val]
                }
                
                ratio_df = pd.DataFrame(ratio_data)
                
                fig = px.bar(
                    ratio_df,
                    x='Level',
                    y='Teacher-Student Ratio',
                    color='Level',
                    title='Teacher-Student Ratio by Education Level',
                    color_discrete_sequence=get_color_palette(len(ratio_df)),
                    text='Teacher-Student Ratio'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='1:%{text:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                # Create default teacher-student ratio visualization
                primary_ratio_val = 30
                secondary_ratio_val = 25
                higher_ed_ratio_val = 20
                
                st.subheader("Teacher-Student Ratios")
                
                ratio_data = {
                    'Level': ['Primary', 'Secondary', 'Higher Education'],
                    'Teacher-Student Ratio': [primary_ratio_val, secondary_ratio_val, higher_ed_ratio_val]
                }
                
                ratio_df = pd.DataFrame(ratio_data)
                
                fig = px.bar(
                    ratio_df,
                    x='Level',
                    y='Teacher-Student Ratio',
                    color='Level',
                    title='Teacher-Student Ratio by Education Level (Default Data)',
                    color_discrete_sequence=get_color_palette(len(ratio_df)),
                    text='Teacher-Student Ratio'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='1:%{text:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
                st.info(f"Using default teacher-student ratio data. Error: {e}")
        except Exception as e:
            st.error(f"Error in educational infrastructure visualization: {e}")
    
    # Tab 3: Quality Metrics
    with tabs[2]:
        try:
            # Extract quality metrics safely
            pisa_reading = df['PISA Reading Score'].iloc[0] if 'PISA Reading Score' in df.columns else "0"
            pisa_math = df['PISA Math Score'].iloc[0] if 'PISA Math Score' in df.columns else "0"
            pisa_science = df['PISA Science Score'].iloc[0] if 'PISA Science Score' in df.columns else "0"
            innovation_index = df['Global Innovation Index'].iloc[0] if 'Global Innovation Index' in df.columns else "0/100"
            higher_ed_rank = df['Higher Education Quality Rank'].iloc[0] if 'Higher Education Quality Rank' in df.columns else "0/0"
            
            # Convert to numeric values
            pisa_reading_val = float(pisa_reading) if isinstance(pisa_reading, str) else 0
            pisa_math_val = float(pisa_math) if isinstance(pisa_math, str) else 0
            pisa_science_val = float(pisa_science) if isinstance(pisa_science, str) else 0
            innovation_index_val = float(innovation_index.split('/')[0]) if isinstance(innovation_index, str) else 0
            higher_ed_rank_val = float(higher_ed_rank.split('/')[0]) if isinstance(higher_ed_rank, str) else 0
            
            quality_data = {  # Unused variable
                'Metric': [
                    'PISA Reading Score', 'PISA Math Score', 'PISA Science Score', 
                    'Global Innovation Index', 'Higher Ed Quality Rank'
                ],
                'Score': [
                    pisa_reading_val, pisa_math_val, pisa_science_val,
                    innovation_index_val, higher_ed_rank_val
                ],
                'Category': [
                    'International Assessment', 'International Assessment', 'International Assessment',
                    'Innovation', 'Higher Education'
                ]
            }
            
#             quality_df = pd.DataFrame(quality_data)  # Unused variable
            
            # PISA scores comparison - with error handling
            try:
                countries_str = df['PISA Comparison Countries'].iloc[0] if 'PISA Comparison Countries' in df.columns else ""
                reading_str = df['PISA Comparison Reading'].iloc[0] if 'PISA Comparison Reading' in df.columns else ""
                math_str = df['PISA Comparison Math'].iloc[0] if 'PISA Comparison Math' in df.columns else ""
                science_str = df['PISA Comparison Science'].iloc[0] if 'PISA Comparison Science' in df.columns else ""
                
                if all(isinstance(x, str) and x for x in [countries_str, reading_str, math_str, science_str]):
                    countries = countries_str.split(', ')
                    reading_scores = [float(x) for x in reading_str.split(', ')]
                    math_scores = [float(x) for x in math_str.split(', ')]
                    science_scores = [float(x) for x in science_str.split(', ')]
                    
                    # Ensure all lists have the same length
                    min_length = min(len(countries), len(reading_scores), len(math_scores), len(science_scores))
                    
                    if min_length > 0:
                        # Create comparison data
                        pisa_df = pd.DataFrame({
                            'Country': countries[:min_length],
                            'Reading': reading_scores[:min_length],
                            'Mathematics': math_scores[:min_length],
                            'Science': science_scores[:min_length]
                        })
                        
                        fig = px.bar(
                            pisa_df,
                            x='Country',
                            y=['Reading', 'Mathematics', 'Science'],
                            title='PISA Score Comparison by Country',
                            barmode='group',
                            labels={'value': 'PISA Score', 'variable': 'Subject'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Show default PISA data
                        default_countries = ['OECD Average', 'China', 'Singapore', 'Japan', 'South Korea', 'India*']
                        default_reading = [487, 555, 549, 504, 514, 410]
                        default_math = [489, 591, 569, 527, 526, 400]
                        default_science = [489, 590, 551, 529, 519, 405]
                        
                        default_pisa_df = pd.DataFrame({
                            'Country': default_countries,
                            'Reading': default_reading,
                            'Mathematics': default_math,
                            'Science': default_science
                        })
                        
                        fig = px.bar(
                            default_pisa_df,
                            x='Country',
                            y=['Reading', 'Mathematics', 'Science'],
                            title='PISA Score Comparison by Country (Default Data)',
                            barmode='group',
                            labels={'value': 'PISA Score', 'variable': 'Subject'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                        st.info("Using default PISA comparison data. *India score is estimated.")
                else:
                    # Show default PISA data
                    default_countries = ['OECD Average', 'China', 'Singapore', 'Japan', 'South Korea', 'India*']
                    default_reading = [487, 555, 549, 504, 514, 410]
                    default_math = [489, 591, 569, 527, 526, 400]
                    default_science = [489, 590, 551, 529, 519, 405]
                    
                    default_pisa_df = pd.DataFrame({
                        'Country': default_countries,
                        'Reading': default_reading,
                        'Mathematics': default_math,
                        'Science': default_science
                    })
                    
                    fig = px.bar(
                        default_pisa_df,
                        x='Country',
                        y=['Reading', 'Mathematics', 'Science'],
                        title='PISA Score Comparison by Country (Default Data)',
                        barmode='group',
                        labels={'value': 'PISA Score', 'variable': 'Subject'}
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                    st.info("Using default PISA comparison data. *India score is estimated.")
            except Exception as e:
                # Show default PISA data even on exception
                default_countries = ['OECD Average', 'China', 'Singapore', 'Japan', 'South Korea', 'India*']
                default_reading = [487, 555, 549, 504, 514, 410]
                default_math = [489, 591, 569, 527, 526, 400]
                default_science = [489, 590, 551, 529, 519, 405]
                
                default_pisa_df = pd.DataFrame({
                    'Country': default_countries,
                    'Reading': default_reading,
                    'Mathematics': default_math,
                    'Science': default_science
                })
                
                fig = px.bar(
                    default_pisa_df,
                    x='Country',
                    y=['Reading', 'Mathematics', 'Science'],
                    title='PISA Score Comparison by Country (Default Data)',
                    barmode='group',
                    labels={'value': 'PISA Score', 'variable': 'Subject'}
                )
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
                st.info(f"Using default PISA comparison data due to error: {e}. *India score is estimated.")
            
            # Top universities - with error handling
            try:
                university_ranking = df['University Ranking'].iloc[0] if 'University Ranking' in df.columns else ""
                
                if isinstance(university_ranking, str) and university_ranking:
                    # Split ranking data into university names and their ranks
                    uni_data = [x.strip() for x in university_ranking.split(',')]
                    
                    if len(uni_data) > 0:
                        # Extract university name and rank
                        universities = []
                        ranks = []
                        
                        for item in uni_data:
                            parts = item.split('(')
                            if len(parts) == 2:
                                uni_name = parts[0].strip()
                                rank_str = parts[1].replace(')', '').strip()
                                
                                universities.append(uni_name)
                                
                                # Handle ranges like "150-200"
                                if '-' in rank_str:
                                    rank_range = rank_str.split('-')
                                    if len(rank_range) == 2:
                                        try:
                                            # Use the middle of the range
                                            lower = int(rank_range[0])
                                            upper = int(rank_range[1])
                                            ranks.append((lower + upper) / 2)
                                        except ValueError:
                                            ranks.append(1000)  # Default value for parsing error
                                else:
                                    try:
                                        ranks.append(float(rank_str))
                                    except ValueError:
                                        ranks.append(1000)  # Default value for parsing error
                        
                        if universities and ranks:
                            # Create university ranking dataframe
                            uni_df = pd.DataFrame({
                                'University': universities,
                                'Global Rank': ranks
                            }).sort_values('Global Rank')
                            
                            fig = px.bar(
                                uni_df.head(10),
                                x='University',
                                y='Global Rank',
                                title='Top Indian Universities - Global Rankings',
                                color='Global Rank',
                                color_continuous_scale='Viridis_r'  # Reversed scale: lower is better
                            )
                            fig = apply_dark_theme(fig)
                            fig.update_yaxes(autorange="reversed")  # Reverse y-axis so better ranks are higher
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            # Show default university ranking data
                            show_default_university_rankings()
                    else:
                        # Show default university ranking data
                        show_default_university_rankings()
                else:
                    # Show default university ranking data
                    show_default_university_rankings()
            except Exception as e:
                # Show default university ranking data on exception
                st.info(f"Could not display university rankings from data source: {e}")
                show_default_university_rankings()
        except Exception as e:
            st.error(f"Error in quality metrics visualization: {e}")
    
    # Tab 4: Gender Parity
    with tabs[3]:
        try:
            # Extract gender parity data safely
            primary_parity = df['Gender Parity Primary'].iloc[0] if 'Gender Parity Primary' in df.columns else 0.98
            secondary_parity = df['Gender Parity Secondary'].iloc[0] if 'Gender Parity Secondary' in df.columns else 0.95
            higher_ed_parity = df['Gender Parity Higher Ed'].iloc[0] if 'Gender Parity Higher Ed' in df.columns else 0.92
            
            # Convert to numeric values with proper error handling
            try:
                primary_parity_val = float(primary_parity) if not pd.isna(primary_parity) else 0.98
                secondary_parity_val = float(secondary_parity) if not pd.isna(secondary_parity) else 0.95
                higher_ed_parity_val = float(higher_ed_parity) if not pd.isna(higher_ed_parity) else 0.92
            except (ValueError, TypeError):
                # Set default values if conversion fails
                primary_parity_val = 0.98
                secondary_parity_val = 0.95
                higher_ed_parity_val = 0.92
            
            gender_data = {
                'Level': ['Primary', 'Secondary', 'Higher Education'],
                'Gender Parity Index': [primary_parity_val, secondary_parity_val, higher_ed_parity_val]
            }
            
            gender_df = pd.DataFrame(gender_data)
            
            fig = px.bar(
                gender_df,
                x='Level',
                y='Gender Parity Index',
                color='Level',
                title='Gender Parity Index by Education Level (1.0 = Perfect Parity)',
                color_discrete_sequence=get_color_palette(len(gender_df)),
                text='Gender Parity Index'
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            
            # Add a horizontal line at 1.0 (perfect parity)
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=1,
                x1=2.5,
                y1=1,
                line=dict(color="red", width=2, dash="dash")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Gender disparity by state - handle with care
            try:
                # First check if the necessary columns exist
                if 'State Names' in df.columns and 'State Female Literacy (%)' in df.columns and 'State Male Literacy (%)' in df.columns:
                    state_names = df['State Names'].iloc[0].split(', ') if isinstance(df['State Names'].iloc[0], str) else []
                    female_literacy = [float(x) for x in df['State Female Literacy (%)'].iloc[0].split(', ')] if isinstance(df['State Female Literacy (%)'].iloc[0], str) else []
                    male_literacy = [float(x) for x in df['State Male Literacy (%)'].iloc[0].split(', ')] if isinstance(df['State Male Literacy (%)'].iloc[0], str) else []
                    
                    # Ensure all lists have the same length
                    min_length = min(len(state_names), len(female_literacy), len(male_literacy))
                    
                    if min_length > 0:
                        state_gender_df = pd.DataFrame({
                            'State': state_names[:min_length],
                            'Female Literacy': female_literacy[:min_length],
                            'Male Literacy': male_literacy[:min_length]
                        })
                        
                        state_gender_df['Literacy Gap'] = state_gender_df['Male Literacy'] - state_gender_df['Female Literacy']
                        state_gender_df = state_gender_df.sort_values('Literacy Gap', ascending=False)
                        
                        fig = px.bar(
                            state_gender_df.head(10),
                            x='State',
                            y=['Male Literacy', 'Female Literacy'],
                            title='States with Highest Gender Literacy Gap',
                            barmode='group',
                            labels={'value': 'Literacy Rate (%)', 'variable': 'Gender'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Use default gender literacy data
                        show_default_gender_literacy()
                else:
                    # Required columns don't exist, use default data
                    show_default_gender_literacy()
            except Exception as e:
                # Use default gender literacy data on exception
                show_default_gender_literacy()
        except Exception as e:
            st.error(f"Error in gender parity visualization: {e}")
    
    # Educational challenges and opportunities
    st.header("Challenges & Future Directions")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚧 Key Challenges")
        st.markdown("""
        - **Accessibility gaps** between urban and rural areas
        - **Quality disparities** across states and socioeconomic groups
        - **High dropout rates** especially in secondary education
        - **Infrastructure deficits** in many government schools
        - **Gender gaps** persistent in certain states and communities
        - **Digital divide** limiting online education reach
        """)
    
    with col2:
        st.subheader("🌟 Future Opportunities")
        st.markdown("""
        - **National Education Policy 2020** reform implementation
        - **EdTech revolution** expanding digital learning access
        - **Skill development initiatives** aligning education with employment
        - **Public-private partnerships** improving infrastructure
        - **International collaborations** raising quality standards
        - **Inclusive education approaches** reducing inequality
        """)
    
    # Final summary
    st.markdown("""
    <div class='story-text'>
    India's education landscape shows remarkable progress alongside persistent challenges. The literacy rate has 
    improved significantly over decades, yet educational quality and access remain uneven across regions. 
    
    The data reveals both the scale of India's educational system and the ongoing work needed to fulfill the 
    promise of quality education for all. With policy reforms, technology integration, and focus on inclusive 
    growth, India's education sector is positioned for transformative change in the coming decades.
    </div>
    """, unsafe_allow_html=True) 

def show_default_university_rankings():
    """Display default university rankings when data is not available"""
    # Default university ranking data
    default_universities = [
        'IISc Bangalore', 'IIT Bombay', 'IIT Delhi', 'IIT Madras', 
        'IIT Kanpur', 'IIT Kharagpur', 'IIT Roorkee', 'JNU', 
        'Delhi University', 'BHU'
    ]
    default_ranks = [175, 212, 227, 285, 324, 348, 395, 487, 525, 614]
    
    # Create university ranking dataframe
    default_uni_df = pd.DataFrame({
        'University': default_universities,
        'Global Rank': default_ranks
    }).sort_values('Global Rank')
    
    fig = px.bar(
        default_uni_df,
        x='University',
        y='Global Rank',
        title='Top Indian Universities - Global Rankings (Default Data)',
        color='Global Rank',
        color_continuous_scale='Viridis_r'  # Reversed scale: lower is better
    )
    fig = apply_dark_theme(fig)
    fig.update_yaxes(autorange="reversed")  # Reverse y-axis so better ranks are higher
    st.plotly_chart(fig, use_container_width=True)
    st.info("Using default university ranking data. Approximate rankings based on QS World University Rankings.") 

def show_default_regional_data():
    """Display default regional data when data is not available"""
    # Default regional data
    default_regions = ['North', 'South', 'East', 'West', 'Central']
    default_primary_schools = [450000, 520000, 380000, 500000, 310000]
    default_secondary_schools = [82000, 95000, 68000, 88000, 54000]
    default_colleges = [9500, 12000, 8800, 11000, 7200]
    default_population = [400, 450, 350, 420, 300]
    
    # Create regional data dataframe
    default_regional_df = pd.DataFrame({
        'Region': default_regions,
        'Primary Schools': default_primary_schools,
        'Secondary Schools': default_secondary_schools,
        'Colleges': default_colleges,
        'Population (millions)': default_population
    })
    
    # Normalize data for better comparison
    default_regional_df['Primary per Million'] = default_regional_df['Primary Schools'] / default_regional_df['Population (millions)']
    default_regional_df['Secondary per Million'] = default_regional_df['Secondary Schools'] / default_regional_df['Population (millions)']
    default_regional_df['Colleges per Million'] = default_regional_df['Colleges'] / default_regional_df['Population (millions)']
    
    # First show absolute numbers
    fig = px.bar(
        default_regional_df,
        x='Region',
        y=['Primary Schools', 'Secondary Schools', 'Colleges'],
        title='Educational Institutions by Region (Default Data)',
        barmode='group',
        labels={'value': 'Number of Institutions', 'variable': 'Institution Type'},
        log_y=True
    )
    fig = apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    # Then show per million data
    fig = px.bar(
        default_regional_df,
        x='Region',
        y=['Primary per Million', 'Secondary per Million', 'Colleges per Million'],
        title='Educational Institutions per Million Population by Region (Default Data)',
        barmode='group',
        labels={'value': 'Institutions per Million', 'variable': 'Institution Type'}
    )
    fig = apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Using default regional data. Approximate counts based on estimated distribution.") 

def show_default_gender_literacy():
    """Display default gender literacy data by state"""
    default_gender_data = {
        'State': ['Rajasthan', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh', 'Jharkhand', 
                'Andhra Pradesh', 'Odisha', 'Gujarat', 'Karnataka', 'Maharashtra'],
        'Male Literacy': [87.9, 78.5, 81.8, 82.5, 79.7, 75.6, 83.2, 89.5, 85.9, 92.8],
        'Female Literacy': [65.5, 60.5, 66.1, 67.0, 64.7, 62.9, 70.5, 77.0, 73.5, 82.3]
    }
    
    default_gender_df = pd.DataFrame(default_gender_data)
    default_gender_df['Literacy Gap'] = default_gender_df['Male Literacy'] - default_gender_df['Female Literacy']
    default_gender_df = default_gender_df.sort_values('Literacy Gap', ascending=False)
    
    fig = px.bar(
        default_gender_df.head(10),
        x='State',
        y=['Male Literacy', 'Female Literacy'],
        title='States with Highest Gender Literacy Gap (Default Data)',
        barmode='group',
        labels={'value': 'Literacy Rate (%)', 'variable': 'Gender'}
    )
    fig = apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Using default gender literacy data by state.") 

def show_default_states_data():
    """Display default state data when data is not available"""
    # Default state data
    default_states = {
        'State': ['Kerala', 'Delhi', 'Himachal Pradesh', 'Uttarakhand', 'Maharashtra', 
                  'Tamil Nadu', 'Gujarat', 'Punjab', 'Karnataka', 'Andhra Pradesh'],
        'Literacy Rate': [94.0, 93.7, 92.5, 90.0, 89.8, 89.1, 89.0, 84.6, 82.8, 81.3],
        'Primary Enrollment': [98.3, 97.8, 98.1, 97.5, 96.2, 95.8, 94.7, 95.6, 94.9, 94.1],
        'Secondary Enrollment': [85.3, 84.2, 86.1, 83.7, 82.9, 81.8, 79.5, 83.2, 80.1, 79.8],
        'Higher Ed Enrollment': [32.4, 30.5, 31.2, 29.8, 28.7, 27.9, 25.2, 28.6, 26.4, 25.8]
    }
    
    default_states_df = pd.DataFrame(default_states)
    
    # Sort by literacy rate
    default_states_df = default_states_df.sort_values('Literacy Rate', ascending=False)
    
    # Create visualization
    fig = px.bar(
        default_states_df,
        x='State',
        y='Literacy Rate',
        color='Literacy Rate',
        title='Literacy Rates by State (%) - Default Data',
        color_continuous_scale='Viridis',
        text='Literacy Rate'
    )
    fig = apply_dark_theme(fig)
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
    # Enrollment rates comparison
    default_enrollment_df = default_states_df.sort_values('Primary Enrollment', ascending=False).head(10)
    
    fig = px.bar(
        default_enrollment_df,
        x='State',
        y=['Primary Enrollment', 'Secondary Enrollment', 'Higher Ed Enrollment'],
        title='Education Enrollment by Level (%) - Default Data',
        barmode='group',
        labels={'value': 'Enrollment Rate (%)', 'variable': 'Education Level'}
    )
    fig = apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Using default state education data.") 

def show_default_historical_data():
    """Display default historical literacy data"""
    default_years = [1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021]
    default_rates = [18.3, 28.3, 34.5, 43.6, 52.2, 64.8, 74.0, 77.7]
    
    default_history_df = pd.DataFrame({
        'Year': default_years,
        'Literacy Rate (%)': default_rates
    })
    
    fig = px.line(
        default_history_df,
        x='Year',
        y='Literacy Rate (%)',
        title='National Literacy Rate Trend (%) - Default Data',
        markers=True
    )
    fig = apply_dark_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Using default historical literacy data.") 
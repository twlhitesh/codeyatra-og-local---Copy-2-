import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import apply_dark_theme, load_historical_data, get_color_palette
import re

def generate_default_historical_data():
    """Generate default historical data when real data is insufficient"""
    default_data = [
        {
            'Era': 'Indus Valley Civilization', 
            'Time Period': '2600-1900 BCE', 
            'Major Events': 'Development of sophisticated urban centers like Harappa and Mohenjo-daro with advanced drainage systems and grid-based city planning.',
            'Cultural Developments': 'Development of early writing system (Indus script), craftwork, and seals with animal motifs.',
            'Timeline Year': -2600
        },
        {
            'Era': 'Vedic Period', 
            'Time Period': '1500-600 BCE', 
            'Major Events': 'Composition of the Vedas, emergence of Aryan culture in northern India.',
            'Religious Trends': 'Early Vedic rituals and sacrifices, development of Brahmanism.',
            'Timeline Year': -1500
        },
        {
            'Era': 'Mauryan Empire', 
            'Time Period': '322-185 BCE', 
            'Major Events': 'First major empire under Chandragupta Maurya, expanded by Ashoka after the Kalinga War.',
            'Cultural Developments': 'Spread of Buddhism, rock edicts and pillars of Ashoka.',
            'Timeline Year': -322
        },
        {
            'Era': 'Gupta Empire', 
            'Time Period': '320-550 CE', 
            'Major Events': 'Classical age of India under rulers like Chandragupta I, Samudragupta, and Chandragupta II.',
            'Scientific Advances': 'Mathematical innovations by Aryabhata, including calculation of pi and concept of zero.',
            'Timeline Year': 320
        },
        {
            'Era': 'Delhi Sultanate', 
            'Time Period': '1206-1526 CE', 
            'Major Events': 'Rule by five dynasties: Mamluk, Khalji, Tughlaq, Sayyid, and Lodi.',
            'Art & Architecture': 'Indo-Islamic architecture, including Qutub Minar and early mosques.',
            'Timeline Year': 1206
        },
        {
            'Era': 'Mughal Empire', 
            'Time Period': '1526-1857 CE', 
            'Major Events': 'Founded by Babur, reached zenith under Akbar, Shah Jahan, and Aurangzeb.',
            'Art & Architecture': 'Taj Mahal, Red Fort, miniature paintings, and integration of Persian and Indian styles.',
            'Timeline Year': 1526
        },
        {
            'Era': 'British Raj', 
            'Time Period': '1858-1947 CE', 
            'Major Events': 'Direct British crown rule after the 1857 revolt, growth of Indian nationalism.',
            'Political Developments': 'Formation of Indian National Congress, freedom struggle under Gandhi and other leaders.',
            'Timeline Year': 1858
        },
        {
            'Era': 'Republic of India', 
            'Time Period': '1950-Present', 
            'Major Events': 'Constitution adoption, five-year plans, economic liberalization in 1991.',
            'Technological Innovations': 'Space program, IT revolution, digital initiatives.',
            'Timeline Year': 1950
        }
    ]
    return pd.DataFrame(default_data)

def create_default_radar_chart(df, aspects, era_colors):
    """Create a default radar chart when real data is insufficient"""
    try:
        # Generate some default values for each era and aspect
        default_data = []
        
        # Get important eras (or all if fewer than 5)
        key_eras = ['Indus Valley Civilization', 'Mauryan Empire', 'Gupta Empire', 
                    'Mughal Empire', 'British Raj', 'Republic of India']
        
        # Filter to only include eras that exist in our dataframe
        available_eras = [era for era in key_eras if era in df['Era'].unique()]
        
        # If none match, just take the first few from the dataframe
        if not available_eras and not df.empty:
            available_eras = df['Era'].unique()[:min(5, len(df['Era'].unique()))]
        
        # Create default values for each era and aspect
        for era in available_eras:
            # Create different patterns for different types of eras
            if 'Ancient' in era or 'Valley' in era or 'Vedic' in era:
                # Ancient periods strong in cultural, religious, architectural
                values = {
                    'Cultural Developments': 4.5,
                    'Religious Trends': 4.0,
                    'Economic Systems': 2.5,
                    'Scientific Advances': 2.0,
                    'Art & Architecture': 4.0,
                    'Social Structure': 3.5,
                    'Military Developments': 2.0,
                    'Technological Innovations': 2.5
                }
            elif 'Empire' in era or 'Kingdom' in era:
                # Empires strong in military, administration, architecture
                values = {
                    'Cultural Developments': 3.5,
                    'Religious Trends': 3.0,
                    'Economic Systems': 4.0,
                    'Scientific Advances': 3.0,
                    'Art & Architecture': 4.5,
                    'Social Structure': 3.0,
                    'Military Developments': 4.5,
                    'Technological Innovations': 3.0
                }
            elif 'Modern' in era or 'Republic' in era or 'Contemporary' in era:
                # Modern periods strong in technology, science, economics
                values = {
                    'Cultural Developments': 3.0,
                    'Religious Trends': 2.0,
                    'Economic Systems': 4.5,
                    'Scientific Advances': 4.5,
                    'Art & Architecture': 3.0,
                    'Social Structure': 3.5,
                    'Military Developments': 3.0,
                    'Technological Innovations': 5.0
                }
            else:
                # Default balanced pattern
                values = {
                    'Cultural Developments': 3.0,
                    'Religious Trends': 3.0,
                    'Economic Systems': 3.0,
                    'Scientific Advances': 3.0,
                    'Art & Architecture': 3.0,
                    'Social Structure': 3.0,
                    'Military Developments': 3.0,
                    'Technological Innovations': 3.0
                }
            
            # Only keep aspects that were selected
            filtered_values = {aspect: values.get(aspect, 2.0) for aspect in aspects}
            
            for aspect, value in filtered_values.items():
                default_data.append({
                    'Era': era,
                    'Aspect': aspect,
                    'Count': value
                })
        
        # Create DataFrame and pivot table
        default_df = pd.DataFrame(default_data)
        
        if not default_df.empty:
            # Create pivot table
            aspect_pivot = default_df.pivot(index='Era', columns='Aspect', values='Count').fillna(0)
            
            # Create the visualization
            fig = go.Figure()
            
            # Add a trace for each era
            for era in aspect_pivot.index:
                values = [aspect_pivot.loc[era, aspect] if aspect in aspect_pivot.columns else 0 for aspect in aspects]
                
                # Close the polygon by repeating the first value
                values.append(values[0])
                categories_closed = aspects + [aspects[0]]
                
                # Get era color or use a default
                era_color = era_colors.get(era, '#888888')
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories_closed,
                    fill='toself',
                    name=era,
                    line_color=era_color
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                title="Historical Emphasis by Era (Representative Visualization)",
                height=600,
                margin=dict(l=10, r=10, t=50, b=10),
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            
            # Display the radar chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Add explanation about default data
            st.info("This is a representative visualization based on general historical patterns. The actual data for your selection is limited.")
        else:
            st.warning("Cannot create visualization. No data available.")
            
    except Exception as e:
        st.warning(f"Could not create default visualization: {str(e)}")
        # Provide textual fallback
        st.markdown("""
        <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
        <h4>Key Historical Developments in India</h4>
        
        <p>While visualization isn't available, here are key developments across India's history:</p>
        
        <ul>
          <li><strong>Scientific Innovations:</strong> From Aryabhata's astronomical calculations to the development of steel and the concept of zero</li>
          <li><strong>Architectural Marvels:</strong> From the precisely engineered cities of the Indus Valley to the Taj Mahal</li>
          <li><strong>Cultural Achievements:</strong> Sanskrit literature, classical music, dance forms, and art traditions that have continued for millennia</li>
          <li><strong>Religious Thought:</strong> Development of philosophical schools within Hinduism, Buddhism, Jainism and later synthesis with Islam</li>
          <li><strong>Administrative Systems:</strong> Innovations from the Arthashastra's statecraft to the Mughals' administrative systems and modern democracy</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def render():
    """Render the Historical Timeline chapter content"""
    st.title("📜 Historical Timeline of India")
    
    st.markdown("""
    <div class='story-text'>
    India's rich history spans over 5,000 years, from the ancient Indus Valley Civilization to the modern republic. 
    This journey through time showcases the rise and fall of powerful empires, cultural and scientific achievements, 
    religious movements, and social transformations that have shaped the world's largest democracy.
    </div>
    """, unsafe_allow_html=True)
    
    # Create default historical timeline data directly in the code
    default_data = [
        # Ancient Period
        {'Year': -2600, 'Era': 'Indus Valley Civilization', 'Event': 'Emergence of Harappa and Mohenjo-daro', 
         'Significance': 'First major urban civilization in South Asia', 'Region': 'Northwestern India and Pakistan', 
         'Key Figures': 'Unknown', 'Category': 'Ancient'},
        
        {'Year': -1500, 'Era': 'Vedic Period', 'Event': 'Arrival of Indo-Aryans and composition of the Vedas', 
         'Significance': 'Foundation of Hindu philosophy and practices', 'Region': 'Northern India', 
         'Key Figures': 'Vedic sages', 'Category': 'Ancient'},
        
        {'Year': -599, 'Era': 'Ancient India', 'Event': 'Birth of Mahavira, founder of Jainism', 
         'Significance': 'Establishment of Jainism', 'Region': 'Eastern India', 
         'Key Figures': 'Mahavira', 'Category': 'Ancient'},
        
        {'Year': -563, 'Era': 'Ancient India', 'Event': 'Birth of Gautama Buddha', 
         'Significance': 'Founding of Buddhism', 'Region': 'Northern India', 
         'Key Figures': 'Gautama Buddha', 'Category': 'Ancient'},
        
        {'Year': -326, 'Era': 'Ancient India', 'Event': 'Alexander the Great\'s invasion of India', 
         'Significance': 'First major Western contact with India', 'Region': 'Northwestern India', 
         'Key Figures': 'Alexander the Great, King Porus', 'Category': 'Ancient'},
        
        {'Year': -322, 'Era': 'Mauryan Empire', 'Event': 'Establishment of Mauryan Empire by Chandragupta Maurya', 
         'Significance': 'First major empire unifying most of India', 'Region': 'Northern and Central India', 
         'Key Figures': 'Chandragupta Maurya, Chanakya', 'Category': 'Ancient'},
        
        {'Year': -273, 'Era': 'Mauryan Empire', 'Event': 'Ashoka the Great becomes emperor', 
         'Significance': 'Spread of Buddhism and principles of non-violence', 'Region': 'Most of Indian subcontinent', 
         'Key Figures': 'Ashoka the Great', 'Category': 'Ancient'},
        
        {'Year': -185, 'Era': 'Post-Mauryan Period', 'Event': 'Fall of Mauryan Empire', 
         'Significance': 'Fragmentation of central authority', 'Region': 'Northern India', 
         'Key Figures': 'Pushyamitra Shunga', 'Category': 'Ancient'},
        
        {'Year': 320, 'Era': 'Gupta Empire', 'Event': 'Establishment of Gupta Empire', 
         'Significance': 'Golden Age of India - advancements in science, art, and literature', 'Region': 'Northern India', 
         'Key Figures': 'Chandragupta I', 'Category': 'Ancient'},
        
        {'Year': 375, 'Era': 'Gupta Empire', 'Event': 'Reign of Chandragupta II (Vikramaditya)', 
         'Significance': 'Peak of classical Indian civilization', 'Region': 'Northern and Central India', 
         'Key Figures': 'Chandragupta II', 'Category': 'Ancient'},
        
        # Medieval Period
        {'Year': 606, 'Era': 'Post-Gupta Period', 'Event': 'Harsha establishes empire in North India', 
         'Significance': 'Last major ancient Indian empire', 'Region': 'Northern India', 
         'Key Figures': 'Harsha', 'Category': 'Medieval'},
        
        {'Year': 712, 'Era': 'Medieval India', 'Event': 'First Arab invasion of Sindh', 
         'Significance': 'Beginning of Islamic influence in India', 'Region': 'Sindh (modern Pakistan)', 
         'Key Figures': 'Muhammad bin Qasim', 'Category': 'Medieval'},
        
        {'Year': 1206, 'Era': 'Delhi Sultanate', 'Event': 'Establishment of Delhi Sultanate', 
         'Significance': 'First Muslim dynasty to rule significant parts of India', 'Region': 'Northern India', 
         'Key Figures': 'Qutb-ud-din Aibak', 'Category': 'Medieval'},
        
        {'Year': 1336, 'Era': 'Vijayanagara Empire', 'Event': 'Establishment of Vijayanagara Empire', 
         'Significance': 'Major Hindu kingdom resisting Islamic expansion', 'Region': 'Southern India', 
         'Key Figures': 'Harihara I and Bukka Raya I', 'Category': 'Medieval'},
        
        {'Year': 1498, 'Era': 'Age of Exploration', 'Event': 'Vasco da Gama reaches Calicut', 
         'Significance': 'Beginning of European colonial interest in India', 'Region': 'Kerala (Southwest coast)', 
         'Key Figures': 'Vasco da Gama', 'Category': 'Medieval'},
        
        {'Year': 1526, 'Era': 'Mughal Empire', 'Event': 'First Battle of Panipat, establishment of Mughal Empire', 
         'Significance': 'Beginning of Mughal rule in India', 'Region': 'Northern India', 
         'Key Figures': 'Babur', 'Category': 'Medieval'},
        
        {'Year': 1556, 'Era': 'Mughal Empire', 'Event': 'Akbar becomes emperor', 
         'Significance': 'Peak of Mughal power and cultural synthesis', 'Region': 'Northern and Central India', 
         'Key Figures': 'Akbar', 'Category': 'Medieval'},
        
        # Colonial Period
        {'Year': 1600, 'Era': 'Colonial Era', 'Event': 'Formation of East India Company', 
         'Significance': 'Beginning of British commercial interests in India', 'Region': 'Eastern and Western coastal regions', 
         'Key Figures': 'Queen Elizabeth I', 'Category': 'Colonial'},
        
        {'Year': 1757, 'Era': 'Colonial Era', 'Event': 'Battle of Plassey', 
         'Significance': 'Beginning of British territorial control in India', 'Region': 'Bengal (Eastern India)', 
         'Key Figures': 'Robert Clive, Siraj ud-Daulah', 'Category': 'Colonial'},
        
        {'Year': 1857, 'Era': 'Colonial Era', 'Event': 'Indian Rebellion (First War of Independence)', 
         'Significance': 'First major uprising against British rule', 'Region': 'Northern and Central India', 
         'Key Figures': 'Mangal Pandey, Rani Lakshmibai, Bahadur Shah Zafar', 'Category': 'Colonial'},
        
        {'Year': 1858, 'Era': 'British Raj', 'Event': 'British Crown takes direct control of India', 
         'Significance': 'End of East India Company rule, beginning of British Raj', 'Region': 'All India', 
         'Key Figures': 'Queen Victoria', 'Category': 'Colonial'},
        
        {'Year': 1885, 'Era': 'Independence Movement', 'Event': 'Formation of Indian National Congress', 
         'Significance': 'Beginning of organized political movement for independence', 'Region': 'All India', 
         'Key Figures': 'A.O. Hume, Dadabhai Naoroji', 'Category': 'Colonial'},
        
        {'Year': 1915, 'Era': 'Independence Movement', 'Event': 'Gandhi returns to India from South Africa', 
         'Significance': 'Beginning of Gandhi\'s leadership in freedom struggle', 'Region': 'All India', 
         'Key Figures': 'Mahatma Gandhi', 'Category': 'Colonial'},
        
        {'Year': 1942, 'Era': 'Independence Movement', 'Event': 'Quit India Movement', 
         'Significance': 'Final major push for independence', 'Region': 'All India', 
         'Key Figures': 'Mahatma Gandhi', 'Category': 'Colonial'},
        
        # Modern Period
        {'Year': 1947, 'Era': 'Independence', 'Event': 'Independence and Partition of India', 
         'Significance': 'End of British rule, creation of India and Pakistan', 'Region': 'All India', 
         'Key Figures': 'Jawaharlal Nehru, Muhammad Ali Jinnah, Lord Mountbatten', 'Category': 'Modern'},
        
        {'Year': 1950, 'Era': 'Republic of India', 'Event': 'Constitution of India comes into effect', 
         'Significance': 'India becomes a sovereign democratic republic', 'Region': 'All India', 
         'Key Figures': 'Dr. B.R. Ambedkar, Rajendra Prasad', 'Category': 'Modern'},
        
        {'Year': 1991, 'Era': 'Economic Reforms', 'Event': 'Economic liberalization begins', 
         'Significance': 'Opening of Indian economy to global market', 'Region': 'All India', 
         'Key Figures': 'P.V. Narasimha Rao, Manmohan Singh', 'Category': 'Modern'},
        
        {'Year': 2014, 'Era': 'Modern India', 'Event': 'BJP forms majority government', 
         'Significance': 'Shift in political landscape', 'Region': 'All India', 
         'Key Figures': 'Narendra Modi', 'Category': 'Modern'},
        
        {'Year': 2023, 'Era': 'Modern India', 'Event': 'India becomes most populous country', 
         'Significance': 'Demographic milestone', 'Region': 'All India', 
         'Key Figures': 'Various', 'Category': 'Modern'}
    ]
    
    # Create DataFrame
    df = pd.DataFrame(default_data)
    
    # Process the data for visualization
    try:
        # Add additional computed columns
        df['Period'] = df['Year'].apply(lambda x: 'BCE' if x < 0 else 'CE')
        df['Display Year'] = df['Year'].apply(lambda x: f"{abs(x)} {'BCE' if x < 0 else 'CE'}")
        df['Time Period'] = df['Display Year']
        
        # Create categories for the different periods
        df['Category'] = 'Other'
        df.loc[df['Year'] < 600, 'Category'] = 'Ancient'
        df.loc[(df['Year'] >= 600) & (df['Year'] < 1757), 'Category'] = 'Medieval'
        df.loc[(df['Year'] >= 1757) & (df['Year'] < 1947), 'Category'] = 'Colonial'
        df.loc[df['Year'] >= 1947, 'Category'] = 'Modern'
        
        # Prepare the Major Events column by combining Event and Significance
        df['Major Events'] = df.apply(
            lambda row: f"{row['Event']}. {row['Significance']}" if pd.notna(row['Significance']) else row['Event'], 
            axis=1
        )
        
        # Sort by year for chronological display
        df = df.sort_values('Year')
    except Exception as e:
        st.error(f"Error processing historical data: {e}")
        return
    
    # Define color scheme for different time periods
    period_colors = {
        "Ancient": "#E3663E",
        "Medieval": "#6C8CBF",
        "Colonial": "#4D9078",
        "Modern": "#FFC857"
    }
    
    # Create era colors for the individual eras
    era_colors = {}
    unique_eras = df['Era'].unique()
    color_palette = get_color_palette(len(unique_eras))
    for i, era in enumerate(unique_eras):
        era_colors[era] = color_palette[i]
    
    # INTERACTIVE TIMELINE SECTION
    st.header("Interactive Timeline of Indian History")
    
    st.markdown("""
    <div class='story-text'>
    Use the slider below to explore key eras in Indian history. Each period represents a major 
    historical era with unique cultural, political, and social characteristics.
    </div>
    """, unsafe_allow_html=True)
    
    # Create a slider for timeline navigation
    selected_index = st.slider(
        "Explore Historical Periods",
        min_value=0,
        max_value=len(df) - 1,
        value=0,
        format=None
    )
    
    # Get the selected era data
    selected_era = df.iloc[selected_index]
    
    # Display era information in two columns
    col1, col2 = st.columns([1, 2])
    
    # Left column: Basic information
    with col1:
        with st.container():
            # Era name with appropriate styling
            era_name = selected_era['Era'] if 'Era' in selected_era else "Unknown Era"
            era_color = era_colors.get(era_name, "#FFFFFF")
            st.markdown(f"<h2 style='color:{era_color}'>{era_name}</h2>", unsafe_allow_html=True)
            
            # Time period with BCE/CE notation
            if 'Display Year' in selected_era:
                st.markdown(f"**Period:** {selected_era['Display Year']}")
            
            # Key figures if available
            if 'Key Figures' in selected_era and pd.notna(selected_era['Key Figures']):
                st.markdown(f"**Key Figures:** {selected_era['Key Figures']}")
            
            # Region if available
            if 'Region' in selected_era and pd.notna(selected_era['Region']):
                st.markdown(f"**Region:** {selected_era['Region']}")
            
            # Create era badge based on category
            badge_colors = {
                'Ancient': '#9C6644',
                'Classical': '#4C9900',
                'Medieval': '#9966CC',
                'Colonial': '#3366CC',
                'Modern': '#3366CC',
                'Other': '#888888'
            }
            
            # Display period badge
            period_category = selected_era.get('Category', 'Other')
            if period_category in badge_colors:
                st.markdown(f"""
                <div style='margin-top:20px;'>
                    <span style='background-color:{badge_colors[period_category]}33;
                    color:{badge_colors[period_category]};
                    padding:5px 15px;border-radius:20px;font-size:0.9rem;'>
                    {period_category} Period
                    </span>
                </div>
                """, unsafe_allow_html=True)
    
    # Right column: Detailed information
    with col2:
        # Create tabs for different aspects
        tabs = st.tabs(["Major Events", "Culture & Society", "Economy & Technology"])
        
        # Tab 1: Major Events
        with tabs[0]:
            st.markdown(f"### Key Historical Events")
            
            if 'Event' in selected_era and pd.notna(selected_era['Event']):
                st.markdown(f"**Event:** {selected_era['Event']}")
                
                if 'Significance' in selected_era and pd.notna(selected_era['Significance']):
                    st.markdown(f"**Significance:** {selected_era['Significance']}")
            else:
                st.info("No major events information available for this period.")
            
            if 'Region' in selected_era and pd.notna(selected_era['Region']):
                st.markdown("#### Region")
                st.markdown(f"{selected_era['Region']}")
        
        # Tab 2: Culture & Society
        with tabs[1]:
            st.markdown("### Cultural & Social Context")
            
            # Generate content based on the era
            era_name = selected_era.get('Era', '')
            period = selected_era.get('Category', 'Other')
            
            cultural_content = ""
            
            if period == 'Ancient':
                if 'Indus Valley' in era_name:
                    cultural_content = """
                    The Indus Valley Civilization developed a sophisticated urban culture with standardized weights, measures, and a writing system that remains undeciphered. Archaeological evidence shows advanced planning in cities like Harappa and Mohenjo-daro with impressive drainage systems and grid layouts.
                    """
                elif 'Vedic' in era_name:
                    cultural_content = """
                    The Vedic period saw the composition of the Vedas, establishment of early Hinduism, and formation of the caste system. Society was organized around ritual sacrifices performed by Brahmin priests, and early philosophical concepts that would influence Indian thought for millennia were developed.
                    """
                elif 'Mauryan' in era_name:
                    cultural_content = """
                    The Mauryan period witnessed the spread of Buddhism under Emperor Ashoka following the Kalinga War. This era produced significant cultural developments including rock-cut edicts, pillars with lion capitals (now India's national emblem), and early Buddhist art forms.
                    """
                else:
                    cultural_content = """
                    Ancient Indian society developed sophisticated philosophical systems, early scientific knowledge, and diverse artistic traditions. Religious developments included early Hinduism, Buddhism, and Jainism, while social structures were organized around the varna (caste) system.
                    """
            
            elif period == 'Medieval':
                if 'Delhi Sultanate' in era_name:
                    cultural_content = """
                    The Delhi Sultanate period introduced Indo-Islamic architecture and cultural forms. Persian, Turkish, and Arabic influences blended with existing Indian traditions in art, literature, and music. The Qutub Minar and early mosques represent the architectural achievements of this period.
                    """
                elif 'Mughal' in era_name:
                    cultural_content = """
                    The Mughal era represents a high point of Indo-Islamic cultural synthesis. Persian was the court language, and miniature painting flourished. Architecture reached its zenith with monuments like the Taj Mahal and Red Fort, while music, literature, and cuisine all developed distinctive Mughal styles that continue to influence Indian culture.
                    """
                else:
                    cultural_content = """
                    Medieval India saw significant cultural synthesis between Hindu and Islamic traditions. Regional kingdoms developed distinctive architectural styles, literary traditions, and artistic expressions. This period witnessed the growth of Bhakti and Sufi movements emphasizing personal devotion and challenging social hierarchies.
                    """
            
            elif period == 'Colonial':
                cultural_content = """
                The colonial period introduced Western education, legal systems, and cultural influences. This era saw the emergence of reform movements addressing social practices like sati and child marriage. Modern Indian literature developed in both regional languages and English, while art forms began incorporating Western techniques alongside traditional styles.
                """
            
            elif period == 'Modern':
                cultural_content = """
                Modern India has developed a vibrant blend of traditional and contemporary cultural expressions. Cinema (Bollywood and regional industries), literature, and arts reflect India's diverse heritage while engaging with global trends. Cultural policy has emphasized both preserving traditional forms and promoting innovation in the arts.
                """
            
            st.markdown(cultural_content)
        
        # Tab 3: Economy & Technology
        with tabs[2]:
            st.markdown("### Economic & Technological Context")
            
            # Generate content based on the era
            era_name = selected_era.get('Era', '')
            period = selected_era.get('Category', 'Other')
            
            economic_content = ""
            
            if period == 'Ancient':
                if 'Indus Valley' in era_name:
                    economic_content = """
                    The Indus Valley Civilization had an advanced trading economy with standardized weights and measures for commerce. They developed sophisticated urban planning, drainage systems, and water management technologies, including docks at cities like Lothal for maritime trade with Mesopotamia.
                    """
                elif 'Vedic' in era_name:
                    economic_content = """
                    The early Vedic economy was primarily pastoral, later transitioning to agriculture as iron technology developed. The late Vedic period saw the emergence of territorial states (mahajanapadas), urbanization, and craft specialization with guilds (shrenis) organizing production.
                    """
                elif 'Mauryan' in era_name:
                    economic_content = """
                    The Mauryan economy featured centralized control of key industries, standardized currency, and extensive trade networks. Administrative innovations included sophisticated taxation systems, bureaucracy, and infrastructure development, as described in Kautilya's Arthashastra.
                    """
                elif 'Gupta' in era_name:
                    economic_content = """
                    The Gupta period saw advances in mathematics (including the concept of zero), astronomy, and metallurgy (as evidenced by the rust-resistant Iron Pillar of Delhi). The economy flourished through agriculture, crafts, and extensive trade networks reaching Southeast Asia, Rome, and China.
                    """
                else:
                    economic_content = """
                    Ancient Indian economies developed sophisticated trade networks, standardized currency systems, and specialized craft production. Technological innovations included advances in metallurgy, textile production, and water management systems for agriculture.
                    """
            
            elif period == 'Medieval':
                economic_content = """
                Medieval Indian economies were primarily agricultural with significant international trade. Technological innovations included improvements in textile production (particularly cotton and silk), shipbuilding, and metallurgy. Regional trading networks connected with broader Indian Ocean and Central Asian commercial systems.
                """
            
            elif period == 'Colonial':
                economic_content = """
                The colonial economy was restructured to serve British interests, with railway networks, telegraph systems, and modern infrastructure introduced primarily for resource extraction. Traditional industries declined while plantation agriculture (tea, cotton, indigo) expanded. Late colonial period saw limited industrialization focused on textiles and steel.
                """
            
            elif period == 'Modern':
                economic_content = """
                Post-independence India initially followed a planned economic model before transitioning to liberalization in 1991. Technological developments include a space program, nuclear capabilities, and a globally significant IT sector. Digital initiatives like Aadhaar (biometric ID) and UPI (payment system) represent recent innovations in governance and financial inclusion.
                """
            
            st.markdown(economic_content)
    
    # VISUAL TIMELINE SECTION
    st.header("Visual Timeline of Indian History")
    
    # Create tabs for different time periods
    timeline_tabs = st.tabs([
        "Ancient (Before 600 CE)", 
        "Medieval (600-1757 CE)", 
        "Colonial (1757-1947)",
        "Modern (1947-Present)"
    ])
    
    # ANCIENT PERIOD TAB
    with timeline_tabs[0]:
        st.markdown(f"<h3 style='color:{period_colors['Ancient']}'>Ancient India</h3>", unsafe_allow_html=True)
        
        # Filter data for ancient period
        ancient_df = df[df['Category'] == 'Ancient'].copy()
        
        if not ancient_df.empty:
            # Create visualization
            fig = go.Figure()
            
            # Add events as scatter points
            fig.add_trace(go.Scatter(
                x=ancient_df['Year'],
                y=[1] * len(ancient_df),
                mode='markers+text',
                marker=dict(
                    symbol='circle',
                    size=16,
                    color=period_colors['Ancient'],
                    line=dict(width=2, color='white')
                ),
                text=ancient_df['Era'],
                textposition="top center",
                hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
            ))
            
            # Add a line connecting all points
            fig.add_trace(go.Scatter(
                x=ancient_df['Year'],
                y=[1] * len(ancient_df),
                mode='lines',
                line=dict(color=period_colors['Ancient'], width=3),
                hoverinfo='skip'
            ))
            
            # Update layout
            fig.update_layout(
                title="Ancient Indian Timeline",
                showlegend=False,
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    range=[0.5, 1.5]
                ),
                xaxis=dict(
                    title="Year (Negative values represent BCE)",
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                height=250,
                margin=dict(l=10, r=10, t=50, b=30),
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            
            # Display timeline
            st.plotly_chart(fig, use_container_width=True)
            
            # Display key events in a formatted table
            st.subheader("Key Events in Ancient India")
            
            for _, row in ancient_df.iterrows():
                st.markdown(f"""
                <div style='margin-bottom:15px; padding:10px; border-radius:5px; background-color:rgba(227, 102, 62, 0.1);'>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='font-weight:bold; color:{period_colors["Ancient"]};'>{row['Era']}</span>
                        <span style='color:#AAAAAA;'>{row['Display Year']}</span>
                    </div>
                    <div style='margin-top:5px;'>
                        <span>{row['Event']}</span>
                    </div>
                    <div style='margin-top:5px; font-size:0.9em;'>
                        {row['Significance'] if pd.notna(row['Significance']) else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available for the ancient period.")
    
    # MEDIEVAL PERIOD TAB
    with timeline_tabs[1]:
        st.markdown(f"<h3 style='color:{period_colors['Medieval']}'>Medieval India</h3>", unsafe_allow_html=True)
        
        # Filter data for medieval period
        medieval_df = df[df['Category'] == 'Medieval'].copy()
        
        if not medieval_df.empty:
            # Create visualization
            fig = go.Figure()
            
            # Add events as scatter points
            fig.add_trace(go.Scatter(
                x=medieval_df['Year'],
                y=[1] * len(medieval_df),
                mode='markers+text',
                marker=dict(
                    symbol='circle',
                    size=16,
                    color=period_colors['Medieval'],
                    line=dict(width=2, color='white')
                ),
                text=medieval_df['Era'],
                textposition="top center",
                hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
            ))
            
            # Add a line connecting all points
            fig.add_trace(go.Scatter(
                x=medieval_df['Year'],
                y=[1] * len(medieval_df),
                mode='lines',
                line=dict(color=period_colors['Medieval'], width=3),
                hoverinfo='skip'
            ))
            
            # Configure the layout
            fig.update_layout(
                showlegend=False,
                xaxis=dict(
                    title="Year (CE)",
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)',
                    tickfont=dict(color='rgba(255,255,255,0.7)')
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    range=[0.5, 1.5]
                ),
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
                title=dict(
                    text="Medieval Period in India (600-1757 CE)",
                    font=dict(color='rgba(255,255,255,0.9)'),
                    x=0.5
                )
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display era summaries
            st.markdown("### Key Developments in Medieval India")
            st.markdown("""
            Medieval India saw the establishment of Islamic sultanates and the Mughal Empire, with significant cultural synthesis between Hindu and Islamic traditions. 
            This period witnessed remarkable developments in art, architecture, and religious philosophy, including the growth of Bhakti and Sufi movements.
            """)
            
            # Show the main events in a table format
            st.markdown("### Timeline of Major Events")
            
            # Create a dataframe for display
            display_df = medieval_df[['Display Year', 'Era', 'Major Events']].copy()
            display_df.columns = ['Year', 'Era', 'Major Events']
            
            # Show the table
            st.table(display_df)
        else:
            st.info("No data available for the medieval period.")
    
    # COLONIAL PERIOD TAB
    with timeline_tabs[2]:
        st.markdown(f"<h3 style='color:{period_colors['Colonial']}'>Colonial India</h3>", unsafe_allow_html=True)
        
        # Filter data for colonial period
        colonial_df = df[df['Category'] == 'Colonial'].copy()
        
        if not colonial_df.empty:
            # Create visualization
            fig = go.Figure()
            
            # Add events as scatter points
            fig.add_trace(go.Scatter(
                x=colonial_df['Year'],
                y=[1] * len(colonial_df),
                mode='markers+text',
                marker=dict(
                    symbol='circle',
                    size=16,
                    color=period_colors['Colonial'],
                    line=dict(width=2, color='white')
                ),
                text=colonial_df['Era'],
                textposition="top center",
                hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
            ))
            
            # Add a line connecting all points
            fig.add_trace(go.Scatter(
                x=colonial_df['Year'],
                y=[1] * len(colonial_df),
                mode='lines',
                line=dict(color=period_colors['Colonial'], width=3),
                hoverinfo='skip'
            ))
            
            # Configure the layout
            fig.update_layout(
                showlegend=False,
                xaxis=dict(
                    title="Year (CE)",
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)',
                    tickfont=dict(color='rgba(255,255,255,0.7)')
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    range=[0.5, 1.5]
                ),
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
                title=dict(
                    text="Colonial Period in India (1757-1947)",
                    font=dict(color='rgba(255,255,255,0.9)'),
                    x=0.5
                )
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display era summaries
            st.markdown("### Key Developments in Colonial India")
            st.markdown("""
            The Colonial period marked British rule over the Indian subcontinent, beginning with East India Company rule and later direct British Crown control.
            This era saw significant social, economic, and political transformations, including the freedom struggle led by figures like Mahatma Gandhi.
            """)
            
            # Show the main events in a table format
            st.markdown("### Timeline of Major Events")
            
            # Create a dataframe for display
            display_df = colonial_df[['Display Year', 'Era', 'Major Events']].copy()
            display_df.columns = ['Year', 'Era', 'Major Events']
            
            # Show the table
            st.table(display_df)
        else:
            st.info("No data available for the colonial period.")
    
    # MODERN PERIOD TAB
    with timeline_tabs[3]:
        st.markdown(f"<h3 style='color:{period_colors['Modern']}'>Modern India</h3>", unsafe_allow_html=True)
        
        # Filter data for modern period
        modern_df = df[df['Category'] == 'Modern'].copy()
        
        if not modern_df.empty:
            # Create visualization
            fig = go.Figure()
            
            # Add events as scatter points
            fig.add_trace(go.Scatter(
                x=modern_df['Year'],
                y=[1] * len(modern_df),
                mode='markers+text',
                marker=dict(
                    symbol='circle',
                    size=16,
                    color=period_colors['Modern'],
                    line=dict(width=2, color='white')
                ),
                text=modern_df['Era'],
                textposition="top center",
                hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
            ))
            
            # Add a line connecting all points
            fig.add_trace(go.Scatter(
                x=modern_df['Year'],
                y=[1] * len(modern_df),
                mode='lines',
                line=dict(color=period_colors['Modern'], width=3),
                hoverinfo='skip'
            ))
            
            # Configure the layout
            fig.update_layout(
                showlegend=False,
                xaxis=dict(
                    title="Year (CE)",
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)',
                    tickfont=dict(color='rgba(255,255,255,0.7)')
                ),
                yaxis=dict(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    range=[0.5, 1.5]
                ),
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
                title=dict(
                    text="Modern India (1947-Present)",
                    font=dict(color='rgba(255,255,255,0.9)'),
                    x=0.5
                )
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display era summaries
            st.markdown("### Key Developments in Modern India")
            st.markdown("""
            Modern India has transformed from a newly independent nation to a major global power with significant economic, technological, and cultural influence.
            Key developments include the adoption of the Constitution, economic liberalization, technological advances, and growing international prominence.
            """)
            
            # Show the main events in a table format
            st.markdown("### Timeline of Major Events")
            
            # Create a dataframe for display
            display_df = modern_df[['Display Year', 'Era', 'Major Events']].copy()
            display_df.columns = ['Year', 'Era', 'Major Events']
            
            # Show the table
            st.table(display_df)
        else:
            st.info("No data available for the modern period.")
    
    # Add final summary section
    st.header("The Legacy of Indian History")
    
    st.markdown("""
    <div class='story-text'>
    India's historical journey represents one of humanity's most remarkable continuous civilizational stories. 
    From the urban planning of Harappa to the democratic institutions of modern India, the nation's history 
    demonstrates remarkable adaptability and cultural synthesis. Each historical period has left lasting legacies 
    that continue to shape contemporary Indian society, politics, art, and thought.
    
    This tapestry of historical experiences - empires rising and falling, religious movements spreading, cultural 
    and scientific achievements flourishing - forms the foundation for understanding the complexity and resilience 
    of modern India.
    </div>
    """, unsafe_allow_html=True) 
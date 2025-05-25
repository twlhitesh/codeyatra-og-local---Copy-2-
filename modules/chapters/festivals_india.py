import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import apply_dark_theme, style_matplotlib_for_dark, get_color_palette
import re

def render():
    """Render the Festivals of India chapter content"""
    st.title("🪔 Festivals of India")
    
    st.markdown("""
    <div class='story-text'>
    India's vibrant cultural landscape is illuminated by its diverse festivals, celebrated throughout the year across 
    the country. These festivals reflect the rich tapestry of religions, cultures, and traditions that define India's 
    unique identity. From the colorful festivities of Holi to the spiritual celebrations of Diwali, each festival 
    represents a unique aspect of India's cultural heritage.
    </div>
    """, unsafe_allow_html=True)
    
    # Create comprehensive festivals dataset directly in the code
    festivals_data = [
        {
            'Festival': 'Diwali',
            'Religion/Type': 'Hindu',
            'Description': 'Festival of lights celebrating the victory of light over darkness and good over evil',
            'Season': 'October-November',
            'Primary States': 'All India',
            'Participants (millions)': 800,
            'Economic Impact (Millions USD)': 7200,
            'Duration (days)': 5,
            'Tourist Attraction Level': 'Very High',
            'Global Celebrations': '30+ countries',
            'Environmental Impact': 'High',
            'Practices': 'Lighting diyas (oil lamps), fireworks, family gatherings, worship of Goddess Lakshmi',
            'Special Foods': 'Sweets like ladoo, barfi, and savory snacks like chakli and mathri',
            'Traditional Attire': 'New clothes, especially traditional wear like sarees, kurta-pajama',
            'Cultural Significance': 'Symbolizes prosperity, joy, and the triumph of light over darkness'
        },
        {
            'Festival': 'Holi',
            'Religion/Type': 'Hindu',
            'Description': 'Festival of colors celebrating the arrival of spring and triumph of good over evil',
            'Season': 'February-March',
            'Primary States': 'North and East India primarily, but celebrated across India',
            'Participants (millions)': 600,
            'Economic Impact (Millions USD)': 1500,
            'Duration (days)': 2,
            'Tourist Attraction Level': 'Very High',
            'Global Celebrations': '20+ countries',
            'Environmental Impact': 'Moderate to High',
            'Practices': 'Playing with colored powders and water, bonfires (Holika Dahan), community celebrations',
            'Special Foods': 'Gujiya, thandai, bhang, malpua, and other sweets',
            'Traditional Attire': 'White clothes (to show colors better), casual wear',
            'Cultural Significance': 'Celebrates love, forgiveness, and the renewal of relationships'
        },
        {
            'Festival': 'Eid ul-Fitr',
            'Religion/Type': 'Islamic',
            'Description': 'Celebration marking the end of Ramadan, the month of fasting',
            'Season': 'Variable (Islamic calendar)',
            'Primary States': 'All India with significant Muslim populations',
            'Participants (millions)': 200,
            'Economic Impact (Millions USD)': 2000,
            'Duration (days)': 3,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '150+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Prayer at mosques, family gatherings, charity (zakat al-fitr), exchanging gifts',
            'Special Foods': 'Biryani, sevaiyan (sweet vermicelli), sheer khurma, kebabs',
            'Traditional Attire': 'New clothes, men wear kurta-pajama or sherwani, women wear salwar kameez or sarees',
            'Cultural Significance': 'Emphasizes charity, community, and gratitude'
        },
        {
            'Festival': 'Durga Puja',
            'Religion/Type': 'Hindu',
            'Description': 'Worship of goddess Durga celebrating her victory over the demon Mahishasura',
            'Season': 'September-October',
            'Primary States': 'West Bengal, Assam, Odisha, Tripura',
            'Participants (millions)': 100,
            'Economic Impact (Millions USD)': 1200,
            'Duration (days)': 10,
            'Tourist Attraction Level': 'High',
            'Global Celebrations': '10+ countries',
            'Environmental Impact': 'Moderate to High',
            'Practices': 'Elaborate pandals (temporary temples), idol worship, cultural performances, processions',
            'Special Foods': 'Bhog (community feast), sweets like sandesh, rosogolla, and mishti doi',
            'Traditional Attire': 'Women wear sarees (especially red and white), men wear dhoti-kurta or kurta-pajama',
            'Cultural Significance': 'Celebrates feminine divine power and the triumph of good over evil'
        },
        {
            'Festival': 'Ganesh Chaturthi',
            'Religion/Type': 'Hindu',
            'Description': 'Celebration of the birth of Lord Ganesha',
            'Season': 'August-September',
            'Primary States': 'Maharashtra, Karnataka, Telangana, Andhra Pradesh, Tamil Nadu',
            'Participants (millions)': 150,
            'Economic Impact (Millions USD)': 800,
            'Duration (days)': 10,
            'Tourist Attraction Level': 'High',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Moderate to High',
            'Practices': 'Installation of Ganesha idols, prayers, immersion ceremony (visarjan)',
            'Special Foods': 'Modak, ladoo, puran poli, and other sweets',
            'Traditional Attire': 'Traditional Indian wear, especially in Maharashtra - dhoti-kurta for men, nauvari saree for women',
            'Cultural Significance': 'Symbolizes wisdom, prosperity, and good fortune'
        },
        {
            'Festival': 'Navratri',
            'Religion/Type': 'Hindu',
            'Description': 'Nine nights dedicated to the worship of Goddess Durga in her nine forms',
            'Season': 'September-October',
            'Primary States': 'Gujarat, Maharashtra, Karnataka, Tamil Nadu',
            'Participants (millions)': 200,
            'Economic Impact (Millions USD)': 900,
            'Duration (days)': 9,
            'Tourist Attraction Level': 'High',
            'Global Celebrations': '10+ countries',
            'Environmental Impact': 'Moderate',
            'Practices': 'Dandiya raas and garba (folk dances), fasting, prayers',
            'Special Foods': 'Sabudana khichdi, kuttu puris, singhare ka halwa, and other fasting foods',
            'Traditional Attire': 'Colorful traditional attire - chaniya choli for women, kediya for men in Gujarat',
            'Cultural Significance': 'Celebrates the triumph of good over evil, and feminine divine power'
        },
        {
            'Festival': 'Christmas',
            'Religion/Type': 'Christian',
            'Description': 'Celebration of the birth of Jesus Christ',
            'Season': 'December',
            'Primary States': 'All India, especially Goa, Kerala, and Northeastern states',
            'Participants (millions)': 30,
            'Economic Impact (Millions USD)': 500,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '150+ countries',
            'Environmental Impact': 'Low to Moderate',
            'Practices': 'Midnight mass, carol singing, Christmas trees, gift exchanges',
            'Special Foods': 'Christmas cake, wine, roast meats, traditional sweets',
            'Traditional Attire': 'Formal or festive wear, often red and green colors',
            'Cultural Significance': 'Celebrates love, family, giving, and peace'
        },
        {
            'Festival': 'Onam',
            'Religion/Type': 'Cultural/Hindu',
            'Description': 'Harvest festival of Kerala celebrating King Mahabali\'s annual visit',
            'Season': 'August-September',
            'Primary States': 'Kerala',
            'Participants (millions)': 35,
            'Economic Impact (Millions USD)': 400,
            'Duration (days)': 10,
            'Tourist Attraction Level': 'High',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Floral decorations (pookalam), boat races (vallam kali), grand feast (sadya)',
            'Special Foods': 'Onam sadya (26-course meal on banana leaf), payasam',
            'Traditional Attire': 'Kasavu saree (cream with gold border) for women, mundu for men',
            'Cultural Significance': 'Celebrates harmony, equality, and prosperity'
        },
        {
            'Festival': 'Pongal',
            'Religion/Type': 'Cultural/Hindu',
            'Description': 'Harvest festival of Tamil Nadu thanking the Sun God',
            'Season': 'January',
            'Primary States': 'Tamil Nadu',
            'Participants (millions)': 70,
            'Economic Impact (Millions USD)': 350,
            'Duration (days)': 4,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Boiling of first rice harvest, cattle worship (Mattu Pongal), bonfires, kite flying',
            'Special Foods': 'Sweet pongal, ven pongal (savory rice), sugarcane',
            'Traditional Attire': 'Traditional Tamil attire - silk sarees for women, veshti for men',
            'Cultural Significance': 'Gratitude for harvest, celebration of cattle and nature'
        },
        {
            'Festival': 'Baisakhi',
            'Religion/Type': 'Sikh/Cultural',
            'Description': 'Punjabi harvest festival and Sikh New Year, commemorating the formation of Khalsa',
            'Season': 'April',
            'Primary States': 'Punjab, Haryana',
            'Participants (millions)': 30,
            'Economic Impact (Millions USD)': 300,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '10+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Processions, bhangra and gidda dances, community meals (langar)',
            'Special Foods': 'Langar food, sarson ka saag, makki di roti, sweets like jalebi and ladoo',
            'Traditional Attire': 'Colorful Punjabi traditional wear - salwar kameez for women, kurta and turban for men',
            'Cultural Significance': 'Marks the founding of the Khalsa panth and celebrates harvest'
        },
        {
            'Festival': 'Bihu',
            'Religion/Type': 'Cultural',
            'Description': 'Assamese harvest festival and new year celebration',
            'Season': 'April, October, January',
            'Primary States': 'Assam',
            'Participants (millions)': 25,
            'Economic Impact (Millions USD)': 200,
            'Duration (days)': 7,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '3+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Bihu dance, buffalo fights (now banned), community feasts',
            'Special Foods': 'Pitha (rice cakes), laru (coconut sweets), traditional Assamese dishes',
            'Traditional Attire': 'Traditional Assamese wear - mekhela chador for women, dhoti and gamosa for men',
            'Cultural Significance': 'Celebrates agriculture cycles and Assamese cultural identity'
        },
        {
            'Festival': 'Raksha Bandhan',
            'Religion/Type': 'Hindu/Cultural',
            'Description': 'Celebration of the bond between brothers and sisters',
            'Season': 'July-August',
            'Primary States': 'All India',
            'Participants (millions)': 100,
            'Economic Impact (Millions USD)': 650,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Low',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Sisters tie rakhi (sacred thread) on brothers\' wrists, brothers give gifts and promise protection',
            'Special Foods': 'Sweets, especially ladoos and barfi',
            'Traditional Attire': 'Traditional Indian wear',
            'Cultural Significance': 'Celebrates sibling relationships and duty of protection'
        },
        {
            'Festival': 'Janmashtami',
            'Religion/Type': 'Hindu',
            'Description': 'Celebration of Lord Krishna\'s birth',
            'Season': 'August-September',
            'Primary States': 'All India, especially Mathura, Vrindavan (UP), Maharashtra, Gujarat',
            'Participants (millions)': 100,
            'Economic Impact (Millions USD)': 500,
            'Duration (days)': 2,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '10+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Dahi Handi (breaking of clay pot), fasting, night vigil, bhajans (devotional songs)',
            'Special Foods': 'Makhan (butter), milk-based sweets, chappan bhog (56 food offerings)',
            'Traditional Attire': 'Traditional Indian wear, children often dressed as Krishna or Radha',
            'Cultural Significance': 'Celebrates divine playfulness and spiritual devotion'
        },
        {
            'Festival': 'Chhath Puja',
            'Religion/Type': 'Hindu',
            'Description': 'Ancient festival dedicated to the Sun God and Chhathi Maiya',
            'Season': 'October-November',
            'Primary States': 'Bihar, Jharkhand, Uttar Pradesh, Delhi',
            'Participants (millions)': 50,
            'Economic Impact (Millions USD)': 200,
            'Duration (days)': 4,
            'Tourist Attraction Level': 'Low',
            'Global Celebrations': '3+ countries',
            'Environmental Impact': 'Low to Moderate',
            'Practices': 'Fasting, standing in water offering prayers to the rising and setting sun',
            'Special Foods': 'Thekua (sweet cookies), rice laddoos, fruits',
            'Traditional Attire': 'Traditional wear - yellow sarees for women, dhoti-kurta for men',
            'Cultural Significance': 'Expresses gratitude to the sun for sustaining life on earth'
        },
        {
            'Festival': 'Eid ul-Adha',
            'Religion/Type': 'Islamic',
            'Description': 'Feast of sacrifice commemorating Prophet Ibrahim\'s willingness to sacrifice his son',
            'Season': 'Variable (Islamic calendar)',
            'Primary States': 'All India with significant Muslim populations',
            'Participants (millions)': 150,
            'Economic Impact (Millions USD)': 1500,
            'Duration (days)': 3,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '150+ countries',
            'Environmental Impact': 'Low to Moderate',
            'Practices': 'Prayer, animal sacrifice, charity, family gatherings',
            'Special Foods': 'Biryani, haleem, sewaiyan, kebabs, various meat dishes',
            'Traditional Attire': 'New clothes, men wear kurta-pajama or sherwani, women wear salwar kameez or sarees',
            'Cultural Significance': 'Emphasizes sacrifice, devotion, and charity'
        },
        {
            'Festival': 'Mahashivratri',
            'Religion/Type': 'Hindu',
            'Description': 'Night dedicated to Lord Shiva',
            'Season': 'February-March',
            'Primary States': 'All India',
            'Participants (millions)': 100,
            'Economic Impact (Millions USD)': 300,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Night vigil, fasting, temple worship, meditation',
            'Special Foods': 'Fruits, milk, bhang (cannabis preparation)',
            'Traditional Attire': 'Traditional Indian wear, often white',
            'Cultural Significance': 'Focuses on overcoming darkness and ignorance through spiritual practice'
        },
        {
            'Festival': 'Lohri',
            'Religion/Type': 'Cultural/Hindu/Sikh',
            'Description': 'Punjabi harvest festival celebrating winter solstice',
            'Season': 'January',
            'Primary States': 'Punjab, Haryana, Delhi',
            'Participants (millions)': 20,
            'Economic Impact (Millions USD)': 150,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Low',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Moderate',
            'Practices': 'Bonfire, throwing popcorn and rewri into fire, singing, dancing',
            'Special Foods': 'Rewri, gajak, popcorn, peanuts, til ladoos',
            'Traditional Attire': 'Traditional Punjabi wear - colorful clothes',
            'Cultural Significance': 'Marks winter\'s end and honors sun deity for returning warmth'
        },
        {
            'Festival': 'Puri Rath Yatra',
            'Religion/Type': 'Hindu',
            'Description': 'Chariot festival of Lord Jagannath',
            'Season': 'June-July',
            'Primary States': 'Odisha',
            'Participants (millions)': 10,
            'Economic Impact (Millions USD)': 100,
            'Duration (days)': 9,
            'Tourist Attraction Level': 'High',
            'Global Celebrations': '20+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Pulling giant wooden chariots carrying deities through streets',
            'Special Foods': 'Mahaprasad (56 dishes), poda pitha',
            'Traditional Attire': 'Traditional Odia wear',
            'Cultural Significance': 'Symbolizes equality as devotees of all castes pull the chariot'
        },
        {
            'Festival': 'Kumbh Mela',
            'Religion/Type': 'Hindu',
            'Description': 'World\'s largest religious gathering held at four river bank pilgrimage sites',
            'Season': 'Variable (every 3 years, rotating locations)',
            'Primary States': 'Uttar Pradesh (Prayagraj, Haridwar), Maharashtra (Nashik), Madhya Pradesh (Ujjain)',
            'Participants (millions)': 200,
            'Economic Impact (Millions USD)': 2000,
            'Duration (days)': 45,
            'Tourist Attraction Level': 'Very High',
            'Global Celebrations': '1 country (India)',
            'Environmental Impact': 'High',
            'Practices': 'Ritual bathing in sacred rivers, prayers, spiritual discourses',
            'Special Foods': 'Sattvic food, prasad',
            'Traditional Attire': 'Simple traditional wear, saffron robes for sadhus',
            'Cultural Significance': 'Sacred pilgrimage for spiritual purification'
        },
        {
            'Festival': 'Karva Chauth',
            'Religion/Type': 'Hindu',
            'Description': 'Festival where married women fast for their husband\'s longevity',
            'Season': 'October-November',
            'Primary States': 'North India',
            'Participants (millions)': 20,
            'Economic Impact (Millions USD)': 250,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Low',
            'Global Celebrations': '5+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Day-long fast, moonrise ritual, prayer, henna application',
            'Special Foods': 'Sargi (pre-dawn meal), feast after moonrise',
            'Traditional Attire': 'Traditional red or maroon sarees or lehengas, bridal jewelry',
            'Cultural Significance': 'Celebrates marital bonds and love'
        },
        {
            'Festival': 'Makar Sankranti',
            'Religion/Type': 'Hindu',
            'Description': 'Harvest festival marking the sun\'s transit into Capricorn',
            'Season': 'January',
            'Primary States': 'All India (known by different names)',
            'Participants (millions)': 80,
            'Economic Impact (Millions USD)': 300,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '3+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Kite flying, ritual bathing, bonfires, cow worship',
            'Special Foods': 'Til (sesame) sweets, jaggery products, khichdi',
            'Traditional Attire': 'Traditional wear, often in yellow',
            'Cultural Significance': 'Marks the end of winter and beginning of harvest season'
        },
        {
            'Festival': 'Guru Nanak Jayanti',
            'Religion/Type': 'Sikh',
            'Description': 'Birth anniversary of Guru Nanak, the founder of Sikhism',
            'Season': 'October-November',
            'Primary States': 'Punjab, Haryana, Delhi, and areas with Sikh population',
            'Participants (millions)': 30,
            'Economic Impact (Millions USD)': 100,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '15+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Akhand Path (48-hour non-stop reading of Guru Granth Sahib), processions, langar',
            'Special Foods': 'Langar (community meal), kada prasad',
            'Traditional Attire': 'Traditional Punjabi wear',
            'Cultural Significance': 'Honors the teachings of equality, selfless service, and devotion'
        },
        {
            'Festival': 'Buddha Purnima',
            'Religion/Type': 'Buddhist',
            'Description': 'Celebration of Buddha\'s birth, enlightenment, and death',
            'Season': 'April-May',
            'Primary States': 'Bihar, Uttar Pradesh, Ladakh, Arunachal Pradesh, Sikkim',
            'Participants (millions)': 10,
            'Economic Impact (Millions USD)': 50,
            'Duration (days)': 1,
            'Tourist Attraction Level': 'Medium',
            'Global Celebrations': '30+ countries',
            'Environmental Impact': 'Low',
            'Practices': 'Prayer, meditation, charity, pilgrimage to Buddhist sites',
            'Special Foods': 'Kheer (rice pudding)',
            'Traditional Attire': 'White clothes',
            'Cultural Significance': 'Emphasizes peace, non-violence, and mindfulness'
        },
        {
            'Festival': 'Thrissur Pooram',
            'Religion/Type': 'Hindu',
            'Description': 'Temple festival with spectacular display of elephants, music, and fireworks',
            'Season': 'April-May',
            'Primary States': 'Kerala',
            'Participants (millions)': 2,
            'Economic Impact (Millions USD)': 50,
            'Duration (days)': 36,
            'Tourist Attraction Level': 'High',
            'Global Celebrations': '1 country (India)',
            'Environmental Impact': 'Moderate',
            'Practices': 'Procession of decorated elephants, percussion performances, fireworks',
            'Special Foods': 'Traditional Kerala snacks',
            'Traditional Attire': 'Traditional Kerala wear - kasavu saree for women, mundu for men',
            'Cultural Significance': 'Showcases Kerala\'s cultural heritage and artistic traditions'
        }
    ]
    
    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(festivals_data)
    
    # Interactive festival exploration section
    st.header("Explore India's Major Festivals")
    
    # Create 2-column layout
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Festival selection
        selected_festival = st.selectbox(
            "Select a festival to explore:",
            options=df['Festival'].tolist()
        )
        
        # Display festival image or icon
        festival_icons = {
            'Diwali': '🪔',
            'Holi': '🎨',
            'Durga Puja': '🛕',
            'Ganesh Chaturthi': '🐘',
            'Navratri/Durgotsav': '💃',
            'Onam': '🌸',
            'Eid ul-Fitr': '🌙',
            'Christmas': '🎄',
            'Baisakhi': '🌾',
            'Janmashtami': '👶',
        }
        
        # Display festival icon or default
        icon = festival_icons.get(selected_festival, '🎯')
        st.markdown(f"<h1 style='text-align:center; font-size:4rem;'>{icon}</h1>", unsafe_allow_html=True)
    
    # Display detailed information about the selected festival
    with col2:
        try:
            festival_data = df[df['Festival'] == selected_festival].iloc[0]
            
            # Create a clean display of festival details
            st.markdown(f"### {selected_festival}")
            
            # Add basic info with styling
            st.markdown(f"""
            <div style='margin-bottom:15px;'>
                <span style='background-color:rgba(255,153,51,0.2); 
                color:#FF9933; 
                padding:3px 8px; 
                border-radius:12px; 
                font-size:0.85rem;'>
                {festival_data['Religion/Type']}
                </span>
                <span style='margin-left:10px; 
                background-color:rgba(108,140,191,0.2); 
                color:#6C8CBF; 
                padding:3px 8px; 
                border-radius:12px; 
                font-size:0.85rem;'>
                {festival_data['Season']}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Display description
            if 'Description' in festival_data:
                st.markdown(f"""
                <div style='margin-bottom:15px; font-size:0.95rem;'>
                {festival_data['Description']}
                </div>
                """, unsafe_allow_html=True)
            
            # Create two-column layout for details
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                # Show regional information
                if 'Primary States' in festival_data:
                    st.markdown(f"**Celebrated in:** {festival_data['Primary States']}")
                
                # Show duration
                if 'Duration (days)' in festival_data:
                    st.markdown(f"**Duration:** {festival_data['Duration (days)']} days")
                
                # Show practices
                if 'Practices' in festival_data:
                    st.markdown("**Key Practices:**")
                    st.markdown(f"<div style='font-size:0.9rem;'>{festival_data['Practices']}</div>", unsafe_allow_html=True)
            
            with detail_col2:
                # Show foods
                if 'Special Foods' in festival_data:
                    st.markdown("**Traditional Foods:**")
                    st.markdown(f"<div style='font-size:0.9rem;'>{festival_data['Special Foods']}</div>", unsafe_allow_html=True)
                
                # Show attire
                if 'Traditional Attire' in festival_data:
                    st.markdown("**Traditional Attire:**")
                    st.markdown(f"<div style='font-size:0.9rem;'>{festival_data['Traditional Attire']}</div>", unsafe_allow_html=True)
            
            # Cultural significance
            if 'Cultural Significance' in festival_data:
                st.markdown("**Cultural Significance:**")
                st.markdown(f"<div style='font-size:0.95rem; font-style:italic; background-color:rgba(30, 33, 41, 0.3); padding:8px; border-radius:5px;'>{festival_data['Cultural Significance']}</div>", unsafe_allow_html=True)
            
            # Create metrics row
            st.markdown("### Festival Impact")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                if 'Participants (millions)' in festival_data:
                    st.metric("Participants", f"{festival_data['Participants (millions)']}M")
                else:
                    st.metric("Participants", "N/A")
            
            with metric_col2:
                if 'Economic Impact (Millions USD)' in festival_data:
                    impact_value = festival_data['Economic Impact (Millions USD)']
                    if isinstance(impact_value, (int, float)):
                        if impact_value >= 1000:
                            st.metric("Economic Impact", f"${impact_value/1000:.1f}B")
                        else:
                            st.metric("Economic Impact", f"${impact_value:.0f}M")
                    else:
                        st.metric("Economic Impact", "N/A")
                else:
                    st.metric("Economic Impact", "N/A")
            
            with metric_col3:
                if 'Global Reach' in festival_data:
                    st.metric("Global Reach", f"{festival_data['Global Reach']}+ countries")
                elif 'Global Celebrations' in festival_data:
                    st.metric("Global Reach", f"{festival_data['Global Celebrations']}")
                else:
                    st.metric("Global Reach", "N/A")
            
            # Environmental impact badge
            if 'Environmental Impact' in festival_data:
                impact_colors = {
                    'High': '#FF5733',
                    'Moderate to High': '#FF9933',
                    'Moderate': '#FFCC33',
                    'Low to Moderate': '#33CC66',
                    'Low': '#33CCCC'
                }
                impact = festival_data['Environmental Impact']
                color = impact_colors.get(impact, '#888888')
                
                st.markdown(f"""
                <div style='margin-top:15px;'>
                    <span style='background-color:{color}33; 
                    color:{color}; 
                    padding:5px 10px; 
                    border-radius:4px; 
                    font-size:0.9rem;'>
                    Environmental Impact: {impact}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error displaying festival details: {e}")
    
    # Divider
    st.markdown("---")
    
    # Festival visualizations section in tabs
    st.header("Festival Data Insights")
    
    tabs = st.tabs(["Distribution by Type", "Economic Impact", "Seasonal Patterns", "Global Reach", "Cultural Practices"])
    
    # Tab 1: Distribution by Type
    with tabs[0]:
        try:
            # Create religion/type distribution data
            religion_counts = df['Religion/Type'].value_counts().reset_index()
            religion_counts.columns = ['Religion/Type', 'Count']
            
            fig = px.pie(
                religion_counts, 
                values='Count', 
                names='Religion/Type',
                title='Distribution of Festivals by Type',
                color_discrete_sequence=get_color_palette(len(religion_counts)),
                hole=0.4
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Hindu festivals make up the largest segment, reflecting the majority religion, 
            but India's festival landscape shows remarkable diversity with cultural, Islamic, harvest, and other celebrations 
            that span across religious boundaries.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in distribution visualization: {e}")
    
    # Tab 2: Economic Impact
    with tabs[1]:
        try:
            # Sort data by economic impact
            economic_df = df.sort_values('Economic Impact (Millions USD)', ascending=False).head(10)
            
            fig = px.bar(
                economic_df,
                x='Festival',
                y='Economic Impact (Millions USD)',
                color='Religion/Type',
                title='Top 10 Festivals by Economic Impact (USD Millions)',
                color_discrete_sequence=get_color_palette(len(economic_df['Religion/Type'].unique())),
                text='Economic Impact (Millions USD)'
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(texttemplate='%{text:.0f}M', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Diwali generates the highest economic impact at approximately $7.2 billion USD annually, 
            followed by Eid ul-Fitr, Kumbh Mela, and Holi. Major festivals significantly boost sectors like retail, food, 
            clothing, travel, and services.
            </div>
            """, unsafe_allow_html=True)
            
            # Correlation between participants and economic impact
            fig = px.scatter(
                df,
                x='Participants (millions)',
                y='Economic Impact (Millions USD)',
                size='Duration (days)',
                color='Religion/Type',
                hover_name='Festival',
                title='Relationship: Participants, Economic Impact & Festival Duration',
                log_x=True,
                size_max=25,
                color_discrete_sequence=get_color_palette(len(df['Religion/Type'].unique()))
            )
            fig = apply_dark_theme(fig)
            fig.update_layout(xaxis_title="Participants (Millions, log scale)", 
                            yaxis_title="Economic Impact (USD Millions)")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> There's a strong correlation between the number of participants and economic impact. 
            Mass participation festivals like Diwali and Holi generate disproportionately large economic benefits compared to 
            regional or niche celebrations.
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in economic impact visualization: {e}")
    
    # Tab 3: Seasonal Patterns
    with tabs[2]:
        try:
            # Extract month data for visualization
            def extract_month(season_str):
                months = {
                    'January': 1, 'February': 2, 'March': 3, 'April': 4,
                    'May': 5, 'June': 6, 'July': 7, 'August': 8,
                    'September': 9, 'October': 10, 'November': 11, 'December': 12
                }
                
                if pd.isna(season_str) or season_str == 'Variable':
                    return None
                
                # Extract first month mentioned
                for month in months.keys():
                    if month in season_str:
                        return month
                return None
            
            # Create a season order for better visualization
            season_order = ['Winter', 'Spring', 'Summer', 'Monsoon', 'Autumn']
            
            # Map months to seasons
            month_to_season = {
                'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
                'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
                'June': 'Summer', 'July': 'Summer',
                'August': 'Monsoon', 'September': 'Monsoon',
                'October': 'Autumn', 'November': 'Autumn'
            }
            
            # Extract month and add season
            df['Month'] = df['Season'].apply(extract_month)
            df['Season_Category'] = df['Month'].map(lambda x: month_to_season.get(x, 'Variable'))
            
            # Count festivals by season
            season_counts = df['Season_Category'].value_counts().reset_index()
            season_counts.columns = ['Season', 'Count']
            
            # Handle season_counts data
            if not season_counts.empty:
                # Order seasons properly
                valid_seasons = [s for s in season_order if s in season_counts['Season'].values]
                season_counts['Season'] = pd.Categorical(
                    season_counts['Season'], 
                    categories=valid_seasons, 
                    ordered=True
                )
                season_counts = season_counts.sort_values('Season')
                
                fig = px.bar(
                    season_counts,
                    x='Season',
                    y='Count',
                    color='Season',
                    title='Seasonal Distribution of Festivals',
                    text='Count',
                    color_discrete_sequence=get_color_palette(len(season_counts))
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            # Festival timeline through the year
            months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                           'July', 'August', 'September', 'October', 'November', 'December']
            
            # Create month-festival mapping for visualization
            df_with_months = df[df['Month'].notna()]
            
            if not df_with_months.empty:
                # Group festivals by month
                month_festivals = {}
                for month in months_order:
                    month_festivals[month] = df_with_months[df_with_months['Month'] == month]['Festival'].tolist()
                
                # Create monthly festival count data
                months_with_festivals = []
                festival_counts = []
                
                for month in months_order:
                    festivals_in_month = month_festivals.get(month, [])
                    if festivals_in_month:
                        months_with_festivals.append(month)
                        festival_counts.append(len(festivals_in_month))
                
                # Create the visualization
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=months_with_festivals,
                    y=festival_counts,
                    text=festival_counts,
                    textposition='outside',
                    marker_color=get_color_palette(len(months_with_festivals)),
                    hoverinfo='text',
                    hovertext=[', '.join(month_festivals.get(month, [])) for month in months_with_festivals]
                ))
                
                fig.update_layout(
                    title='Festival Calendar Throughout the Year',
                    xaxis_title='Month',
                    yaxis_title='Number of Major Festivals',
                    xaxis={'categoryorder': 'array', 'categoryarray': months_order}
                )
                
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Autumn months (September-November) host the highest number of festivals, coinciding with the 
            harvest season and favorable weather. Winter and Spring also see significant celebrations, while the Summer and 
            Monsoon seasons have fewer major festivals.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in seasonal patterns visualization: {e}")
    
    # Tab 4: Global Reach
    with tabs[3]:
        try:
            # Process global reach data
            def extract_countries_number(global_reach_str):
                if pd.isna(global_reach_str):
                    return 0
                    
                # Extract number from strings like "30+ countries"
                match = re.search(r'(\d+)\+', global_reach_str)
                if match:
                    return int(match.group(1))
                elif global_reach_str == "1 country (India)":
                    return 1
                else:
                    return 0
            
            # Add Global Reach column with extracted numbers
            df['Global Reach'] = df['Global Celebrations'].apply(extract_countries_number)
            
            # Sort and get top festivals by global reach
            global_df = df.sort_values('Global Reach', ascending=False).head(10)
            
            fig = px.bar(
                global_df,
                x='Festival',
                y='Global Reach',
                color='Religion/Type',
                title='Top 10 Indian Festivals with Global Reach (Countries with Celebrations)',
                color_discrete_sequence=get_color_palette(len(global_df['Religion/Type'].unique())),
                text='Global Reach'
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(texttemplate='%{text}+ countries', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # Create a world map showing festival reach
            # First create a dataframe with country codes and festival counts
            # Use ISO country codes for the map
            country_codes = {
                'India': 'IND',
                'United States': 'USA',
                'United Kingdom': 'GBR',
                'Canada': 'CAN',
                'Australia': 'AUS',
                'Singapore': 'SGP',
                'Malaysia': 'MYS',
                'South Africa': 'ZAF',
                'United Arab Emirates': 'ARE',
                'Nepal': 'NPL',
                'Sri Lanka': 'LKA',
                'Indonesia': 'IDN',
                'Saudi Arabia': 'SAU',
                'Germany': 'DEU',
                'France': 'FRA'
            }
            
            # Create festival locations mapping
            festival_locations = {}
            
            # Map festivals to their primary global celebration locations beyond India
            for _, row in global_df.iterrows():
                if row['Religion/Type'] == 'Islamic':
                    # Islamic festivals celebrated in many countries with Muslim populations
                    countries = ['IND', 'SAU', 'ARE', 'IDN', 'MYS', 'NPL', 'USA', 'GBR', 'CAN', 'AUS']
                elif row['Religion/Type'] == 'Hindu':
                    # Hindu festivals primarily in countries with significant Indian diaspora
                    countries = ['IND', 'NPL', 'LKA', 'USA', 'GBR', 'CAN', 'AUS', 'SGP', 'MYS', 'ZAF', 'ARE']
                elif row['Religion/Type'] == 'Christian':
                    # Christian festivals are global
                    countries = ['IND', 'USA', 'GBR', 'CAN', 'AUS', 'FRA', 'DEU', 'ZAF', 'IDN', 'SGP', 'MYS']
                elif row['Religion/Type'] == 'Sikh':
                    # Sikh festivals in countries with Sikh diaspora
                    countries = ['IND', 'USA', 'GBR', 'CAN', 'AUS']
                elif row['Religion/Type'] == 'Buddhist':
                    # Buddhist festivals in Buddhist countries and diaspora
                    countries = ['IND', 'NPL', 'LKA', 'IDN', 'MYS', 'SGP', 'USA', 'CAN']
                else:
                    # Cultural festivals primarily in countries with Indian diaspora
                    countries = ['IND', 'USA', 'GBR', 'CAN', 'AUS', 'SGP', 'MYS']
                
                # Limit to global reach number
                max_countries = min(row['Global Reach'], len(countries))
                festival_locations[row['Festival']] = countries[:max_countries]
            
            # Create a dataframe with country code and festival count
            country_festival_counts = {}
            for festival, countries in festival_locations.items():
                for country in countries:
                    if country in country_festival_counts:
                        country_festival_counts[country] += 1
                    else:
                        country_festival_counts[country] = 1
            
            map_data = pd.DataFrame({
                'iso_alpha': list(country_festival_counts.keys()),
                'festival_count': list(country_festival_counts.values())
            })
            
            # Create the map
            fig = px.choropleth(
                map_data,
                locations='iso_alpha',
                color='festival_count',
                hover_name='iso_alpha',
                color_continuous_scale=px.colors.sequential.Plasma,
                title='Global Spread of Indian Festivals',
                template='plotly_dark'
            )
            
            fig.update_layout(
                geo=dict(
                    showcoastlines=True,
                    coastlinecolor="White",
                    showland=True,
                    landcolor="rgba(30, 33, 41, 0.7)",
                    showocean=True,
                    oceancolor="rgba(20, 23, 31, 0.7)",
                    showlakes=False,
                    showcountries=True,
                    countrycolor="White",
                    projection_type='natural earth'
                )
            )
            
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Add table of top festivals by global reach
            st.markdown("### Festivals with Widest Global Reach")
            global_table = global_df[['Festival', 'Religion/Type', 'Global Reach']].copy()
            global_table.columns = ['Festival', 'Type', 'Countries']
            st.table(global_table.head(5))
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Islamic festivals like Eid ul-Fitr and Eid ul-Adha have the widest global reach due to the worldwide Islamic community, 
            while Diwali and Holi have grown in global popularity beyond the Indian diaspora. Christmas, while originating outside India,
            is celebrated widely within India and globally, demonstrating the country's religious diversity.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in global reach visualization: {e}")
    
    # Tab 5: Cultural Practices
    with tabs[4]:
        try:
            st.markdown("### Cultural Traditions of Indian Festivals")
            
            # Create a selection for practices type
            practice_type = st.radio(
                "Explore festival traditions by:",
                ["Food", "Attire", "Rituals & Customs"],
                horizontal=True
            )
            
            if practice_type == "Food":
                st.markdown("#### Traditional Foods Associated with Major Festivals")
                
                # Create a dataframe with festival and food info
                food_df = df[['Festival', 'Religion/Type', 'Special Foods']].sort_values('Festival')
                
                # Display as a formatted table with custom styling
                for _, row in food_df.iterrows():
                    if pd.notna(row['Special Foods']):
                        st.markdown(f"""
                        <div style='margin-bottom:15px; padding:15px; border-radius:8px; background-color:rgba(30, 33, 41, 0.3); border-left:4px solid {get_color_palette(1)[0]};'>
                            <div style='display:flex; justify-content:space-between;'>
                                <span style='font-weight:bold; font-size:1.1em;'>{row['Festival']}</span>
                                <span style='color:#AAAAAA; font-size:0.9em;'>{row['Religion/Type']}</span>
                            </div>
                            <div style='margin-top:8px; font-size:0.95em;'>
                                {row['Special Foods']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class='insight-box'>
                <strong>Insight:</strong> Festival foods in India often feature sweets (mithai) made with ingredients like milk, sugar, 
                nuts, and flour. Regional variations reflect local agriculture and cultural preferences, with many festival foods 
                having symbolic significance related to prosperity, fertility, or purification.
                </div>
                """, unsafe_allow_html=True)
                
            elif practice_type == "Attire":
                st.markdown("#### Traditional Attire for Major Festivals")
                
                # Create a dataframe with festival and attire info
                attire_df = df[['Festival', 'Religion/Type', 'Traditional Attire']].sort_values('Festival')
                
                # Display as a formatted table with custom styling
                for _, row in attire_df.iterrows():
                    if pd.notna(row['Traditional Attire']):
                        st.markdown(f"""
                        <div style='margin-bottom:15px; padding:15px; border-radius:8px; background-color:rgba(30, 33, 41, 0.3); border-left:4px solid {get_color_palette(2)[1]};'>
                            <div style='display:flex; justify-content:space-between;'>
                                <span style='font-weight:bold; font-size:1.1em;'>{row['Festival']}</span>
                                <span style='color:#AAAAAA; font-size:0.9em;'>{row['Religion/Type']}</span>
                            </div>
                            <div style='margin-top:8px; font-size:0.95em;'>
                                {row['Traditional Attire']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class='insight-box'>
                <strong>Insight:</strong> Festival attire in India often features traditional clothing in bright, auspicious colors. 
                Many festivals involve wearing new clothes as a symbol of renewal, with specific colors or styles associated with 
                particular celebrations (like red for weddings and many Hindu festivals).
                </div>
                """, unsafe_allow_html=True)
                
            else:  # Rituals & Customs
                st.markdown("#### Rituals & Practices for Major Festivals")
                
                # Create a dataframe with festival and practices info
                practices_df = df[['Festival', 'Religion/Type', 'Practices', 'Cultural Significance']].sort_values('Festival')
                
                # Display as a formatted table with custom styling
                for _, row in practices_df.iterrows():
                    if pd.notna(row['Practices']):
                        st.markdown(f"""
                        <div style='margin-bottom:15px; padding:15px; border-radius:8px; background-color:rgba(30, 33, 41, 0.3); border-left:4px solid {get_color_palette(3)[2]};'>
                            <div style='display:flex; justify-content:space-between;'>
                                <span style='font-weight:bold; font-size:1.1em;'>{row['Festival']}</span>
                                <span style='color:#AAAAAA; font-size:0.9em;'>{row['Religion/Type']}</span>
                            </div>
                            <div style='margin-top:8px; font-size:0.95em;'>
                                <strong>Practices:</strong> {row['Practices']}
                            </div>
                            <div style='margin-top:5px; font-size:0.9em; font-style:italic; color:#CCCCCC;'>
                                <strong>Significance:</strong> {row['Cultural Significance'] if pd.notna(row['Cultural Significance']) else 'Not specified'}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class='insight-box'>
                <strong>Insight:</strong> Festival rituals often blend religious practices with community celebrations, maintaining 
                ancient traditions while adapting to modern contexts. Common elements include prayer ceremonies, processions, 
                family gatherings, symbolic rituals, and community feasts, with each festival featuring unique practices that 
                reflect its cultural and spiritual significance.
                </div>
                """, unsafe_allow_html=True)
            
            # Add a comparison visualization
            st.markdown("### Duration of Festival Celebrations")
            
            # Sort and get top festivals by duration
            duration_df = df.sort_values('Duration (days)', ascending=False).head(15)
            
            fig = px.bar(
                duration_df,
                x='Festival',
                y='Duration (days)',
                color='Religion/Type',
                title='Longest Festival Celebrations in India (Days)',
                color_discrete_sequence=get_color_palette(len(duration_df['Religion/Type'].unique()))
            )
            fig = apply_dark_theme(fig)
            fig.update_layout(yaxis_title="Duration (Days)")
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in cultural practices visualization: {e}")
    
    # Environmental impact section
    st.header("Environmental Impact of Festivals")
    
    try:
        # Create a categorical mapping for environmental impact
        impact_mapping = {
            'High': 3,
            'Moderate to High': 2.5,
            'Moderate': 2,
            'Low to Moderate': 1.5,
            'Low': 1
        }
        
        # Map impact levels to numeric scores
        df['Impact Score'] = df['Environmental Impact'].map(impact_mapping)
        
        # Sort by impact score
        env_df = df.sort_values('Impact Score', ascending=False)
        
        fig = px.bar(
            env_df,
            x='Festival',
            y='Impact Score',
            color='Environmental Impact',
            title='Environmental Impact of Major Festivals',
            hover_data=['Practices'],
            color_discrete_map={
                'High': '#FF5733',
                'Moderate to High': '#FF9933',
                'Moderate': '#FFCC33',
                'Low to Moderate': '#33CC66',
                'Low': '#33CCCC'
            }
        )
        fig = apply_dark_theme(fig)
        fig.update_layout(yaxis_title="Environmental Impact Level")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error in environmental impact visualization: {e}")
    
    # Key insights about festival sustainability
    st.markdown("""
    <div class='insight-box'>
    <strong>Sustainability Insights:</strong>
    <ul>
      <li><strong>High Impact:</strong> Festivals like Diwali face environmental challenges from air pollution due to fireworks.</li>
      <li><strong>Water Bodies:</strong> Idol immersion during Ganesh Chaturthi and Durga Puja impacts water ecosystems.</li>
      <li><strong>Sustainable Practices:</strong> Many festivals now promote eco-friendly celebrations with natural colors (Holi), 
      eco-friendly idols, and reduced fireworks.</li>
      <li><strong>Low Impact:</strong> Harvest festivals like Onam and cultural festivals generally have minimal environmental footprint.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Regional festival distribution section
    st.header("Regional Festival Distribution")
    
    try:
        # Create a mapping of regions to states for visualization
        region_mapping = {
            'North India': ['Punjab', 'Haryana', 'Himachal Pradesh', 'Uttarakhand', 'Uttar Pradesh', 'Delhi', 'Jammu and Kashmir', 'Ladakh'],
            'East India': ['West Bengal', 'Bihar', 'Jharkhand', 'Odisha', 'Assam', 'Tripura', 'Meghalaya', 'Manipur', 'Nagaland', 'Arunachal Pradesh', 'Sikkim', 'Mizoram'],
            'South India': ['Tamil Nadu', 'Kerala', 'Karnataka', 'Andhra Pradesh', 'Telangana', 'Puducherry'],
            'West India': ['Maharashtra', 'Gujarat', 'Goa', 'Rajasthan'],
            'Central India': ['Madhya Pradesh', 'Chhattisgarh']
        }
        
        # Function to map primary states to regions
        def map_to_region(primary_states):
            if pd.isna(primary_states) or primary_states == 'All India':
                return 'All India'
                
            regions = []
            for region, states in region_mapping.items():
                for state in states:
                    if state in primary_states:
                        regions.append(region)
                        break
            
            if regions:
                return ', '.join(set(regions))
            else:
                return 'Other'
        
        # Add region column
        df['Region'] = df['Primary States'].apply(map_to_region)
        
        # Create region counts
        region_counts = df['Region'].value_counts().reset_index()
        region_counts.columns = ['Region', 'Count']
        
        # Create visualization
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Map visualization (using a sunburst chart to show hierarchy)
            # Create region-religion data
            region_religion_data = df.groupby(['Region', 'Religion/Type']).size().reset_index()
            region_religion_data.columns = ['Region', 'Religion/Type', 'Count']
            
            fig = px.sunburst(
                region_religion_data,
                path=['Region', 'Religion/Type'],
                values='Count',
                title='Distribution of Festivals by Region and Type',
                color_discrete_sequence=get_color_palette(5)
            )
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box' style='font-size:0.9rem;'>
            <strong>Regional Distribution:</strong> While pan-Indian festivals like Diwali are celebrated nationwide, 
            many festivals have strong regional identities. South India has distinctive harvest festivals like Pongal and Onam, 
            East India is known for Durga Puja, and North India for Lohri and Baisakhi.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Table showing unique festivals by region
            st.markdown("### Distinctive Regional Festivals")
            
            # Get region-specific festivals (exclude those celebrated across all India)
            region_specific = df[df['Primary States'] != 'All India']
            
            # Define regions to show
            regions_to_show = ['North India', 'South India', 'East India', 'West India']
            
            for region in regions_to_show:
                # Get festivals primarily celebrated in this region
                regional_festivals = region_specific[region_specific['Primary States'].apply(
                    lambda x: any(state in x for state in region_mapping.get(region, []))
                )]
                
                if not regional_festivals.empty:
                    # Get random color from palette for this region
                    region_color = get_color_palette(len(regions_to_show))[regions_to_show.index(region)]
                    
                    st.markdown(f"""
                    <div style='margin-bottom:12px; padding:8px; border-radius:5px; border-left:3px solid {region_color};'>
                        <span style='font-weight:bold; color:{region_color};'>{region}</span>
                        <div style='font-size:0.9rem; margin-top:5px;'>
                            {', '.join(regional_festivals['Festival'].sample(min(3, len(regional_festivals))).tolist())}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error in regional festival visualization: {e}")
    
    # Final summary
    st.header("The Cultural Significance of Indian Festivals")
    
    st.markdown("""
    <div class='story-text'>
    Festivals in India transcend mere celebrations – they are living heritage that connects generations, 
    strengthens community bonds, and preserves cultural traditions. Beyond their religious significance, 
    festivals play crucial economic roles, driving consumer spending, tourism, and employment in 
    handicrafts, food, and services sectors.
    
    Indian festivals represent a unique blend of ancient traditions and modern adaptations. As India 
    modernizes, festivals continue to evolve while maintaining their essential character. The growing 
    global reach of Indian festivals like Diwali and Holi demonstrates their universal appeal and 
    the soft power of Indian culture worldwide.
    </div>
    """, unsafe_allow_html=True)
    
    # Key takeaways in expandable sections
    with st.expander("🔍 Key Takeaways"):
        st.markdown("""
        - **Cultural Diversity:** India's festival landscape mirrors its religious and cultural diversity.
        - **Economic Engine:** Festivals drive significant economic activity ($15+ billion USD annually).
        - **Seasonal Rhythm:** Festival calendar follows agricultural cycles and seasonal changes.
        - **Global Influence:** Indian festivals increasingly celebrated worldwide.
        - **Evolving Traditions:** Ancient festivals adapting to modern contexts while preserving core values.
        - **Sustainability Challenges:** Growing awareness of environmental impacts leading to greener celebrations.
        """) 
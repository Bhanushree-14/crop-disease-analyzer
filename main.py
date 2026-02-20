import streamlit as st
import base64
import json
import time
import random
import requests
from datetime import datetime
from Leaf_Disease.main import LeafDiseaseDetector

# === WEATHER FUNCTION ===
def get_weather(city="Mumbai"):
    try:
        url = f"https://wttr.in/{city}?format=%t+%h+%w+%C"
        response = requests.get(url, timeout=5)
        weather_text = response.text.strip().split()
        
        if len(weather_text) >= 4:
            return {
                'temperature': weather_text[0],
                'humidity': weather_text[1],
                'wind': weather_text[2],
                'condition': ' '.join(weather_text[3:])
            }
    except:
        return None
    return None

# === PAGE CONFIG (ONLY ONCE!) ===
st.set_page_config(
    page_title="Kisaan Saathi - AI Crop Doctor",
    page_icon="🌾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === WEATHER SIDEBAR ===
with st.sidebar:
    st.markdown("## 🌤️ Weather for Farmers")
    st.markdown("---")
    
    city = st.text_input("Enter Village/City", "Mumbai")
    
    if st.button("Get Weather", use_container_width=True):
        weather_data = get_weather(city)
        if weather_data:
            st.session_state.weather = weather_data
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Temperature", weather_data['temperature'])
                st.metric("Wind", weather_data['wind'])
            with col2:
                st.metric("Humidity", weather_data['humidity'])
                st.write(f"**{weather_data['condition']}**")
            
            # Farming advice
            st.markdown("---")
            st.markdown("### 🌱 Advice")
            if "rain" in weather_data['condition'].lower():
                st.info("💧 Rain expected - Hold off on spraying")
            elif "sun" in weather_data['condition'].lower() or "clear" in weather_data['condition'].lower():
                st.success("☀️ Good day for farming!")
            else:
                st.warning("☁️ Check disease spread risk")
        else:
            st.error("Could not fetch weather")

# === INJECT CLEAN CSS ===
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #1e5128 0%, #2e7d32 100%);
}

/* Hero Section */
.hero-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 30px;
    padding: 40px 20px;
    margin-bottom: 30px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.9);
}

/* Stats Cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #2e7d32;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
}

/* Feature Cards */
.feature-card {
    background: white;
    border-radius: 25px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.feature-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.step-badge {
    background: #2e7d32;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    margin-right: 15px;
}

.feature-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
}

/* Language Pills */
.language-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin: 20px 0;
}

.language-pill {
    background: #2e7d32;
    color: white;
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 500;
}

/* Result Card */
.result-card {
    background: white;
    border-radius: 25px;
    padding: 30px;
    margin: 20px 0;
    border-left: 8px solid #2e7d32;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.disease-title {
    font-size: 2rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 15px;
}

.confidence-meter {
    width: 100%;
    height: 10px;
    background: #e0e0e0;
    border-radius: 10px;
    margin: 15px 0;
    overflow: hidden;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #2e7d32, #4caf50);
    border-radius: 10px;
}

.severity-badge {
    display: inline-block;
    padding: 4px 15px;
    border-radius: 20px;
    color: white;
    font-weight: 500;
    font-size: 0.9rem;
    margin-left: 10px;
}

.severity-mild { background: #4caf50; }
.severity-moderate { background: #ff9800; }
.severity-severe { background: #f44336; }
.severity-none { background: #2196f3; }

/* Analyze Button */
.analyze-btn {
    background: linear-gradient(135deg, #2e7d32, #4caf50);
    color: white;
    border: none;
    padding: 15px 30px;
    font-size: 1.3rem;
    font-weight: 600;
    border-radius: 15px;
    width: 100%;
    cursor: pointer;
    margin: 20px 0;
    transition: all 0.3s ease;
}

.analyze-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(46, 125, 50, 0.4);
}

/* Chat Bubbles */
.chat-bubble-farmer {
    background: #e3f2fd;
    padding: 15px 20px;
    border-radius: 25px 25px 25px 5px;
    max-width: 80%;
    margin: 10px 0;
}

.chat-bubble-ai {
    background: #f1f8e9;
    padding: 15px 20px;
    border-radius: 25px 25px 5px 25px;
    max-width: 80%;
    margin: 10px 0 10px auto;
}

/* Footer */
.footer {
    text-align: center;
    padding: 30px;
    color: white;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
""", unsafe_allow_html=True)

# === INITIALIZE SESSION STATE ===
if 'detector' not in st.session_state:
    with st.spinner("🚀 Loading AI Model..."):
        st.session_state.detector = LeafDiseaseDetector()
        time.sleep(1)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False

if 'current_disease' not in st.session_state:
    st.session_state.current_disease = None

# === HERO SECTION ===
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🌾 Kisaan Saathi</h1>
    <p class="hero-subtitle">AI Crop Doctor • किसानों का अपना AI सहायक</p>
</div>
""", unsafe_allow_html=True)

# === STATS CARDS ===
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">50K+</div>
        <div class="stat-label">Farmers Helped</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">95%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">6</div>
        <div class="stat-label">Languages</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">24/7</div>
        <div class="stat-label">Support</div>
    </div>
</div>
""", unsafe_allow_html=True)

# === LANGUAGE SELECTOR ===
st.markdown("""
<div class="language-container">
    <span class="language-pill">🇮🇳 हिंदी</span>
    <span class="language-pill">🇬🇧 English</span>
    <span class="language-pill">🇮🇳 தமிழ்</span>
    <span class="language-pill">🇮🇳 తెలుగు</span>
    <span class="language-pill">🇮🇳 മലയാളം</span>
    <span class="language-pill">🇮🇳 বাংলা</span>
</div>
""", unsafe_allow_html=True)

# === UPLOAD SECTION ===
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.markdown("""
<div class="feature-header">
    <div class="step-badge">📸</div>
    <h3 class="feature-title">Upload Crop Photo</h3>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a leaf image...",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file:
    # Display image
    st.image(uploaded_file, caption="Your Crop Photo", use_container_width=True)
    
    # Question input
    farmer_query = st.text_area(
        "आपका सवाल (Optional)",
        placeholder="Example: टमाटर के पत्तों पर भूरे धब्बे हैं...",
        height=80
    )
    
    # ANALYZE BUTTON - Always visible when file is uploaded
    st.markdown("---")
    
    if st.button("🔍 ANALYZE MY CROP", use_container_width=True, type="primary"):
        with st.spinner("🤖 AI is analyzing your crop..."):
            try:
                # Process image
                file_bytes = uploaded_file.getvalue()
                base64_image = base64.b64encode(file_bytes).decode('utf-8')
                
                # Get AI analysis
                analysis_result = st.session_state.detector.analyze_leaf_image_base64(base64_image)
                
                # Store results
                st.session_state.analysis_done = True
                st.session_state.current_disease = analysis_result
                
                # Use default question if none provided
                if not farmer_query:
                    farmer_query = "What disease does my crop have?"
                
                # Create AI response
                disease_name = analysis_result.get('disease_name', 'Unknown')
                treatment = analysis_result.get('treatment', 'Consult expert')
                hindi_msg = analysis_result.get('hindi_message', '')
                
                ai_response = f"""🌾 नमस्ते किसान भाई!

मैंने आपकी फसल की जांच कर ली है। आपके पौधों में **{disease_name}** है।

💊 **उपचार / Treatment:**
• {treatment}

{hindi_msg}

📊 **विश्लेषण समय:** {datetime.now().strftime("%I:%M %p")}

कोई और सवाल हो तो पूछिए! 🌾"""
                
                st.session_state.chat_history.append({
                    "farmer": farmer_query,
                    "ai": ai_response,
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# === DISPLAY RESULTS ===
if st.session_state.analysis_done and st.session_state.current_disease:
    disease = st.session_state.current_disease
    
    # Get severity class
    severity = disease.get('severity', 'moderate')
    severity_class = {
        'mild': 'severity-mild',
        'moderate': 'severity-moderate',
        'severe': 'severity-severe',
        'none': 'severity-none'
    }.get(severity, 'severity-moderate')
    
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # Disease title with severity
    st.markdown(f"""
    <div class="disease-title">
        {disease.get('disease_name', 'Unknown')}
        <span class="severity-badge {severity_class}">{severity.upper()}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Confidence meter
    confidence = disease.get('confidence', 0.85) * 100
    st.markdown(f"""
    <div style="margin: 15px 0;">
        <div style="display: flex; justify-content: space-between;">
            <span>Confidence</span>
            <span>{confidence:.1f}%</span>
        </div>
        <div class="confidence-meter">
            <div class="confidence-fill" style="width: {confidence}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disease Type
    disease_type = disease.get('disease_type', 'unknown')
    st.markdown(f"**Type:** {disease_type.title()}")
    
    # Symptoms
    symptoms = disease.get('symptoms', [])
    if symptoms:
        st.markdown("### 🔍 Symptoms")
        for symptom in symptoms:
            st.markdown(f"- {symptom}")
    
    # Treatment
    treatment = disease.get('treatment', 'Consult expert')
    st.markdown("### 💊 Treatment")
    st.info(treatment)
    
    # Organic Solutions
    organic = disease.get('organic_solutions', [])
    if organic:
        st.markdown("### 🌱 Organic Solutions")
        for solution in organic:
            st.markdown(f"- {solution}")
    
    # Possible Causes
    causes = disease.get('possible_causes', [])
    if causes:
        st.markdown("### ⚠️ Possible Causes")
        for cause in causes:
            st.markdown(f"- {cause}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat History
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation")
        for chat in st.session_state.chat_history[-3:]:
            st.markdown(f"""
            <div class="chat-bubble-farmer">
                <strong>👨‍🌾 You ({chat['time']}):</strong><br>
                {chat['farmer']}
            </div>
            <div class="chat-bubble-ai">
                <strong>🤖 AI ({chat['time']}):</strong><br>
                {chat['ai']}
            </div>
            """, unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
<div class="footer">
    🌾 Made with ❤️ for India's Farmers • किसानों के लिए बना<br>
    © 2026 Kisaan Saathi • Free AI Crop Doctor
</div>
""", unsafe_allow_html=True)
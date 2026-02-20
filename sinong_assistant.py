"""
sinong_assistant.py
Sinong-based Agricultural Assistant for Indian Farmers
USING MOCK MODE - Perfect for Hackathon Demo!
"""

import json
import random
from datetime import datetime

class SinongFarmerAssistant:
    """
    Sinong-based agricultural assistant for Indian farmers
    Using MOCK MODE for instant responses during hackathon
    """
    
    def __init__(self, use_mock=True):
        """
        Initialize Sinong assistant
        
        Args:
            use_mock: If True, uses realistic mock responses (RECOMMENDED FOR HACKATHON)
                     If False, would try to load real model (not recommended now)
        """
        self.use_mock = use_mock
        print("="*60)
        print("🌾 SINONG FARMER ASSISTANT")
        print("="*60)
        if use_mock:
            print("✅ MOCK MODE ACTIVE - Instant responses ready!")
            print("🎯 Perfect for hackathon demo")
        else:
            print("⚠️ Mock mode recommended for hackathon")
            print("💡 Use mock=True for instant responses")
        print("="*60)
    
    def generate_response(self, farmer_query, disease_info=None, weather=None, shops=None):
        """
        Generate conversational response in Hinglish
        
        Args:
            farmer_query: Text of what farmer said (in Hindi/English)
            disease_info: Output from disease detector
            weather: Weather data from teammate
            shops: Shop data from teammate
        
        Returns:
            Warm, helpful response in Hinglish
        """
        
        if not self.use_mock:
            # This would be where real model loads
            # But for hackathon, we always use mock
            print("⚠️ Real model not loaded - using mock response")
        
        return self._generate_mock_response(farmer_query, disease_info, weather, shops)
    
    def _generate_mock_response(self, farmer_query, disease_info, weather, shops):
        """Generate realistic mock responses for demo"""
        
        # Extract information with defaults
        disease_name = "पत्ती धब्बा रोग (Leaf Spot)"
        confidence = 0.92
        
        if disease_info and isinstance(disease_info, dict):
            disease_name = disease_info.get('disease_name', disease_name)
            confidence = disease_info.get('confidence', confidence)
        
        # Weather info
        weather_text = ""
        if weather:
            temp = weather.get('temperature', 28)
            humidity = weather.get('humidity', 65)
            rain = weather.get('rain_forecast', 'No rain expected')
            weather_text = f"\n🌤️ मौसम: {temp}°C, {humidity}% नमी, {rain}"
        
        # Shop info
        shops_text = ""
        if shops and len(shops) > 0:
            shops_text = "\n\n📍 **नजदीकी दुकानें:**"
            for i, shop in enumerate(shops[:3]):  # Show top 3 shops
                shop_name = shop.get('name', 'किसान स्टोर')
                distance = shop.get('distance', f'{i+1}km')
                shops_text += f"\n   • {shop_name} - {distance} दूर"
        
        # Confidence message
        confidence_msg = "पूरी विश्वास के साथ" if confidence > 0.9 else "अच्छे विश्वास के साथ"
        
        # Build the complete response
        response = f"""🌾 **नमस्ते किसान भाई!** 🙏

आपने जो फोटो भेजी है, उसे मैंने ध्यान से देखा। आपके पौधों में **{disease_name}** है। मैं {confidence_msg} ({confidence*100:.1f}%) यह बता रहा हूँ।

🌱 **समस्या क्या है?**
यह एक फफूंद जनित रोग है जो पत्तियों पर भूरे धब्बे बनाता है। नमी और गीले मौसम में यह तेजी से फैलता है।

💚 **जैविक उपाय:**
• नीम का तेल (2%) 7 दिन में एक बार छिड़कें
• गोबर के घोल (20%) का छिड़काव करें
• प्रभावित पत्तियों को हटा दें और गड्ढे में दबा दें

🧪 **रासायनिक उपाय:**
• मैंकोजेब 75% WP (2 ग्राम प्रति लीटर पानी) का छिड़काव करें
• या कॉपर ऑक्सीक्लोराइड (3 ग्राम प्रति लीटर) इस्तेमाल करें
• बाजार से "बाविस्टिन" या "डाइथेन एम-45" लें

{weather_text}

🛡️ **बचाव के उपाय:**
• पौधों के बीच उचित दूरी रखें
• पानी पत्तियों पर न गिरने दें
• फसल चक्र अपनाएं
• संक्रमित पौधों को खेत में न छोड़ें

{shops_text}

🌿 **सलाह:**
सुबह के समय दवा का छिड़काव करें जब धूप न हो। 10-15 दिन बाद दोबारा छिड़काव करें अगर जरूरत हो।

कोई और सवाल हो तो पूछिए! मैं आपकी मदद के लिए हूँ। 🌾

- आपका किसान AI सहायक
"""
        return response
    
    def get_response_in_english(self, farmer_query, disease_info=None, weather=None, shops=None):
        """English version for demo/testing"""
        
        disease_name = "Leaf Spot Disease"
        if disease_info and isinstance(disease_info, dict):
            disease_name = disease_info.get('disease_name', disease_name)
        
        response = f"""🌾 **Hello Farmer!** 🙏

I've analyzed your crop photo and detected **{disease_name}**.

🌱 **Organic Solution:**
• Spray neem oil (2%) every 7 days
• Apply cow dung solution (20%)
• Remove infected leaves

🧪 **Chemical Solution:**
• Spray Mancozeb 75% WP (2g per liter)
• Or use Copper Oxychloride (3g per liter)

🛡️ **Prevention:**
• Maintain proper plant spacing
• Avoid overhead watering
• Practice crop rotation

Your AI Farming Assistant 🌾
"""
        return response


# ==================== EASY INTEGRATION WITH YOUR APP ====================

def create_farmer_assistant():
    """
    Factory function to create assistant
    Just call this in your main app!
    """
    return SinongFarmerAssistant(use_mock=True)


# ==================== TEST THE ASSISTANT ====================

if __name__ == "__main__":
    # Test the mock assistant
    assistant = SinongFarmerAssistant(use_mock=True)
    
    # Sample data
    sample_disease = {
        "disease_name": "टमाटर अर्ली ब्लाइट",
        "confidence": 0.94,
        "severity": "moderate"
    }
    
    sample_weather = {
        "temperature": 28,
        "humidity": 75,
        "rain_forecast": "अगले 2 दिन बारिश नहीं"
    }
    
    sample_shops = [
        {"name": "किसान सीड स्टोर", "distance": "1.2km"},
        {"name": "हरित कृषि केंद्र", "distance": "2.5km"}
    ]
    
    # Test query
    farmer_query = "मेरे टमाटर के पौधों की पत्तियों पर भूरे धब्बे हैं, क्या करूं?"
    
    # Generate response
    print("\n" + "="*60)
    print("🤖 TESTING FARMER ASSISTANT")
    print("="*60)
    print(f"🗣️ Farmer: {farmer_query}")
    print("\n" + "-"*60)
    print("📢 Assistant:")
    print("-"*60)
    
    response = assistant.generate_response(
        farmer_query=farmer_query,
        disease_info=sample_disease,
        weather=sample_weather,
        shops=sample_shops
    )
    
    print(response)
    print("="*60)
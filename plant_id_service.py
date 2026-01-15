"""
plant_id_service.py
Handles all communication with the Plant.id API.
"""

import base64
import os
from typing import Optional, Dict, Any
from kindwise import PlantApi

class PlantIDService:
    """Service class for Plant.id API operations."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Plant.id API client.
        
        Args:
            api_key: Your Plant.id API key. If None, tries to get from environment.
        """
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('PLANT_ID_API_KEY')
        if not self.api_key:
            raise ValueError("Plant.id API key not provided. Set PLANT_ID_API_KEY in .env file.")
        
        # Initialize the API client
        self.api = PlantApi(api_key=self.api_key)
        
    def analyze_image(self, image_bytes: bytes) -> Optional[Dict[str, Any]]:
        """
        Analyze an image and return structured disease information.
        
        Args:
            image_bytes: Raw bytes of the uploaded image.
            
        Returns:
            Dictionary with disease information, or None if analysis fails.
        """
        try:
            print("🌱 Calling Plant.id API...")
            
            # Send image to Plant.id for identification
            identification = self.api.identification.identify(image_bytes)
            
            # Check if we have valid results
            if not identification.result or not identification.result.disease:
                print("⚠️ No disease results from API.")
                return self._create_healthy_result()
            
            # Get the top disease suggestion
            top_disease = identification.result.disease.suggestions[0]
            
            print(f"✅ Disease detected: {top_disease.name} (Confidence: {top_disease.probability:.1%})")
            
            # Format the result for your app
            return self._format_disease_result(top_disease)
            
        except Exception as e:
            print(f"❌ Plant.id API Error: {e}")
            return None
    
    def _format_disease_result(self, disease_suggestion) -> Dict[str, Any]:
        """Format Plant.id API response to match your app's structure."""
        
        # Extract details if available
        details = disease_suggestion.details or {}
        
        # Get treatment information
        treatment_info = details.get('treatment', {})
        treatments = []
        
        if treatment_info.get('biological'):
            treatments.append(f"🧪 Biological: {treatment_info['biological']}")
        if treatment_info.get('chemical'):
            treatments.append(f"⚗️ Chemical: {treatment_info['chemical']}")
        if treatment_info.get('prevention'):
            treatments.append(f"🛡️ Prevention: {treatment_info['prevention']}")
        
        # Default treatments if none found
        if not treatments:
            treatments = [
                "Remove infected leaves to prevent spread.",
                "Apply appropriate organic fungicide.",
                "Improve air circulation around plants."
            ]
        
        # Get symptoms
        symptoms_info = details.get('symptoms', {})
        symptoms = symptoms_info.get('localized', ['Yellowing leaves', 'Spots on foliage'])
        
        # Determine severity based on confidence
        confidence = disease_suggestion.probability
        if confidence > 0.8:
            severity = "severe"
        elif confidence > 0.5:
            severity = "moderate"
        else:
            severity = "mild"
        
        # Build the result dictionary
        return {
            "disease_detected": True,
            "disease_name": disease_suggestion.name,
            "disease_type": details.get('type', 'fungal'),  # fungal, bacterial, viral, pest
            "severity": severity,
            "confidence": round(confidence * 100, 1),
            "symptoms": symptoms[:3],  # Take first 3 symptoms
            "possible_causes": [
                "High humidity",
                "Poor air circulation", 
                "Contaminated soil or water"
            ],
            "treatment": treatments[:3],  # Take first 3 treatments
            "similar_images": disease_suggestion.similar_images or []
        }
    
    def _create_healthy_result(self) -> Dict[str, Any]:
        """Create a result for healthy plants."""
        return {
            "disease_detected": False,
            "disease_name": "Healthy",
            "disease_type": "healthy",
            "severity": "none",
            "confidence": 95.0,
            "symptoms": ["No disease symptoms detected"],
            "possible_causes": ["Good plant health maintained"],
            "treatment": [
                "Continue regular watering schedule",
                "Apply organic compost every 2 months",
                "Monitor for early signs of pests"
            ]
        }

# Singleton instance for easy import
plant_id_service = None

def get_plant_id_service(api_key: str = None):
    """Get or create the Plant.id service instance."""
    global plant_id_service
    if plant_id_service is None:
        plant_id_service = PlantIDService(api_key)
    return plant_id_service

# Quick test function
def test_service():
    """Test the Plant.id service with a sample image."""
    try:
        # Try to get service with environment variable
        service = get_plant_id_service()
        print("✅ PlantIDService initialized successfully!")
        
        # Test with a small sample (optional)
        # with open("Media/test_leaf.jpg", "rb") as f:
        #     result = service.analyze_image(f.read())
        #     print(f"Test result: {result}")
            
    except Exception as e:
        print(f"❌ Service test failed: {e}")
        print("💡 Make sure you have PLANT_ID_API_KEY in your .env file")

if __name__ == "__main__":
    test_service()
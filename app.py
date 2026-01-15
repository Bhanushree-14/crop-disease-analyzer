# app.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

app = FastAPI(title="Crop Disease API")

# Allow your Streamlit app (on localhost:8501) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Your Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rural Roots - Crop Disease API", "status": "active"}

@app.post("/disease-detection-file")
async def analyze_image(file: UploadFile = File(...)):
    """
    This is a MOCK endpoint that simulates the AI analysis.
    It returns a valid response matching your Streamlit app's expectations.
    Replace the mock logic with real AI model calls later.
    """
    # Accept the file (your frontend sends it here)
    contents = await file.read()

    # --- MOCK ANALYSIS LOGIC ---
    # For now, we'll return a realistic fake result so your app has data to display.
    # Later, you can connect this to your real 'LeafDiseaseDetector' class.
    mock_result = {
        "disease_detected": True,
        "disease_name": "Early Blight",
        "disease_type": "fungal",
        "severity": "moderate",
        "confidence": 88.5,
        "symptoms": [
            "Dark brown concentric rings on leaves",
            "Yellow halos around spots",
            "Lower leaves affected first"
        ],
        "possible_causes": [
            "High humidity and warm temperatures",
            "Poor air circulation between plants",
            "Infected plant debris in soil"
        ],
        "treatment": [
            "Remove and destroy infected leaves.",
            "Apply copper-based fungicide weekly.",
            "Water at the soil level (avoid wetting leaves).",
            "Ensure proper spacing for air flow."
        ],
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    # --- END MOCK LOGIC ---

    return mock_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
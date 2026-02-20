# sinong_gguf_wrapper.py
from llama_cpp import Llama
import os

class SinongGGUFFarmerAssistant:
    def __init__(self, model_path=r"{model_path}"):
        print("🔄 Loading Sinong GGUF model...")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # Context window
            n_threads=8,  # CPU threads
            n_gpu_layers=-1  # Use GPU if available
        )
        print("✅ Model loaded!")
    
    def generate_response(self, farmer_query, disease_info=None, weather=None, shops=None):
        prompt = f"""You are a friendly agricultural assistant helping an Indian farmer. Speak in simple Hinglish.

Farmer's question: {{farmer_query}}
Crop diagnosis: {{disease_info}}
Weather: {{weather}}
Nearby shops: {{shops}}

Provide helpful advice in simple language."""
        
        response = self.llm(
            prompt,
            max_tokens=512,
            temperature=0.7,
            stop=["</s>", "\\n\\n"]
        )
        return response['choices'][0]['text']
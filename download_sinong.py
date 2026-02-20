"""
download_sinong_gguf.py
Downloads Sinong Agricultural LLM in GGUF format from Hugging Face
GGUF is optimized for fast loading and smaller size
Source: https://huggingface.co/mradermacher/Sinong1.0-32B-GGUF

This version is RECOMMENDED FOR HACKATHON - smaller downloads, faster loading
"""

import os
import sys
import time
import requests
from pathlib import Path
from tqdm import tqdm

# Try to install tqdm if not available
try:
    from tqdm import tqdm
    print("✅ tqdm imported successfully")
except ImportError:
    print("📦 Installing tqdm...")
    os.system(f"{sys.executable} -m pip install tqdm")
    from tqdm import tqdm
    print("✅ tqdm installed and imported")

def ensure_dir(directory):
    """Create directory if it doesn't exist"""
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"📁 Ensured directory: {directory}")

def check_disk_space(required_gb=25):
    """Check if enough disk space is available"""
    import shutil
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    
    print(f"💾 Available disk space: {free_gb} GB")
    
    if free_gb < required_gb:
        print(f"⚠️  Warning: Less than {required_gb} GB free space")
        print(f"You need at least {required_gb}GB for this model")
        response = input("Continue anyway? (y/n): ")
        return response.lower() == 'y'
    return True

def download_sinong_gguf(model_quality="Q4_K_M", force_download=False):
    """
    Download Sinong model in GGUF format from Hugging Face
    
    Args:
        model_quality: "Q3_K_M", "Q4_K_M", or "Q5_K_M"
        force_download: If True, download even if exists
    
    Returns:
        Path to downloaded model file
    """
    
    # Model configurations
    models = {
        "Q3_K_M": {
            "url": "https://huggingface.co/mradermacher/Sinong1.0-32B-GGUF/resolve/main/Sinong1.0-32B.Q3_K_M.gguf",
            "size_gb": 16.1,
            "description": "Smallest, fastest - Good for quick demos"
        },
        "Q4_K_M": {
            "url": "https://huggingface.co/mradermacher/Sinong1.0-32B-GGUF/resolve/main/Sinong1.0-32B.Q4_K_M.gguf",
            "size_gb": 19.9,
            "description": "RECOMMENDED - Best quality/size balance for hackathon"
        },
        "Q5_K_M": {
            "url": "https://huggingface.co/mradermacher/Sinong1.0-32B-GGUF/resolve/main/Sinong1.0-32B.Q5_K_M.gguf", 
            "size_gb": 23.3,
            "description": "Highest quality - Best results, larger download"
        }
    }
    
    if model_quality not in models:
        print(f"❌ Invalid model quality: {model_quality}")
        print("Available options: Q3_K_M, Q4_K_M, Q5_K_M")
        return None
    
    model_info = models[model_quality]
    
    # Set save directory
    save_dir = os.path.abspath("./models/Sinong/gguf")
    ensure_dir(save_dir)
    
    # Set filename
    filename = f"Sinong1.0-32B.{model_quality}.gguf"
    save_path = os.path.join(save_dir, filename)
    
    print("\n" + "="*70)
    print(f"🚀 DOWNLOADING SINONG GGUF MODEL ({model_quality})")
    print("="*70)
    print(f"📦 Model: {model_info['description']}")
    print(f"📏 Size: {model_info['size_gb']} GB")
    print(f"📁 Save to: {save_path}")
    print(f"🔗 Source: {model_info['url']}")
    print("="*70)
    print("\n⚠️  Download time: 15-45 minutes depending on internet speed")
    print("⚠️  GGUF format loads faster and uses less RAM than full model\n")
    
    # Check if already downloaded
    if not force_download and os.path.exists(save_path):
        file_size_gb = os.path.getsize(save_path) / (1024**3)
        print(f"✅ Model already exists at: {save_path}")
        print(f"📏 Existing file size: {file_size_gb:.2f} GB")
        response = input("Download again? (y/n): ")
        if response.lower() != 'y':
            return save_path
    
    try:
        print("🔄 Starting download...")
        print("⏳ This may take a while. Progress bar will show below:\n")
        
        # Download with progress bar
        response = requests.get(model_info['url'], stream=True)
        response.raise_for_status()  # Check for HTTP errors
        
        total_size = int(response.headers.get('content-length', 0))
        
        if total_size == 0:
            print("⚠️  Could not determine file size, but continuing...")
        
        # Download with progress bar
        with open(save_path, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                desc="Downloading",
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
            ) as pbar:
                for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # Verify download
        if total_size > 0:
            downloaded_size = os.path.getsize(save_path)
            if downloaded_size < total_size * 0.99:  # Less than 99%
                print(f"\n⚠️  Warning: File may be incomplete ({downloaded_size}/{total_size} bytes)")
                retry = input("Download seems incomplete. Retry? (y/n): ")
                if retry.lower() == 'y':
                    os.remove(save_path)
                    return download_sinong_gguf(model_quality, force_download=True)
        
        print("\n" + "="*70)
        print(f"✅✅✅ DOWNLOAD COMPLETE! ✅✅✅")
        print("="*70)
        print(f"📁 Model saved to: {save_path}")
        print(f"📏 Final size: {os.path.getsize(save_path) / (1024**3):.2f} GB")
        
        # Create success indicator
        with open(os.path.join(save_dir, ".downloaded"), 'w') as f:
            f.write(f"Downloaded {filename} at: {time.ctime()}\n")
            f.write(f"Size: {os.path.getsize(save_path) / (1024**3):.2f} GB\n")
            f.write(f"Quality: {model_quality}")
        
        return save_path
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network error downloading model: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. The Hugging Face server might be busy - try again later")
        print("3. Try a different quality option (Q3_K_M is smallest)")
        print("4. If download keeps failing, use mock mode for hackathon")
        return None
        
    except Exception as e:
        print(f"\n❌ Unexpected error downloading model: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure you have enough disk space")
        print("2. Try running as administrator")
        print("3. If download fails, use mock mode for hackathon")
        return None

def create_gguf_integration_guide(model_path):
    """Create a guide for integrating the GGUF model with your app"""
    
    guide_path = os.path.join(os.path.dirname(os.path.dirname(model_path)), "USE_GGUF_MODEL.md")
    
    with open(guide_path, 'w') as f:
        f.write(f"""# Using Sinong GGUF Model in Your Project

## Model Location
Your downloaded GGUF model is at:
"""
Example script demonstrating how to use the Local Podcast Agent API
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def generate_podcast_with_agent(topic, length="short", host_name="Host", guest_name="Guest", model="qwen2.5:0.5b"):
    """
    Generate a podcast using AI agents
    """
    url = f"{BASE_URL}/api/generate"
    
    payload = {
        "topic": topic,
        "length": length,
        "host_name": host_name,
        "guest_name": guest_name,
        "model": model
    }
    
    print(f"Starting podcast generation for topic: '{topic}'")
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
    result = response.json()
    job_id = result.get("jobId")
    
    print(f"Job started with ID: {job_id}")
    
    # Poll for completion
    while True:
        status_response = requests.get(f"{BASE_URL}/api/status/{job_id}")
        status_data = status_response.json()
        
        print(f"Status: {status_data['status']} - {status_data.get('message', 'No message')}")
        
        if status_data['status'] == 'completed':
            print(f"Podcast generated successfully! Filename: {status_data['filename']}")
            return status_data['filename']
        elif status_data['status'] == 'failed':
            print(f"Podcast generation failed: {status_data['message']}")
            return None
        
        time.sleep(5)  # Wait 5 seconds before checking again

def generate_podcast_from_script(script):
    """
    Generate a podcast from a manual script
    """
    url = f"{BASE_URL}/api/manual"
    
    payload = {
        "script": script
    }
    
    print("Generating podcast from manual script...")
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
    result = response.json()
    filename = result.get("filename")
    
    print(f"Podcast generated from script! Filename: {filename}")
    return filename

def download_audio_file(filename):
    """
    Download the generated audio file
    """
    url = f"{BASE_URL}/api/audio/{filename}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Audio file downloaded: {filename}")
        return True
    else:
        print(f"Error downloading audio: {response.status_code}")
        return False

def list_available_models():
    """
    List available Ollama models
    """
    url = f"{BASE_URL}/api/models"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        models = response.json().get("models", [])
        print("Available models:")
        for model in models:
            print(f"  - {model}")
        return models
    else:
        print(f"Error getting models: {response.status_code}")
        return []

if __name__ == "__main__":
    print("Local Podcast Agent API Example")
    print("=" * 40)
    
    # Check if API is running
    try:
        health_check = requests.get(BASE_URL)
        if health_check.status_code == 200:
            print("✓ API is running")
        else:
            print("✗ API is not responding")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API. Make sure the API server is running on http://localhost:8000")
        exit(1)
    
    # List available models
    print("\nChecking available models...")
    models = list_available_models()
    
    # Example 1: Generate podcast from topic
    print("\nExample 1: Generating podcast from topic...")
    filename1 = generate_podcast_with_agent(
        topic="The Future of Artificial Intelligence",
        length="short",
        host_name="Tech Expert",
        guest_name="AI Researcher",
        model=models[0] if models else "qwen2.5:0.5b"
    )
    
    if filename1:
        download_audio_file(filename1)
    
    # Example 2: Generate podcast from manual script
    print("\nExample 2: Generating podcast from manual script...")
    sample_script = """
Host: Welcome to our tech podcast!
Guest: Thanks for having me today.
Host: Today we're discussing the future of artificial intelligence.
Guest: It's an exciting time for AI development.
Host: What do you think are the biggest challenges ahead?
Guest: Ethical considerations and bias in AI systems are major concerns.
Host: Thanks for your insights!
    """
    
    filename2 = generate_podcast_from_script(sample_script)
    
    if filename2:
        download_audio_file(filename2)
    
    print("\nExamples completed!")
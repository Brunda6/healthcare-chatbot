import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the GEMINI_API_KEY from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key was loaded correctly
if api_key is None:
    raise ValueError("API key not found. Make sure GEMINI_API_KEY is set in the .env file.")

# Configure Google Generative AI with the API key
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def GenerateResponse(input_text):
    # Generate the response using the model
    response = model.generate_content([
        "input: who are you? ",
        "output: HI. I'm a chatbot ",
        "input: what all can you do? ",
        "output: I can help you with any problems that you might be facing! How can I help you? ",
        f"input: {input_text}",
        "output: ",
    ])
    points = response.text.split(".")
    points = [point.strip() for point in points if point.strip()]  # Clean up extra spaces and empty points
    
    return points
    return response.text
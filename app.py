from flask import Flask, render_template, request, jsonify
import requests
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("MISTRAL_API_KEY:", os.getenv("MISTRAL_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

# Set up the Mistral AI API endpoint
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completionss"

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling user queries
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get("query")
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Mistral API request setup
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-7b",  # Adjust if needed, depending on the model
        "messages": [{"role": "user", "content": user_query}],
    }

    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)

    print("Mistral API response status code:", response.status_code)  # Log status code
    print("Mistral API response content:", response.text)  # Log the response content

    if response.status_code == 200:
        result = response.json()
        print(result)  # Debugging line to print the response
        return jsonify({"response": result["choices"][0]["message"]["content"]})
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Log the error response
        return jsonify({"error": "Error communicating with Mistral API"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

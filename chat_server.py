from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
from langdetect import detect

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up OpenAI API credentials
openai.api_key = 'YOUR_API_KEY'  # Replace with your OpenAI API key

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']

    try:
        # Detect the language of the message
        language = detect(message)

        # Choose the appropriate AI model based on the detected language
        if language == 'en':
            engine = 'text-davinci-003'
        elif language == 'hi':
            engine = 'text-davinci-XXXX'  # Example: Hindi AI model
        else:
            engine = 'text-davinci-002'  # Example: Default AI model for other languages

        # Set the temperature based on the length of the input message
        if len(message) <= 10:
            temperature = 0.8
        elif len(message) <= 20:
            temperature = 0.6
        else:
            temperature = 0.4

        # Generate the AI response
        response = openai.Completion.create(
            engine=engine,
            prompt=message,
            max_tokens=100,
            temperature=temperature,
            n=1,
            stop=None
        )
        reply = response.choices[0].text.strip()
    except Exception as e:
        reply = "I apologize, but I'm unable to provide a response at the moment."

    # Add CORS headers to the response
    response = jsonify({'reply': reply})
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow CORS for all URLs
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

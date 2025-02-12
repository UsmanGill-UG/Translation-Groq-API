from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app) 

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def translate_with_llama(text):
    try:
        # Use Groq's Llama 3 model to translate text
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Just only translate this text from English to Urdu: '{text}'",
                }
            ],
            model="llama3-70b-8192",
        )
        # Extract the response from Llama 3
        response = chat_completion.choices[0].message.content
        return {"translation": response}
    except Exception as e:
        return {"error": str(e)}

@app.route('/translate/', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400

    translation_result = translate_with_llama(text)
    if 'error' in translation_result:
        return jsonify({'error': translation_result['error']}), 500
    return jsonify(translation_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

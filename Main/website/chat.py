from flask import Flask, request, render_template, Response
from flask_cors import CORS
import google.generativeai as genai
import traceback

chat = Flask(__name__)
CORS(chat)

API_KEY = "AIzaSyA0SFx28KyIplkFnMSa9GBxHS4vdmNUlIQ"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')



@chat.route('/api/search', methods=['POST'])
def search():
    try:
        print("Received request:", request.data)
        
        data = request.json
        if not data:
            return Response("No data received", status=400)
        
        query = data.get('query')
        if not query:
            return Response("No query provided", status=400)

        response = model.generate_content(query)
        result_text = response.text if hasattr(response, 'text') else "No response received."

        return Response(result_text, mimetype="text/plain")

    except Exception as e:
        print("Error occurred:", traceback.format_exc())
        return Response(f"Error: {str(e)}\nDetails:\n{traceback.format_exc()}", status=500, mimetype="text/plain")

if __name__ == '__main__':
    chat.run(debug=True, port=5000)

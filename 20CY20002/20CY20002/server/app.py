from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_groq import ChatGroq
import os
import json
import pdfplumber

app = Flask(__name__)
CORS(app)

# Initialize ChatGroq
groq_api_key = ""# provide your own api key
llm = ChatGroq(groq_api_key=groq_api_key, model_name='llama-3.1-8b-instant')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
KNOWLEDGE_BASE = 'knowledge_base.json'

@app.route('/chat', methods=['POST'])
def chat():
    # data = request.get_json()
    # question = data.get('question', '')
    # if not question:
    #     return jsonify({'error': 'No question provided'}), 400

    # try:
    #     response = llm.invoke(question)
    #     return jsonify({'answer': response.content})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        # Load knowledge base
        with open(KNOWLEDGE_BASE, 'r') as kb:
            knowledge_base = json.load(kb)

        # Check if question matches any content in the knowledge base
        relevant_text = "You are a Ai assitant which will help us to answer questions based on provide infoamtion"
        for key, value in knowledge_base.items():
            relevant_text += value

        if relevant_text:
            # Pass the relevant text to the LLM prompt
            prompt = f"""Knowledge base content: {relevant_text}
            please read the infomation provided above and answer the following provided question if you find anyinformation related
            to the question.
            Remember: if you do not find any information related to question just give answer i am not able to answer this question
            \nQuestion: {question}\nAnswer:"""
            response = llm.invoke(prompt)
            return jsonify({'answer': response.content})
        else:
            return jsonify({'answer': "I am not able to answer this question."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file part in the request'}), 400

    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({'error': 'No selected file'}), 400

    # try:
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #     file.save(filepath)
    #     return jsonify({'message': 'File uploaded successfully'}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the file temporarily
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Check if the file is a PDF
        if file.filename.lower().endswith('.pdf'):
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"

            if not text.strip():
                return jsonify({'error': 'Unable to extract text from the PDF.'}), 400
        else:
            # Handle non-PDF files (e.g., plain text files)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

        # Update the knowledge base
        if not os.path.exists(KNOWLEDGE_BASE):
            with open(KNOWLEDGE_BASE, 'w') as kb:
                json.dump({}, kb)
        with open(KNOWLEDGE_BASE, 'r+') as kb:
            knowledge_base = json.load(kb)
            knowledge_base[file.filename] = text
            kb.seek(0)
            json.dump(knowledge_base, kb, indent=4)
            kb.truncate()

        return jsonify({'message': 'File uploaded and knowledge base updated successfully'}), 200
    except UnicodeDecodeError:
        return jsonify({'error': 'The uploaded file contains unsupported characters or an unknown encoding.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

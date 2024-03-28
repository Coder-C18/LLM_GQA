from flask import Flask, request, jsonify
from LLM_model.db_vector import insert_db, QA_Gemini, get_list_collection_name


# Define the Flask app
app = Flask(__name__)

# API endpoint for question-answering
@app.route('/qa', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get("question")
    collection_name = data.get("collection_name")

    if question is None or collection_name is None:
        return jsonify({"error": "Missing required fields: question and collection_name"}), 400

    try:
        answer = QA_Gemini(question, collection_name)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint for listing collection names
@app.route('/collections', methods=['GET'])
def list_collections():
    collection_names = get_list_collection_name()
    return jsonify({"collections": collection_names})

# API endpoint for inserting text into the database
@app.route('/insert', methods=['POST'])
def insert_text():
    data = request.get_json()
    text = data.get("text")
    collection_name = data.get("collection_name")

    if text is None or collection_name is None:
        return jsonify({"error": "Missing required fields: text and collection_name"}), 400

    try:
        insert_db(text, collection_name)
        return jsonify({"message": "Text inserted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False for production
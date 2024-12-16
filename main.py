from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Get the JSON data from the POST request
        data = request.get_json()
        
        # Ensure the data is a list or array and has exactly two numbers
        if not isinstance(data, list) or len(data) != 2:
            return jsonify({"error": "Request body must be a list containing exactly two numbers."}), 400
        
        # Extract the two numbers from the list
        first_number, second_number = data
        
        # Validate the inputs
        if not isinstance(first_number, (int, float)) or not isinstance(second_number, (int, float)):
            return jsonify({"error": "Both elements in the list must be numbers."}), 400
        
        # Determine whether to accept or not
        if first_number > second_number:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

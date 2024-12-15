from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Get the JSON data from the POST request
        data = request.get_json()
        
        # Extract the two numbers from the JSON data
        first_number = data.get('first_number')
        second_number = data.get('second_number')
        
        # Validate the inputs
        if first_number is None or second_number is None:
            return jsonify({"error": "Both 'first_number' and 'second_number' are required."}), 400
        
        if not isinstance(first_number, (int, float)) or not isinstance(second_number, (int, float)):
            return jsonify({"error": "Both 'first_number' and 'second_number' must be numbers."}), 400
        
        # Determine whether to accept or not
        if first_number > second_number:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

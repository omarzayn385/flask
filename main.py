from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Get raw data from the POST request
        raw_data = request.data.decode('utf-8').strip()
        
        # Split the numbers by a comma, since Retell might be sending "300000,485000"
        numbers = raw_data.split(',')
        
        # Ensure there are exactly two numbers
        if len(numbers) != 2:
            return jsonify({"error": "Request body must contain exactly two numbers separated by a comma."}), 400
        
        # Convert the numbers to integers or floats
        try:
            owner_price = float(numbers[0])
            estimated_value = float(numbers[1])
        except ValueError:
            return jsonify({"error": "Both elements must be numbers."}), 400
        
        # Determine whether to accept or not
        if owner_price > estimated_value:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

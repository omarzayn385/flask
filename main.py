from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Force Flask to parse the request body as JSON
        data = request.get_json(force=True)
        
        # Extract owner_price and estimated_value from the JSON payload
        owner_price = data.get('owner_price')
        estimated_value = data.get('estimated_value')
        
        # Validate the inputs
        if owner_price is None or estimated_value is None:
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' are required."}), 400
        
        if not isinstance(owner_price, (int, float)) or not isinstance(estimated_value, (int, float)):
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' must be numbers."}), 400
        
        # Determine whether to accept or not
        if owner_price > estimated_value:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Log the incoming request details for debugging
        raw_data = request.data.decode('utf-8').strip()
        content_type = request.content_type
        print(f"Raw Data: {raw_data}")
        print(f"Content-Type: {content_type}")
        
        # Try to parse the request as JSON
        try:
            data = request.get_json(force=True)
        except Exception as e:
            data = None

        # If parsing JSON failed, try to manually parse the raw data
        if data is None:
            try:
                data = json.loads(raw_data)  # Try to load raw data as JSON
            except Exception as e:
                return jsonify({"error": "Request body is not valid JSON"}), 400

        # Extract owner_price and estimated_value from the JSON payload
        owner_price = data.get("owner_price")
        estimated_value = data.get("estimated_value")
        
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

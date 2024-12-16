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
        headers = dict(request.headers)
        
        # Log everything for debugging
        print(f"\n===== INCOMING REQUEST =====")
        print(f"Content-Type: {content_type}")
        print(f"Headers: {headers}")
        print(f"Raw Data: {raw_data}")
        print(f"============================\n")
        
        # Try to parse the request as JSON
        try:
            data = request.get_json(force=True)  # force=True ignores Content-Type
            print(f"Parsed JSON Data: {data}")
        except Exception as e:
            print(f"JSON Parsing Error: {e}")
            data = None

        # If parsing JSON failed, try to manually parse the raw data
        if data is None:
            try:
                data = json.loads(raw_data)  # Try to load raw data as JSON
                print(f"Manually Parsed Data: {data}")
            except Exception as e:
                print(f"Manual Parsing Error: {e}")
                return jsonify({"error": "Request body is not valid JSON"}), 400

        # Extract owner_price and estimated_value from the JSON payload
        owner_price = data.get('owner_price')
        estimated_value = data.get('estimated_value')

        # Validate the inputs
        if owner_price is None or estimated_value is None:
            print(f"Missing owner_price or estimated_value in request body.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' are required."}), 400

        if not isinstance(owner_price, (int, float)) or not isinstance(estimated_value, (int, float)):
            print(f"Invalid data types for owner_price or estimated_value.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' must be numbers."}), 400

        # Determine whether to accept or not
        if owner_price > estimated_value:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        print(f"Unexpected Server Error: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

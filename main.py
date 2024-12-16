from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Log the incoming request for debugging
        raw_data = request.data.decode('utf-8').strip()
        content_type = request.content_type
        headers = dict(request.headers)
        
        print(f"\n===== INCOMING REQUEST =====")
        print(f"Content-Type: {content_type}")
        print(f"Headers: {headers}")
        print(f"Raw Data: {raw_data}")
        print(f"============================\n")

        # Step 1: Force JSON parsing, even if Content-Type is incorrect
        try:
            data = request.get_json(force=True)  # force=True parses JSON even if Content-Type is incorrect
            print(f"Parsed JSON Data (from request.get_json): {data}")
        except Exception as e:
            print(f"JSON Parsing Error (request.get_json): {e}")
            data = None

        # Step 2: If JSON parsing failed, manually parse the raw body
        if data is None:
            try:
                data = json.loads(raw_data)  # Try to load raw data as JSON
                print(f"Manually Parsed Data: {data}")
            except Exception as e:
                print(f"Manual Parsing Error: {e}")
                return jsonify({"error": "Request body is not valid JSON"}), 400

        # Step 3: Extract owner_price and estimated_value from the JSON payload
        owner_price = data.get('owner_price')
        estimated_value = data.get('estimated_value')

        # Step 4: Validate the inputs
        if owner_price is None or estimated_value is None:
            print(f"Missing owner_price or estimated_value in request body.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' are required."}), 400

        if not isinstance(owner_price, (int, float)) or not isinstance(estimated_value, (int, float)):
            print(f"Invalid data types for owner_price or estimated_value.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' must be numbers."}), 400

        # Step 5: Determine whether to accept or not
        if owner_price > estimated_value:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        print(f"Unexpected Server Error: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Step 1: Log the incoming request for debugging
        content_type = request.content_type
        headers = dict(request.headers)

        # Step 2: Force raw_data from WSGI input, even if request.form consumes it
        try:
            raw_data = request.environ['wsgi.input'].read(int(request.environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        except Exception as e:
            raw_data = ''
            print(f"WSGI Input Read Error: {e}")

        # Step 3: Fallback to request.data if raw_data is still empty
        if not raw_data:
            try:
                raw_data = request.data.decode('utf-8').strip()
            except Exception as e:
                print(f"request.data decoding error: {e}")
                raw_data = ''

        print(f"\n===== INCOMING REQUEST =====")
        print(f"Content-Type: {content_type}")
        print(f"Headers: {headers}")
        print(f"Raw Data from WSGI: {raw_data}")
        print(f"============================\n")

        data = None

        # Step 4: Handle application/json Content-Type
        if content_type == 'application/json':
            try:
                data = request.get_json(force=True, silent=True)
                print(f"Parsed JSON Data (from request.get_json): {data}")
            except Exception as e:
                print(f"JSON Parsing Error (request.get_json): {e}")

        # Step 5: Handle x-www-form-urlencoded
        if data is None and content_type == 'application/x-www-form-urlencoded':
            try:
                # Get form data
                data = request.form.to_dict()
                if not data:
                    print(f"request.form is empty. Trying to parse raw data as JSON.")
                    data = json.loads(raw_data)
                else:
                    # Attempt to convert numeric strings to int or float
                    for key, value in data.items():
                        if value.isdigit():
                            data[key] = int(value)
                        else:
                            try:
                                data[key] = float(value)
                            except ValueError:
                                pass  # Keep as string if not a number
                print(f"Parsed Form Data (from request.form): {data}")
            except Exception as e:
                print(f"Form Data Parsing Error: {e}")
        
        # Step 6: Fallback - handle raw data if Content-Type is text/plain, or if no Content-Type is provided
        if data is None and raw_data:
            try:
                data = json.loads(raw_data)  # Manually parse raw data as JSON
                print(f"Manually Parsed Data: {data}")
            except Exception as e:
                print(f"Manual Parsing Error: {e}")
                return jsonify({"error": "Request body is not valid JSON"}), 400

        # Step 7: Extract owner_price and estimated_value from the JSON payload
        if data is None:
            return jsonify({"error": "Request body is empty"}), 400

        # Adjusted extraction to navigate into 'args'
        args = data.get('args')
        if not args:
            print(f"'args' section is missing in the request body.")
            return jsonify({"error": "'args' section is required."}), 400

        owner_price = args.get('owner_price')
        estimated_value = args.get('estimated_value')

        # Step 8: Validate the inputs
        if owner_price is None or estimated_value is None:
            print(f"Missing owner_price or estimated_value in 'args'.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' are required within 'args'."}), 400

        if not isinstance(owner_price, (int, float)) or not isinstance(estimated_value, (int, float)):
            print(f"Invalid data types for owner_price or estimated_value.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' must be numbers."}), 400

        # Step 9: Determine whether to accept or not
        if owner_price > estimated_value:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        print(f"Unexpected Server Error: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))

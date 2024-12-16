from flask import Flask, request, jsonify
import os
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/ask_price', methods=['POST'])
def ask_price():
    try:
        # Log the incoming request details for debugging
        raw_data = request.data.decode('utf-8').strip()
        content_type = request.content_type
        app.logger.debug(f"Raw Data: {raw_data}")
        app.logger.debug(f"Content-Type: {content_type}")
        
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
                app.logger.error("JSON parsing failed.")
                return jsonify({"error": "Request body is not valid JSON"}), 400

        # Extract owner_price and estimated_value from the JSON payload
        owner_price = data.get('owner_price')
        estimated_value = data.get('estimated_value')
        
        app.logger.debug(f"Extracted owner_price: {owner_price}, estimated_value: {estimated_value}")
        
        # Validate the inputs
        if owner_price is None or estimated_value is None:
            app.logger.error("Missing required fields: 'owner_price' and/or 'estimated_value'.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' are required."}), 400
        
        if not isinstance(owner_price, (int, float)) or not isinstance(estimated_value, (int, float)):
            app.logger.error("Invalid data types for 'owner_price' and/or 'estimated_value'.")
            return jsonify({"error": "Both 'owner_price' and 'estimated_value' must be numbers."}), 400
        
        # Determine whether to accept or not
        if owner_price > estimated_value:
            app.logger.debug("Decision: don't accept")
            return jsonify({"result": "don't accept"})
        else:
            app.logger.debug("Decision: accept")
            return jsonify({"result": "accept"})
    except Exception as e:
        app.logger.exception("An unexpected error occurred.")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

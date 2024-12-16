from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/ask_price/<int:first_number>/<int:second_number>', methods=['POST'])
def ask_price(first_number, second_number):
    try:
        # Validate the inputs
        if not isinstance(first_number, (int, float)) or not isinstance(second_number, (int, float)):
            return jsonify({"error": "Both elements must be numbers."}), 400
        
        # Determine whether to accept or not
        if first_number > second_number:
            return jsonify({"result": "don't accept"})
        else:
            return jsonify({"result": "accept"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

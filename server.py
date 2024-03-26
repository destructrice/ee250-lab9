from flask import Flask, request, jsonify
# Import process1 from your main solution. Ensure process2 is also imported or defined.
from main import process1, process2

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the processing server'})

@app.route('/process1', methods=['POST'])
def process1_route():
    """Process data using process1."""
    # Get data from the request's JSON body
    data = request.get_json().get('data')
    if data is None:
        return jsonify({'error': 'No data provided'}), 400
    # Call process1 and return the result
    processed_data = process1(data)
    return jsonify(processed_data)

@app.route('/process2', methods=['POST'])
def process2_route():
    """Process data using process2."""
    # Get data from the request's JSON body
    data = request.get_json().get('data')
    if data is None:
        return jsonify({'error': 'No data provided'}), 400
    # Call process2 and return the result
    processed_data = process2(data)
    return jsonify(processed_data)

if __name__ == "__main__":
    app.run(host='localhost', port=5001)
    # Use the line below instead if you want to allow connections from any machine in the same network
    # app.run(host='0.0.0.0', port=5001)

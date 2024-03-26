from flask import Flask, request, jsonify

from main_sol import process1


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})

# TODO: Create a flask app with two routes, one for each function.
# The route should get the data from the request, call the function, and return the result.
@app.route('/process1', methods=['POST'])
def process1_route():
    """Process the data."""
    data = request.get_json()
    return jsonify(process1(data))


if __name__ == "__main__":
    app.run(host='localhost', port=5001) # This will only allow connections from the same machine
    #app.run(host='0.0.0.0', port=5001) # This will allow connections from any machine in the same network

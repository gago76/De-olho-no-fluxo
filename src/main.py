import os
import sys
import json
from datetime import datetime

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
# from src.models.user import db # Database not used in this version for simplicity
# from src.routes.user import user_bp # Default user blueprint not used

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Location data will be stored in a simple text file for this version
LOCATION_DATA_FILE = os.path.join(os.path.dirname(__file__), 'location_data.txt')

@app.route('/api/location', methods=['POST'])
def receive_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timestamp = data.get('timestamp') # Already formatted by client

        if latitude is None or longitude is None or timestamp is None:
            return jsonify({'status': 'error', 'message': 'Dados incompletos'}), 400

        # Store data
        with open(LOCATION_DATA_FILE, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - Lat: {latitude}, Lon: {longitude}, Client Timestamp: {timestamp}\n")
        
        print(f"Received data: Lat: {latitude}, Lon: {longitude}, Timestamp: {timestamp}")
        return jsonify({'status': 'success', 'message': 'Dados recebidos'}), 200
    except Exception as e:
        print(f"Error receiving location: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    # Ensure the location data file exists
    if not os.path.exists(LOCATION_DATA_FILE):
        with open(LOCATION_DATA_FILE, 'w') as f:
            f.write("Location Data Log\n")
            f.write("--------------------\n")
    app.run(host='0.0.0.0', port=5000, debug=True)


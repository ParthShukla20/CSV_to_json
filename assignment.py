from flask import Flask, request, jsonify,render_template
import pandas as pd
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def convert_to_json(csv_data):
    # Read the CSV data
    df = pd.read_csv(csv_data)
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict(orient='records')
    
    # Convert dot-separated keys to nested dictionaries
    def nest_keys(d):
        result = {}
        for k, v in d.items():
            parts = k.split('.')
            current_level = result
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            current_level[parts[-1]] = v
        return result
    
    # Apply nesting to all records
    nested_records = [nest_keys(record) for record in records]
    
    return nested_records

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            result = convert_to_json(file)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/' ,methods=['GET'])
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

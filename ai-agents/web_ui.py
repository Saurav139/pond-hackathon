from flask import Flask, render_template, jsonify
from environment_detection_agent import EnvironmentDetectionAgent
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def run_scan():
    try:
        agent = EnvironmentDetectionAgent()
        report = agent.run_full_scan()
        return jsonify(report.model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
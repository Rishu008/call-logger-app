from flask import Flask, request, jsonify
import json
import datetime

app = Flask(__name__)

LOG_FILE = "call_logs.txt"

# Function to convert timestamp (milliseconds) to a readable date
def convert_timestamp(timestamp):
    try:
        return datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "Invalid Timestamp"

# Route to receive call logs
@app.route('/upload_call_logs', methods=['POST'])
def upload_call_logs():
    try:
        call_logs = request.json  # Get JSON data from request
        
        if not call_logs:
            return jsonify({"error": "No data received"}), 400

        # Convert timestamps in all logs
        for log in call_logs:
            if "date" in log and log["date"].isdigit():
                log["date"] = convert_timestamp(log["date"])

        # Print the converted logs
        print("Converted Call Logs:", call_logs)

        # Save logs to a file
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"\n[{timestamp}] Received Call Logs:\n")
            json.dump(call_logs, file, indent=4, ensure_ascii=False)
            file.write("\n\n")

        return jsonify({"message": "Call logs received and saved successfully", "logs": call_logs}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test endpoint
@app.route('/')
def home():
    return "Flask Server is Running now!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

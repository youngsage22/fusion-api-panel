import requests
from flask import Flask, request, render_template, jsonify

# ⚠️ Replace this with your actual access token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
API_URL = "https://api.petrock.biz"

app = Flask(__name__)

def call_api(action, params=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    data = {"action": action}
    if params:
        data.update(params)
    response = requests.post(API_URL, headers=headers, json=data)
    try:
        return response.json()
    except:
        return {"error": "Invalid response", "raw": response.text}

@app.route("/")
def index():
    services = call_api("get_services")
    return render_template("index.html", services=services)

@app.route("/order", methods=["POST"])
def place_order():
    data = request.json
    imei = data.get("imei")
    service_id = data.get("service_id")
    result = call_api("place_order", {"imei": imei, "service_id": int(service_id)})
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
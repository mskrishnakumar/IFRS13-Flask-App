# app.py
from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Azure ML endpoint and API key
ENDPOINT = "https://uksouthwg-ncnbx.uksouth.inference.ml.azure.com/score"
API_KEY = os.environ["AZURE_API_KEY"]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form

        inputs = {
            "instrument_type": data['instrument_type'],
            "market_price_available": data['market_price_available'],
            "pricing_input_type": data['pricing_input_type'],
            "valuation_method": data['valuation_method'],
            "trade_volume": int(data['trade_volume']),
            "trade_currency": data['trade_currency'],
            "instrument_rating": data['instrument_rating'],
            "price_volatility_30d": float(data['price_volatility_30d']),
            "days_since_last_trade": int(data['days_since_last_trade']),
            "avg_curve_observability": float(data['avg_curve_observability'])
        }

        payload = {
            "input_data": {
                "columns": list(inputs.keys()),
                "index": [0],
                "data": [list(inputs.values())]
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        prediction = result[0] if isinstance(result, list) else result.get("predictions", ["Unknown"])[0]

        return render_template('index.html', prediction=prediction, summary=inputs)

    except Exception as e:
        return render_template('index.html', prediction=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
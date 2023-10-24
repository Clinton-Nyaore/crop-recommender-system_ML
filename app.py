from load_model import saved_model
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import json

app = Flask(__name__)

CORS(app, resources = {r'/api/*': {'origins': '*'}}) # needed for cross-domain requests, allow everything by default

# Loading crop recommendation model
crop_recommendation_model = saved_model

# Loading crop data into a dataframe
crop_data = pd.read_csv('fertiliser-application-stage.csv')

def crop_prediction(N, P, K, temperature, humidity, ph, rainfall):
    data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    data = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
    my_prediction = crop_recommendation_model.predict(data)
    final_prediction = my_prediction[0]

    return final_prediction


def fertilizer_recommendation(crop_name, dataframe):
    crop_row = dataframe[dataframe['CROP TYPE'] == crop_name]
    if not crop_row.empty:
        crop_ferts = crop_row.values.tolist()[0]
    else:
        crop_ferts = "Crop not found in the dataframe."

    return crop_ferts, crop_name


    # Define the fertilizer data with ratios
fertilizer_data = {
    'MAIZE': {'fertilizer': ['NPK', 'CAN'], 'ratios': [[23, 23, 0], [23, 0, 0, 4, 0]]},
    'BEANS': {'fertilizer': ['UREA'], 'ratios': [[23, 0, 0]]},
    'CUCUMBER': {'fertilizer': ['NPK'], 'ratios': [[23, 17, 17, 0, 0]]},
    'PASTURE GRASS': {'fertilizer': ['NPK'], 'ratios': [[23, 6, 0, 4, 0]]},
    'NAPIER GRASS': {'fertilizer': ['NPK'], 'ratios': [[23, 6, 0, 4, 0]]},
    'TOMATOES': {'fertilizer': ['NPK'], 'ratios': [[23, 6, 0, 4, 0]]},
    'ONION': {'fertilizer': ['DAP'], 'ratios': [[23, 46, 0, 0, 0]]},
    'SUGARCANE': {'fertilizer': ['NPK'], 'ratios': [[23, 17, 17, 0, 0]]},
    'AVOCADO': {'fertilizer': ['NPK'], 'ratios': [[23, 17, 17, 0, 0]]},
    'GREEN PEAS': {'fertilizer': ['NPK'], 'ratios': [[23, 23, 0, 4, 0]]},
    'CAPSICUM': {'fertilizer': ['NPK'], 'ratios': [[23, 17, 17, 0, 0]]},
    'COFFEE': {'fertilizer': ['DAP'], 'ratios': [[23, 46, 0, 0, 0]]}
}


@app.route('/api/crop-recommendation', methods=['GET'])
def get_crop_recommendation():
    # Get user input from request data or query parameters
    data = request.get_json() or request.args
    print('request data', data)
    # Extract user input data
    N = float(data.get('N', 0))
    P = float(data.get('P', 0))
    K = float(data.get('K', 0))
    temperature = float(data.get('temperature', 0))
    humidity = float(data.get('humidity', 0))
    ph = float(data.get('ph', 0))
    rainfall = float(data.get('rainfall', 0))

     # Recommended ratios
    constant_ph = 6.5

    # Perform crop prediction
    crop_name = crop_prediction(N, P, K, temperature, humidity, ph, rainfall).upper()
    
    # Retrieve fertilizer recommendation for the predicted crop
    crop_fert, _ = fertilizer_recommendation(crop_name, crop_data)
   
    response = {
    'recommended_crop': crop_name,
    'recommended_ph': constant_ph,
    'recommended_fertilizers': fertilizer_data[crop_name]['fertilizer'],
'pre_planting_fertilizer': {'fertilizer': fertilizer_data[crop_name]['fertilizer'][0], 'ratio': fertilizer_data[crop_name]['ratios'][0]},
'top_dressing_fertilizer': {'fertilizer': fertilizer_data[crop_name]['fertilizer'][1] if len(fertilizer_data[crop_name]['fertilizer']) > 1 else None, 'ratio': fertilizer_data[crop_name]['ratios'][1] if len(fertilizer_data[crop_name]['ratios']) > 1 else None}
}

    data = json.dumps(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

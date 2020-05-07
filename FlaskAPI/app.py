import flask
from flask import Flask, jsonify, request
import json
import numpy as np
import pickle



def load_model():
    file_name = "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

def load_scaler():
    return pickle.load(open('models/scaler.pkl','rb'))

app = Flask(__name__)
@app.route('/predict', methods=['GET'])
def predict():
    # stub input features
    request_json = request.get_json()
    x = request_json['input']
    #load scaler
    scaler = load_scaler()
    x_in = np.array(x).reshape(1,-1)
    x_scaled = scaler.transform(x_in)
    # load model
    model = load_model()
    prediction = (model.predict(x_scaled)[0]).astype(str)
    response = json.dumps({'response': prediction})
    return response, 200

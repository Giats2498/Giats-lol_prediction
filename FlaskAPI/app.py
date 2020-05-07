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

    

#clf = svm.SVC(C=100, break_ties=False, cache_size=200,class_weight=None,coef0=0.0,decision_function_shape='ovr',degree=3,gamma=0.01,kernel='rbf',max_iter=-1, probability= True, random_state= None, shrinking= True,tol=0.001, verbose=False)

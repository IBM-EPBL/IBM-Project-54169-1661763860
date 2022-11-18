import flask
import joblib
from flask import render_template, request
from flask_cors import CORS
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "DhAX4qyVNw37UViVP9kWoz2UcYqGM-CoKWoFQHNK5MCb"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)


@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predictSpecies():
    
    do = float(request.form['do'])
    ph = float(request.form['ph'])
    co = float(request.form['co'])
    bod = float(request.form['bod'])
    na = float(request.form['na'])
    tc = float(request.form['tc'])
    year = int(request.form['year'])
    X = [[do, ph, co, bod, na, tc, year]]
    payload_scoring = {"input_data": [{"field": [['do', 'ph', 'co', 'bod','na','tc','year']], "values":X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6a2cd8b2-6371-417f-9dae-f60de85b61aa/predictions?version=2022-11-16', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print("Final prediction :",predict)

    return render_template('predict.html',predict=predict)
    

if __name__ == '__main__':
    app.run(debug=True,port=5000)
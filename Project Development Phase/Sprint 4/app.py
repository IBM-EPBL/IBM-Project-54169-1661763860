import flask
import joblib
from flask import render_template, request
from flask_cors import CORS

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
    model = joblib.load('water.pkl')
    y_pred = model.predict(X)[0]
    return render_template('predict.html',predict=y_pred)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import joblib
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        try:
            gre_score = float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            research = request.form['research']

            if research == "yes":
                research = 1
            else:
                research = 0

            model = joblib.load('Final_Model.pickle')
            scaler = joblib.load('scaler_object.pickle')

            prediction = model.predict(
                scaler.transform(np.array([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])))
            prediction1 = round(prediction[0], 2) * 100

            return render_template('results.html', prediction=str(prediction1) + '%')

        except ValueError:
            return render_template('ValueError.html')
        except:
            return render_template('Error.html')




    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)  # running the app



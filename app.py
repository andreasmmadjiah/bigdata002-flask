from flask import render_template_string
from flask import Flask, request
from flask import jsonify, url_for
from flask import Flask, render_template, request
import pickle
import datetime
import json


from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import pandas as pd
import pickle

app = Flask(__name__)
# server = app.server

@app.route('/')
def Test():
   return render_template_string("""
   <html>
      <body>
         <form action = "{{url_for('predict') }}" method = "POST">
            <p>SepalLengthCm <input type = "number" step="0.001" name = "SepalLengthCm" /></p>
            <p>SepalWidthCm <input type = "number" step="0.001" name = "SepalWidthCm" /></p>
            <p>PetalLengthCm <input type = "number" step="0.001" name = "PetalLengthCm" /></p>
            <p>PetalWidthCm <input type = "number" step="0.001" name = "PetalWidthCm" /></p>
            <button id="button-a" type="submit">Submit</button>
         </form>
         
      </body>
   </html>
   """)

@app.route('/predict',methods=['POST'])
def predict():
   SepalLengthCm = request.form['SepalLengthCm']
   SepalWidthCm = request.form['SepalWidthCm']
   PetalLengthCm = request.form['PetalLengthCm']
   PetalWidthCm = request.form['PetalWidthCm']

   with open("trainning/model.pkl","rb") as pkl:
      clf = pickle.load(pkl)
   with open("trainning/label_enc.pkl","rb") as pkl:
      le = pickle.load(pkl)
   
   data = pd.DataFrame([[SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm]],columns=['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm'])
   
   pred = le.inverse_transform(clf.predict(data))[0]

   json_data= {'SepalLengthCm':SepalLengthCm,'SepalWidthCm':SepalWidthCm, 'PetalLengthCm':PetalLengthCm,"PetalWidthCm":PetalWidthCm}
   response={'status':200,'data':json_data,"prediction":pred,'created_at': datetime.datetime.now()}
   return render_template_string("""
   <html>
      <head>
         <title>Prediction Result! EYEYEYEYEY</title>
      </head>
      <body>
         <h3>Prediction Coba Sharing 11.22</h3>
         <div>This is the predicted classification oy <strong>{{ response.prediction }}</strong>.</div>
         <div>with data {{response.data}}</div>
      </body>
   </html>
   """,response=response)

if __name__=='__main__':
   app.run()
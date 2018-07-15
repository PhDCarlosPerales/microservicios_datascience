import pandas as pd
import pickle

from flask import Flask, Response
from flask import json
from flask import request


app = Flask(__name__)


filename = "../010_model/iris_model.pkl"
loaded_model = pickle.load(open(filename, 'rb'))



def predict_data(data_dict):
    data=pd.DataFrame(data_dict, index=[0])
    prediction= loaded_model.predict_proba(data)
    return prediction.tolist()[0]



def is_data_correct(data):
    """Check if data has the correct data"""
    if len(data) == 4:
        return True
    return False


@app.route("/predict",methods=['POST'])
def predict():
    response = Response(status=400, response="INFORMACION ERRONEA")
    try:
        data= request.get_json()
        print(data)
        if is_data_correct(data):
            prediction = {}
            prediction['Scores'] = predict_data(data)
            prediction['Input'] = data
            response = app.response_class(
                response=json.dumps(prediction),
                status=200
            )
        return response
    except Exception as ex:
        return Response(status=400, response=ex)



if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000)


# Windows Curl: don't like single quotes
# curl -H "Content-Type: application/json" --request POST --data "{\"s_l\":5.9,\"s_w\":3,\"p_l\":5.1,\"p_w\":1.8}" http://127.0.0.1:5000/predict

# Linux curl
# curl -i -X POST  -H "Content-Type:application/json"  -d  '{"s_l":5.9,"s_w":3,"p_l":5.1,"p_w":1.8}' 'http://127.0.0.1:5000/predict'


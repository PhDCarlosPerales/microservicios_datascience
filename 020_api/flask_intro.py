from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


@app.route("/predict",methods=['GET'])
def predict():
    response = app.response_class(
        response="Aquí viene la previsión",
        status=200
    )
    return response

if __name__ == "__main__":
    app.run()
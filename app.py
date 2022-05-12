from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def hoola():
    return 2

def prueba2():
    return 69
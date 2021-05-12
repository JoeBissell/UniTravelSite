from __main__ import app

# app = Flask(__name__)

print('hi')

@app.route("/joee")
def joee():
    return "Hey"
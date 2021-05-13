from flask import Flask, render_template

app = Flask(__name__)

@app.route('/airtravel')
def index():
    return render_template('AirTravel.html')







if __name__ == '__main__':
    app.run(debug = True)
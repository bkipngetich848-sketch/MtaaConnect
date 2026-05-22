from flask import *

#create flask application
app =Flask(__name__)

#define a simple route
@app.route('/api/home')
def home():
    return("Welcome to home API")

#@calculator route
@app.route('/api/calc', methods=['POST'])
def calc():
    num1=request.form["number1"]
    num2=request.form["number2"]

    add=int(num1)+int(num2)

    return jsonify({'answer':'add'})


if __name__=='__main__':
    app.run(debug=True)
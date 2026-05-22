from flask import *
import pymysql

#from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256
import os
from flask_cors import *

#create flask app
app=Flask(__name__)

CORS(app)

#config the storage path of product photos
os.makedirs('static/images',exist_ok=True)
app.config['UPLOAD_FOLDER']='static/images'

#create signin route
@app.route('/api/signup',methods=['POST'])
def signup():
   username=request.form['username']
   email=request.form['email']
   password=request.form['password']
   phone=request.form['phone']

   #connection to datebase
   connection=pymysql.connect(user='tikwet',host='mysql-tikwet.alwaysdata.net',password='modcom123',database='tikwet_sokogarden')

   #initialize a curser
   cursor=connection.cursor()

   #check if email exist in the database
   sqlc= 'select * from users where email= %s'
   datac=(email,)

   cursor.execute(sqlc,datac)


   #check if there is a email return
   userc=cursor.fetchone()

   if userc:
       return jsonify({"error":"users already exist!"})
   
   hashed_pass=pbkdf2_sha256.hash(password)

   #ceate the sql query
   sql='insert into users(username,email,password,phone) values(%s,%s,%s,%s)'

   #prepare data to replace the placeholder in the sql query
   data=(username,email,hashed_pass,phone)

   #use cursor to execute the query
   cursor.execute(sql,data)

   #commit the changes to the database
   connection.commit()

   #close the connection
   connection.close()

   #return a response after a successful registration
   return jsonify({'success':'user register successully'})

#signin route
@app.route('/api/signin',methods=['POST'])
def signin():
      email=request.form['email']
      password=request.form['password']

      #conect to database
      connection=pymysql.connect(user='tikwet',host='mysql-tikwet.alwaysdata.net',password='modcom123',database='tikwet_sokogarden')
      
      #create cursor
      cursor=connection.cursor(pymysql.cursors.DictCursor)

      #find the user email
      sql='select * from users where email= %s'
      data=(email,)

      cursor.execute(sql,data)

      user=cursor.fetchone()

      if user is None:
          return jsonify({'error':'wrong credentials!'})
      
      stored_pass=user['password']

      #compare enter password with the stored password
      if pbkdf2_sha256.verify(password, stored_pass):
       return jsonify({'success':    f"welcome back"})

      else:
       return jsonify({'error':'invalid credentials!'})


@app.route('/api/addproduct',methods=['POST'])
def product():
   
   product_name=request.form['product_name']
   product_description=request.form['product_description']
   product_cost=request.form['product_cost']

   #extract image data
   photo=request.files['photo']

   #get the image file
   filename=photo.filename

   #specify where the image will be saved
   photo_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)

   #save the photo
   photo.save(photo_path)

   connection=pymysql.connect(user='tikwet',host='mysql-tikwet.alwaysdata.net',password='modcom123',database='tikwet_sokogarden')

   #cursor
   cursor=connection.cursor()

   sql='insert into product_details(product_name,product_description,product_cost,product_photo)values(%s,%s,%s,%s)'
   data=(product_name,product_description,product_cost,filename)

   cursor.execute(sql,data)

   connection.commit()
   connection.close()

   return jsonify({'success':'product added successfully'})

#create a route to get all the products from the datatbase
@app.route('/api/getproducts',methods=['GET'])
def getproducts():
   connection=pymysql.connect(user='tikwet',host='mysql-tikwet.alwaysdata.net',password='modcom123',database='tikwet_sokogarden')

   # create cursor
   cursor=connection.cursor(pymysql.cursors.DictCursor)

   sql='select * from product_details'

   cursor.execute(sql)

   connection.close()

   products=cursor.fetchall()

   return jsonify({'products':products})


#Mpesa payment endpoint
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
      #  amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "rHhI33JakfzxyIiYV8LVIx1twKTPhjMIsGRBz9cHhzR8XMEi"
        consumer_secret = "gIyDdVJYU2MZKs1nSjGTsuAEhqWPMXdcxDCqYVHT7GDhxtONzgDC0ZxnYxxlB4VQ"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919 '
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})


   


    
#f __name__=='__main__':
 # app.run(debug=True)
 
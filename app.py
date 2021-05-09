from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os, sys,stat
import json

app = Flask(__name__)

app.secret_key = "secret_key"
#app.config["UPLOAD_FOLDER"] = "/static/img/"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://eurek8d7_common:common#123?@md-in-30.webhostbox.net:2083/eurek8d7_agrisell'
db = SQLAlchemy(app)

app.config["SQLALCHEMY_POOL_RECYCLE"] = 3600

# This table will contain the credential information of the farmers
class Farmer_credentials(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), nullable=False)
    pword = db.Column(db.String(100), nullable=False)

# This table will contain the credential information of the trader
class Trader_credentials(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), nullable=False)
    pword = db.Column(db.String(100), nullable=False)

# This table will contain the information of the farmer produce
class Farmer_produce(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), nullable=False)
    produce_type = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# This table contains the information of the traders
class Traders_info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)

# This table contains the information of the farmers
class Farmer_info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)

SQLALCHEMY_POOL_RECYCLE = 90

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/farmer_login", methods=["GET","POST"])
def farmer_login():
    if("farmer" in session):
        return redirect("/farmer_dashboard")

    if(request.method == "POST"):
        # Farmer Credentials
        farmer_creds = Farmer_credentials.query.filter_by().all()

        username = request.form.get("username")
        password = request.form.get("password")

        print("username : ", username)
        print("password : ", password)

        for i in range(0,len(farmer_creds)):
            if((username in farmer_creds[i].uname) and (password in farmer_creds[i].pword)):
                # Farmer Session started
                session["farmer"] = username
                # Redirect to the dashboard
                return redirect("/farmer_dashboard")

    return render_template("farmer_login.html")

@app.route("/trader_login", methods=["GET","POST"])
def reseller_login():
    # If Logged in, go to dashboard
    if("trader" in session):
        return redirect("/trader_dashboard")

    # Got Post request via login
    if(request.method == "POST"):
        trader_creds = Trader_credentials.query.filter_by().all()

        username = request.form.get("username")
        password = request.form.get("password")

        print("username : ", username)
        print("password : ", password)

        for i in range(0, len(trader_creds)):
            if ((username in trader_creds[i].uname) and (password in trader_creds[i].pword)):
                session["trader"] = username
                return redirect("/trader_dashboard")
                # return render_template("trader_dashboard.html")

    return render_template("trader_login.html")

@app.route("/farmer_dashboard", methods=["GET","POST"])
def farmer_dashboard():
    # If user is logged in
    if("farmer" in session):
        farm_produce = Farmer_produce.query.filter_by(uname=session["farmer"]).all()
        #farm_produce = Farmer_produce.query.all()
        print("session user : ",session["farmer"])
        return render_template("farmer_dashboard.html", produce=farm_produce, uname=session["farmer"])
    # Otherwise, go the login
    return redirect("/farmer_login")
    # return render_template("farmer_login.html")

@app.route("/trader_dashboard", methods=["GET","POST"])
def trader_dashboard():
    # if a trader is already logged in
    if("trader" in session):
        return render_template("trader_dashboard.html", title="Trader Dashboard", uname=session["trader"])
    # Otherwise, go to login
    return redirect("/trader_login")
    # return render_template("trader_login.html")

@app.route("/logout")
def logout():
    session["farmer"] = None
    session["trader"] = None
    session.pop("farmer")
    session.pop("trader")
    return redirect("/")

# A farmer specific function
@app.route("/add_produce" ,methods=["GET","POST"])
def add_produce():
    if("farmer" in session):
        #return render_template("add_produce.html")
        if(request.method == "POST"):
            print("I'm here")
            category = request.form.get("category")
            sub_category = request.form.get("name_of_crop")
            description = request.form.get("details_of_produce")
            quantity = request.form.get("quantity_of_produce")

            print("Let's print, what we recieved")
            print("category : ",category)
            print("sub_category : ",sub_category)
            print("description : ",description)
            print("quantity : ",quantity)

            # Fetch the images
            f1 = request.files["image1"]
            f2 = request.files["image2"]
            f3 = request.files["image3"]

            print("Category : ",category)
            print("Sub-Category : ",sub_category)
            print("Description : ",description)
            print("Quantity : ",quantity)

            # Perform some action (PENDING) -- Insert data into database
            entry = Farmer_produce(uname=session["farmer"],produce_type=category,crop_type=sub_category,description=description, quantity=quantity)
            db.session.add(entry)
            db.session.commit()

            # Take the posts from the database
            farm_produce = Farmer_produce.query.all()

            n = len(farm_produce)
            sno_produce = farm_produce[n-1].sno

            # directory_name = session["farmer"]
            img_path = os.path.dirname(os.path.abspath("app.py"))
            # img_path = "//static//img"

            sno_produce1 = str(sno_produce)

            img_path = img_path + "\static\images"

            s1 = "farmer_produce"

            img_path = os.path.join(img_path,s1)

            img_path = os.path.join(img_path,sno_produce1)

            # img_path = img_path + sno_produce1

            print("image_path : ",img_path)

            os.mkdir(img_path)

            app.config["UPLOAD_FOLDER"] = img_path


            # Create the directory according to the produce sno
            # os.mkdir(img_path,sno_produce)

            # Let's create a new image path
            #img_path_new = img_path + sno_produce

            # Let's check the new image path
            # print(img_path_new)
            # print(img_path_new)
            # print(img_path_new)

            # new_path_chmod_img1 = os.path.join(app.config["UPLOAD_FOLDER"], f1.filename)
            # new_path_chmod_img2 = os.path.join(app.config["UPLOAD_FOLDER"], f2.filename)
            # new_path_chmod_img3 = os.path.join(app.config["UPLOAD_FOLDER"], f3.filename)

            # os.chmod(app.config["UPLOAD_FOLDER"], stat.S_IRWXU)
            # os.chmod(app.config["UPLOAD_FOLDER"], stat.S_IWRITE)
            # os.chmod(app.config["UPLOAD_FOLDER"], stat.S_IWRITE)

            # Let's print the filenames
            print("f1_name : ",f1.filename)
            print("f2_name : ",f2.filename)
            print("f3_name : ",f3.filename)

            # Let's change the filename
            ex_arr = f1.filename.split(".")
            ex1 = ex_arr[1]

            f1.filename = "1." + str(ex1)

            #################

            ex_arr = f2.filename.split(".")
            ex1 = ex_arr[1]

            f2.filename = "2." + str(ex1)

            #################

            ex_arr = f3.filename.split(".")
            ex1 = ex_arr[1]

            f3.filename = "3." + str(ex1)

            ##################

            print("f1_filename : ",f1.filename)

            # Save the images in the folder
            f1.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f1.filename)))
            f2.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f2.filename)))
            f3.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f3.filename)))

            # Return the farmer dashboard
            return redirect("/farmer_dashboard")
            # return render_template("farmer_dashboard.html", produce=farm_produce)
        return render_template("add_produce.html")
    return redirect("/farmer_login")
    # return render_template("farmer_login.html")

# No need of any validation here.... Anyone with a url can access
@app.route("/traders")
def display_traders():
    # if("user" in session):
    trader_info = Traders_info.query.all()
    return render_template("traders_display.html", traders = trader_info, title="traders")
    # return redirect("/")

# No need of any validation here.... Anyone with a url can access
@app.route("/farmers")
def display_farmers():
    # if("user" in session):
    farmers = Farmer_info.query.all()
    return render_template("farmer_display.html", farmers=farmers, title="farmers")
    # return redirect("/")

# An open market...No validation needed
@app.route("/farmer_produce")
def display_farmer_produce():
    # if("farmer" in session):
    farm_produce = Farmer_produce.query.all()
    return render_template("farmers_produce_display.html", farmer_produce=farm_produce, title="Farmer Market")
    # return redirect("/")

# both validation required
@app.route("/new_farmer_registration", methods=["GET","POST"])
def new_farmer_registration():
    farmer_unames = db.session.query(Farmer_credentials.uname)

    if("farmer" in session):
        return redirect("/farmer_dashboard")
    if("trader" in session):
        return redirect("/trader_dashboard")
    if(request.method == "POST"):
        print("Something recieved")

        # farmer_unames = Farmer_credentials.query("uname").filter_by().all()

        name = request.form.get("name")
        phone_number = request.form.get("username")
        username = request.form.get("username")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        password = request.form.get("password")

        # Adding farmer display data in the farmer_info table
        entry = Farmer_info(name=name, phone_number=phone_number, uname=username, address=address, city=city,state=state,country="India")
        db.session.add(entry)
        db.session.commit()

        # Adding farmer credentials in the farmer_credential database
        entry = Farmer_credentials(uname=username, pword=password)
        db.session.add(entry)
        db.session.commit()

        return redirect("/farmer_login")
        # return render_template("index.html")
    return render_template("new_farmer_reg.html", farmer_unames = farmer_unames)

@app.route("/new_trader_registration", methods=["GET","POST"])
def new_trader_registration():
    trader_unames = db.session.query(Trader_credentials.uname)

    if("farmer" in session):
        return redirect("/farmer_dashboard")
    if("trader" in session):
        return redirect("/trader_dashboard")
    if(request.method == "POST"):
        print("Something recieved")

        name = request.form.get("name")
        phone_number = request.form.get("username")
        username = request.form.get("username")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        password = request.form.get("password")

        # Add the trader info to the Traders_info table
        entry = Traders_info(name=name, phone_number=phone_number, uname=username, address=address, city=city,state=state, country="India")
        db.session.add(entry)
        db.session.commit()

        # Add the credentials to the Trader_credential table
        entry = Trader_credentials(uname=username, pword=password)
        db.session.add(entry)
        db.session.commit()

        # Return to index
        return redirect("/trader_login")
        #return render_template("index.html")
    return render_template("new_trader_reg.html", trader_usernames = trader_unames)

@app.route("/delete_produce/<string:sno>")
def delete_produce(sno):
    if("farmer" in session):
        produce = Farmer_produce.query.filter_by(sno=sno).first()
        db.session.delete(produce)
        db.session.commit()
        return redirect("/farmer_dashboard")
    return redirect("/farmer_login")

# Purely for farmer, so that, it may edit its produce in the market
@app.route("/edit_produce/<string:sno>", methods=["GET","POST"])
def edit_produce(sno):
    # Session check
    if("farmer" in session):
        produce = Farmer_produce.query.filter_by(sno=sno).first()
        # Check if the "farmer" user has the authority to access the particular url
        if(produce.uname == session["farmer"]):
            prev_sno = sno
            if(request.method == "POST"):
                new_produce_category = request.form.get("category")
                new_name_of_crop = request.form.get("name_of_crop")
                new_details_of_produce = request.form.get("details_of_produce")
                new_quantity_of_produce = request.form.get("quantity_of_produce")

                produce.produce_type = new_produce_category
                produce.crop_type = new_name_of_crop
                produce.description = new_details_of_produce
                produce.quantity = new_quantity_of_produce

                db.session.commit()

                return redirect("/farmer_dashboard")

            print("kakaji")
            return render_template("edit_produce.html", produce=produce, title="edit_produce", uname=session["farmer"])
        # print("EDIT OPTION")
        return redirect("/farmer_dashboard")
    return redirect("/farmer_login")

if __name__ == "__main__":
    app.run()
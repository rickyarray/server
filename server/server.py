from flask import Flask, request, abort
from config import me, db
import json

app = Flask("server")


@app.get("/")
def home():
    return "Hello Universe"


@app.get("/test")
def test():
    return "This is a test page"


#  get /about to show your name
@app.get("/about")
def name():
    return "Ricky Array"



# ############################################################
# ######## API - PRODUCTS ####################################
# ############  JSON   #######################################
# ############################################################

@app.get("/api/about")
def about_data():
    return json.dumps(me)


# get /api/about/developer
# return full name
@app.get("/api/about/developer")
def developer():
    full_name= me["name"] + " " + me["last_name"]
    # python string formatting, f string
    return json.dumps(full_name)



# ***** GET CATEGORIES *****
@app.get("/api/categories")
def categories():
    all_cats = []
    cursor = db.products.find({})
    for product in cursor:
        category = product["category"]
        if category not in all_cats:
            all_cats.append(category)
    
    
    return json.dumps(all_cats)




# ***** THIS IS HOW YOU FIX THE ID ... MUST BE DONE EVERYTIME YOU READ FROM DB *****
def fix_id(record):
    record["_id"] = str(record["_id"])
    return record



# ***** PRODUCTS *****
@app.get("/api/products")
def get_products():
    products = []
    cursor = db.products.find({})
    for product in cursor: 
        products.append(fix_id(product))

    return json.dumps(products)


# this is how you save data "post" not 'get'
@app.post("/api/products")
def save_product():
    product = request.get_json()
    db.products.insert_one(product)
    print(product)
    return json.dumps(fix_id(product))


@app.get("/api/products/category/<cat>")
def get_by_category(cat):
    products = []
    cursor = db.products.find({ "category": cat })
    for prod in cursor:
        products.append(fix_id(prod))

    return json.dumps(products)



# get api/reports/total
# the total value of the catalog (sum of all prices)
@app.get("/api/reports/total")
def report_total():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(f"The total value is ${total}")


# starts the server
app.run(debug=True)

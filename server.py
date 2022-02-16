from flask import Flask, abort, request
from mock_data import catalog
from me_data import me
import random
import json 

#Create the server/app
app = Flask("server")


@app.route("/myaddress")
def get_myaddress():
    address = me["address"]    
    return address["street"] + " " + address["city"]
    #return f"2-2281 {address['street']}. {address['city']}"
    #return json.dumps(me)

@app.route("/", methods=["get"])
def home_page():
    return "Under Construction"

@app.route("/test")
def test():
    return "I'm a simple test"


@app.route("/about")
def about():
    return "Miles Inada"




#######################################################
################# API ENDPOINT ########################
#######################################################


@app.route("/api/catalog")
def get_catalog():
    return json.dumps(catalog)


@app.route("/api/catalog", methods=["POST"])
def save_products():
    product = request.get_json()

    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title is missing or too short.")

    if not "price" in product:
        return abort(400, "Price is missing.")

    if not isinstance(product["price"], int) or isinstance(product["price"], float):
        return abort(400, "Invaild price credentials.")

    if (product["price"]) < 1:
        return abort(400, "Invalid price, too low.")

    product["_id"] = random.randint(10000, 50000)
    catalog.append(product)
    return json.dumps(product)

# get /api.catalog/count
# return the num of products
@app.route("/api/catalog/count")
def get_count():
    count = len(catalog)
    return  json.dumps(count)
        
#get /api/catalog/sum
#return all prices sum
@app.route("/api/catalog/sum")
def get_sum():
    total = 0
    for prod in catalog:
        total += prod["price"]
    res = f"${total}"
    return json.dumps(res)

# get /api/product/<id>
# get a product by its _id
@app.route("/api/product/<id>")
def get_product(id):
    for prod in catalog:
        if id == prod["_id"]:
            return json.dumps(prod)

    return abort(404)


# get /api/product/most_expensive
@app.route("/api/product/most_expensive")
def get_most_expensive():
    pivot = catalog[0]
    
    for prod in catalog:
        if pivot["price"] > prod["price"]:
            pivot = prod

    return json.dumps(prod)



@app.route("/api/product/categories")
def get_category():

    res=[]
    for prod in catalog:
        catagory = prod["catagory"]
        if not catagory in res:
            res.append(catagory)
    return json.dumps(res)


@app.route("/api/catalog/<catagory>")
def products_by_catagory(catagory):
    for prod in catalog:
        #print(prod["title"])
        res = []
        if prod["catagory"] == catagory :
            print(prod["title"])
            res.append(prod)
        return json.dumps(res)

    
#######################################################
################# API ENDPOINT for coupon codes########
#######################################################


coupons = [
    {
        "code": "savenow",
        "discount": 10 ,
        "_id": 12
    },
    {
        "code": "blackfriday",
        "discount": 30 ,
        "_id": 15
    },
    {
        "code": "xmas",
        "discount": 20 ,
        "_id": 80
    }
]

@app.route("/api/coupons")
def get_coupons():
    return json.dumps(coupons)

@app.route("/api/coupons", methods=["POST"])
def save_coupouns():
    coupon = request.get_json()

    if not "code" in coupon or len(coupon["code"]) < 2:
        return abort(400, "Title is missing or too short.")

    coupon["_id"] = random.randint(10000, 50000)
    coupons.append(coupon)
    return json.dumps(coupon)

@app.route("/api/coupons/<code>")
def get_coupon(code):
    for coupon in coupons:
        if code == coupon["code"]:
            return json.dumps(coupon)

    return abort(404)

# start the server
app.run(debug=True)

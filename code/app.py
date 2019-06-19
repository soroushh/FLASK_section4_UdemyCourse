from flask import Flask, request
from flask_restful import Resource, Api
import json
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)
jwt = JWT(app, authenticate , identity) # /auth
items = []

class Item(Resource):

    @jwt_required()
    def get(self,name):
        # for item in items:
        #     if item["name"]== name:
        #         return(item)
        item = next(filter(lambda x: x["name"] == name , items), None)
        return({"item":item}), 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name , items), None):
            return {"message": "item '{}' already exists" .format(name)}, 400
        data = request.get_json()
        item = {"name":name , "price":data["price"]}
        items.append(item)
        return(item), 201

    def delete(self, name):
        # for item in items:
        #     if item["name"] == name :
        #         items.remove(item)
        #         return {"message": "item removed"}
        # return({"message":"item does not exist"})
        item = next(filter(lambda item: item["name"] == name , items), None)
        if item :
            items.remove(item)
            return{"message":"Item '{}'removed" .format(name)}
        return({"message":"Item does not exist"})

    def put(self, name):
        price = request.get_json()
        for item in items:
            if item["name"] == name :
                item["price"] = price["price"]
                return({"name": name , "price": price["price"]})
        return({"message": "Item does not exist."})

class Items(Resource):
    def get(self):
        return {"items":items} , 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)

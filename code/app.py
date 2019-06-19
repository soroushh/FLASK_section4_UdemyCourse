from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):

    def get(self,name):
        # for item in items:
        #     if item["name"]== name:
        #         return(item)
        item = next(filter(lambda x: x["name"] == name , items), None)
        return({"item":item}), 200 if item else 404

    def post(self, name):
        data = request.get_json()
        item = {"name":name , "price":data["price"]}
        items.append(item)
        return(item), 201

class Items(Resource):
    def get(self):
        return {"items":items} , 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Item(Resource):

    def get(self,name):
        items = {"book":1000}
        for item,price in items.items():
            if item== name:
                return(jsonify({"name":item, "price":price}))
        return(jsonify({"message":"item not found"}))


api.add_resource(Item, '/item/<string:name>')

app.run(port=5000)

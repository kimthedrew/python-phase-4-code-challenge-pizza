#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import validates
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class RestaurantList(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants])
    
    def post(self):
        data = request.get_json()
        new_restaurant = Restaurant(name=data['name'], address=data['address'])
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify(new_restaurant.to_dict()), 201
    
class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"errors": "Restaurant not found"}, 404
        return jsonify(restaurant.to_dict())
    
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"message": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    
class PizzaList(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        if 'name' not in data or 'ingredients' not in data:
            return {"errors": "Missing required fields"}, 400
        return jsonify([pizza.to_dict() for pizza in pizzas])
    
    def post(self):
        data = request.get_json()
        new_pizza = Pizza(name=data['name'], ingredients=data['ingredients'])
        db.session.add(new_pizza)
        db.session.commit()
        return jsonify(new_pizza.to_dict()), 201
    
class RestaurantPizzaList(Resource):
    def post(self):
        data =  request.get_json()

        if 'restaurant_id' not in data or 'pizza_id' not in data or 'price' not in data:
            return {"errors": "Missing required fields"}, 400
        
        restaurant = Restaurant.query.get(data['restaurant_id'])
        pizza = Pizza.query.get(data['pizza_id'])

        if not restaurant or not pizza:
            return {"errors": "Invalid restaurant or pizza ID"}, 400
        
        if not (1 <= data['price'] <= 30):
            return {"errors": "Price must be between 1 and 30"}, 400
        
        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                restaurant_id=data['restaurant_id'],
                pizza_id=data['pizza_id']
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"errors": "Database error occurred"}, 400
        

    

    
api.add_resource(RestaurantList, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzaList, '/pizzas')
api.add_resource(RestaurantPizzaList, '/restaurant_pizzas')

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # response = {
    #     "error": "Internal Server Error",
    #     "message": str(e)
    # }
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)

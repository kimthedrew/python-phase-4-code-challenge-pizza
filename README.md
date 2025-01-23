# Restaurant-Pizza API

This is a Flask-based API for managing restaurants, pizzas, and their relationships through `RestaurantPizza`. It provides endpoints to create, retrieve, update, and delete records for restaurants, pizzas, and their associations.

---

## Features
- Manage restaurants with `GET`, `POST`, and `DELETE` endpoints.
- Manage pizzas with `GET` and `POST` endpoints.
- Associate restaurants and pizzas using a `RestaurantPizza` model with validation for price.
- Handles invalid requests and database errors gracefully with appropriate error responses.

---

## Requirements
- Python 3.8+
- Flask
- Flask-Migrate
- Flask-SQLAlchemy
- Flask-RESTful

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
 ## Licence
 This project is licensed under the MIT license
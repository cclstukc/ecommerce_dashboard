from flask import Flask, jsonify, render_template, Response, abort, make_response
import sqlite3
import pathlib
import logging

# Set-up logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

working_directory = pathlib.Path(__file__).parent.absolute()
DATABASE = working_directory / 'CCL_ecommerce.db'
# http://localhost:5000/api/orders_over_time: OperationalError: sqlite3.OperationalError: no such table: orders
# Also tried:
# 1. Downloaded app.py
# 2. DATABASE = ('/Users/kurtcormack/Documents/ecommerce-dashboard/CCL_ecommerce.db')
# 3. working_directory = pathlib.Path(__file__).parent.resolve()
# 4. Issue appeared to be resolved (accidentally) when using conda env

# This is how the app connects to sqlite db and retrieves data:
def query_db(query: str, args=()) -> list:
    try:
        with sqlite3.connect(DATABASE) as conn:                 # Connects to sqlite db at the path specified by the DATABASE variable 
            cursor = conn.cursor()                              # Creates a cursor object, a tool which interacts with the db 
            result =  cursor.execute(query, args).fetchall()    # Executes the sql query and fetches the all the results
        return result
    except sqlite3.Error as e:
        logging.error("Database error: %s", e)
        abort(500, description="Database error occurred.")
# If error/exception occurs inside the try block the code in the except block is executed 
# Logging records events and messages, e.g. system processes, warnings and errors including exceptions that occur 

# This sets up our Flask application
# A simple way to create web servers, handle requests and return responses
# app = Flask(___name___) creates an instance of the Flask app, to define routes and handle requests 
# ___name____ is a built in python variable letting flask know where to look for resources, templates and components
# Everything else, e.g. defining routes, querying db, depends on the Flask instance which acts as a central controller

app = Flask(__name__)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# Handles http 404 errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

# Handles http 500 errors
@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({"error": "Internal server error"}), 500)


# How Flask will recognise routes/urls a user visits and how to respond 
@app.route('/')                                 # Defines route of app
def index() -> str:                             # Function that is executes when route is accessed
    return render_template('dashboard.html')    # Displays 'dashboard.html' template
# http://127.0.0.1:5000: TemplateNotFound jinja2.exceptions.TemplateNotFound: dashboard.html
# Also tried:
# 1. downloaded app.py
# 2. return render_template('/Users/kurtcormack/Documents/ecommerce-dashboard/templates/dashboard.html')

# Defines a route that returns a json repsonse containing data from sqlite db
# Each route function contain logic needed to fetch data, process it and return repsonse, e.g. .json file or .html template
# API (application programming interfaces) define how a server responds to requests
# SQL query passed query_db function returning data as .json file

# orders_over_time SQL -> json
@app.route("/api/orders_over_time")
def orders_over_time() -> Response:
    query = """
    SELECT order_date, COUNT(order_id) AS num_orders
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    """
    try:
        result = query_db(query)
        dates = [row[0] for row in result]
        counts = [row[1] for row in result]
        return jsonify({"dates": dates, "counts": counts})
    except Exception as e:
        logging.error("Error in /api/orders_over_time: %s", e)
        abort(500, description="Error processing data.")

# low_stock_levels SQL -> json
@app.route("/api/low_stock_levels")
def low_stock_levels() -> Response:
    query = """
    SELECT p.product_name, s.quantity
    FROM stock_level s
    JOIN products p ON s.product_id = p.product_id
    ORDER BY s.quantity ASC;
    """
    result = query_db(query)
    products = [row[0] for row in result]
    quantities = [row[1] for row in result]
    return jsonify({"products": products, "quantities": quantities})

# most_popular_products SQL -> json
@app.route("/api/most_popular_products")
def most_popular_products_new() -> Response:
    query = """
    SELECT p.product_id, p.product_name, SUM(od.quantity_ordered) AS total_quantity
    FROM order_details od
    JOIN products p ON od.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY total_quantity DESC
    LIMIT 10;
    """
    result = query_db(query)
    products = [
        {"product_id": row[0], "product_name": row[1], "total_quantity": row[2]}
        for row in result
    ]
    return jsonify(products)

# revenue_generation SQL -> json
@app.route("/api/revenue_generation")
def revenue_generation() -> Response:
    query = """
    SELECT o.order_date, SUM(od.price_at_time * od.quantity_ordered) AS total_revenue
    FROM order_details od
    JOIN orders o ON od.order_id = o.order_id
    GROUP BY o.order_date
    ORDER BY o.order_date;
    """
    result = query_db(query)
    dates = [row[0] for row in result]
    revenues = [row[1] for row in result]
    return jsonify({"dates": dates, "revenues": revenues})

# product_category_popularity SQL -> json
@app.route("/api/product_category_popularity")
def product_category_popularity() -> Response:
    query = """
    SELECT pc.category_name, SUM(od.price_at_time * od.quantity_ordered) AS total_sales
    FROM products p
    JOIN product_categories pc ON p.category_id = pc.category_id
    JOIN order_details od ON p.product_id = od.product_id
    GROUP BY pc.category_name
    ORDER BY total_sales DESC;
    """
    result = query_db(query)
    categories = [row[0] for row in result]
    sales = [row[1] for row in result]
    return jsonify({"categories": categories, "sales": sales})

# payment_method_popularity SQL -> json
@app.route("/api/payment_method_popularity")
def payment_method_popularity() -> Response:
    query = """
    SELECT pm.method_name, COUNT(p.payment_id) AS transaction_count
    FROM payments p
    JOIN payment_methods pm ON p.method_id = pm.method_id
    GROUP BY pm.method_name
    ORDER BY transaction_count DESC;
    """
    result = query_db(query)
    methods = [row[0] for row in result]
    counts = [row[1] for row in result]
    return jsonify({"methods": methods, "counts": counts})


# Running the application
# Launch app, make it live and respond to API requestss
# Activates Flask server
if __name__ == '__main__':      
    app.run(debug=True)

# debug=True allows for realtime code changes without restarting server which is beneficial for development
# should not be used in production as it can expose sensitive info or allow unauthorised code execution
# in production use debug=false

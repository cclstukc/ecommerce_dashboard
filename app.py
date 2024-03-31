from flask import Flask, jsonify, render_template, Response
import sqlite3
import pathlib


working_directory = pathlib.Path(__file__).parent.absolute()
DATABASE = working_directory / 'CCL_ecommerce.db'
# OperationalError: sqlite3.OperationalError: no such table: orders
# Also tried:
# 1. Downloaded app.py
# 2. DATABASE = ('/Users/kurtcormack/Documents/ecommerce-dashboard/CCL_ecommerce.db')


# This is how the app connects to sqlite db and retrieves data:
def query_db(query: str, args=()) -> list:
    with sqlite3.connect(DATABASE) as conn:                 # Connects to sqlite db at the path specified by the DATABASE variable 
        cursor = conn.cursor()                              # Creates a cursor object, a tool which interacts with the db 
        result =  cursor.execute(query, args).fetchall()    # Executes the sql query and fetches the all the results
    return result


# This sets up our Flask application
# A simple way to create web servers, handle requests and return responses
# app = Flask(___name___) creates an instance of the Flask app, to define routes and handle requests 
# ___name____ is a built in python variable letting flask know where to look for resources, templates and components
# Everything else, e.g. defining routes, querying db, depends on the Flask instance which acts as a central controller

app = Flask(__name__)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# How Flask will recognise routes/urls a user visits and how to respond 
@app.route('/')                                 # Defines route of app
def index() -> str:                             # Function that is executes when route is accessed
    return render_template('dashboard.html')    # Displays 'dashboard.html' template
# TemplateNotFound jinja2.exceptions.TemplateNotFound: dashboard.html
# Also tried:
# 1. downloaded app.py
# 2. return render_template('/Users/kurtcormack/Documents/ecommerce-dashboard/templates/dashboard.html')


# Defines a route that returns a json repsonse containing data from sqlite db
# Each route function contain logic needed to fetch data, process it and return repsonse, e.g. .json file or .html template
# API (application programming interfaces) define how a server responds to requests
@app.route("/api/orders_over_time")
def orders_over_time() -> Response:
 
# SQL query passed query_db function returning data as .json file
    query = """
    SELECT order_date, COUNT(order_id) AS num_orders
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    """
    result = query_db(query)
    dates = [row[0] for row in result]
    counts = [row[1] for row in result]
    return jsonify({"dates": dates, "counts": counts})


# Running the application
# Launch app, make it live and respond to API requestss
# Activates Flask server
if __name__ == '__main__':      
    app.run(debug=True)

# debug=True allows for realtime code changes without restarting server which is beneficial for development
# should not be used in production as it can expose sensitive info or allow unauthorised code execution
# in production use debug=false

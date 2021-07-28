from flask import Flask, json, render_template, jsonify
from app.services.DBservices import DBservices
from app.webhook.routes import webhook
db = DBservices()

# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app

# Defined for fetching template rendering modules 
def template_renderer():
    return render_template

def get_data():
    data = db.fetchAllData()
    return data

def jsonifyObj(obj):
    return jsonify(obj)

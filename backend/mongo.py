from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import os

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'flaskdb'
app.config['MONGO_URI'] = 'mongodb://zakaria:admin@mongodb:27017/flaskdb?authSource=admin'

mongo = PyMongo(app)

# Configuration CORS pour autoriser toutes les origines
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Route de test pour vérifier que l'API fonctionne
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Flask API is running', 'endpoints': {
        'GET /api/tasks': 'Get all tasks',
        'POST /api/task': 'Add a task',
        'PUT /api/task/<id>': 'Update a task',
        'DELETE /api/task/<id>': 'Delete a task'
    }})


@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    try:
        tasks = mongo.db.tasks
        result = []

        for field in tasks.find():
            result.append({'_id': str(field['_id']), 'title': field['title']})
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task', methods=['POST'])
def add_task():
    try:
        tasks = mongo.db.tasks 
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        title = data['title']
        
        # Utiliser insert_one() au lieu de insert() (déprécié dans pymongo 4.6.0)
        result = tasks.insert_one({'title': title})
        new_task = tasks.find_one({'_id': result.inserted_id})

        response_data = {'title': new_task['title'], '_id': str(new_task['_id'])}
        return jsonify({'result': response_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    try:
        tasks = mongo.db.tasks 
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        title = data['title']
        
        result = tasks.find_one_and_update(
            {'_id': ObjectId(id)}, 
            {"$set": {"title": title}}, 
            upsert=False,
            return_document=True
        )
        
        if not result:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({"result": {'title': result['title'], '_id': str(result['_id'])}}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        tasks = mongo.db.tasks
        response = tasks.delete_one({'_id': ObjectId(id)})

        if response.deleted_count == 1:
            result = {'message': 'record deleted'}
            return jsonify({'result': result}), 200
        else: 
            result = {'message': 'no record found'}
            return jsonify({'result': result}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


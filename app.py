from flask import Flask, make_response, request, jsonify
from flask_restful import Api, Resource
from simplexml import dumps
import json
import sqlite3
import re
import os

app = Flask(__name__)
api = Api(app)

def get_db_connection():
    records_db_file = os.path.dirname(os.path.abspath(__file__)) + '/records.db'
    conn = sqlite3.connect(records_db_file)
    conn.row_factory = sqlite3.Row
    return conn

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

@api.representation('application/json')
def output_json(data, code, headers=None):
	resp = make_response(json.dumps({'response' : data}), code)
	resp.headers.extend(headers or {})
	return resp

@api.representation('application/xml')
def output_xml(data, code, headers=None):
    if type(data) == str:
        data = {'message' : data}
    resp = make_response(dumps({'response' : data}), code)
    resp.headers.extend(headers or {})
    return resp

@api.representation('text/csv')
def output_text(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

class Records(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM records')
        records = [
            dict(id=row[0], name=row[1], address=row[2], phone_number=row[3])
            for row in cursor.fetchall()
        ]
        if records is not None:
            return records
        
    def post(self):
        conn = get_db_connection()
        cursor = conn.cursor()  
        new_name = request.json['name']
        new_address = request.json['address']
        new_phone_number = request.json['phone_number']
        sql = '''INSERT INTO records (name, address, phone_number)
                VALUES (?, ?, ?)'''
        cursor = cursor.execute(sql, (new_name, new_address, new_phone_number))
        conn.commit()
        message = f'Record with the id: {cursor.lastrowid} created successfully', 201
        return message

class Match(Resource):
    def get(self, pattern):
        conn = get_db_connection()
        key, value = re.split('[=<>]', pattern, 1)
        if key in ['id', 'phone_number']:
            cursor = conn.cursor()
            cursor = conn.execute(f'SELECT * FROM records WHERE {pattern}')
        else:
            conn.create_function('REGEXP', 2, lambda x, y: 1 if re.search(x,y) else 0)
            cursor = conn.cursor()
            cursor = conn.execute(f'SELECT * FROM records WHERE {key} REGEXP "{value}"')
        records = [
            dict(id=row[0], name=row[1], address=row[2], phone_number=row[3])
            for row in cursor.fetchall()
        ]
        if records is not None:
            return records

class Formats(Resource):
    def get(self):
        formats = ['json', 'xml', 'text']
        message = f'Supported formats are: {formats}'
        return message

api.add_resource(Records, '/records')
api.add_resource(Match, '/filter/<pattern>')
api.add_resource(Formats, '/formats-query')

if __name__ == '__main__':
   app.run(debug = True)
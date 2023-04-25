import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from db import db_session
from record import RenderList
from sqlalchemy import asc
from sqlalchemy.sql import text
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DEBUG = os.getenv('DEBUG') == 'True'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return 'Hello, World 2!'

@app.route('/records', methods = ['POST'])
@cross_origin()
def getRecords():
    data = RenderList.query.order_by(asc(RenderList.position)).all()
    return { 'values': [item.to_dictionary() for item in data] }

@app.route('/save/positions', methods = ['POST'])
@cross_origin()
def saveUpdatedRecordPattern():
    data = request.get_json()
    firstRecord = data['values']['firstRecord']
    secondRecord = data['values']['secondRecord']
    statement = text(f"UPDATE render_lists set title = case position when {firstRecord['position']} then '{secondRecord['title']}' when {secondRecord['position']} then '{firstRecord['title']}' end, type = case position when {firstRecord['position']} then '{secondRecord['type']}' when {secondRecord['position']} then '{firstRecord['type']}' end where position in ({firstRecord['position']}, {secondRecord['position']})")
    db_session.execute(statement)
    db_session.commit()
    return { 'first': firstRecord, 'second': secondRecord }
    
@app.route('/create', methods = ['POST'])
@cross_origin()
def createNewRecord():
    data = request.get_json()
    record = RenderList(data['title'], data['type'], data['link'])
    db_session.add(record)
    db_session.commit()
    return { 'success': True }

@app.route('/delete', methods = ['POST'])
@cross_origin()
def deleteRecords():
    data = request.get_json()
    position = data['position']
    statement = text(f"DELETE FROM render_lists WHERE position = {position}")
    db_session.execute(statement)
    db_session.commit()
    return { 'success': True }

@app.route('/update', methods = ['POST'])
@cross_origin()
def updateRecords():
    data = request.get_json()
    record = data['data']
    statement = text(f"UPDATE render_lists set title = '{record['title']}', type = '{record['type']}', link = '{record['link']}' where position = {record['position']}")
    db_session.execute(statement)
    db_session.commit()
    return { 'success': True }

@app.route('/bulk-update', methods = ['POST'])
@cross_origin()
def bulkUpdateRecords():
    data = request.get_json()
    records = data['values']
    start_query = 'UPDATE render_lists set '
    set_type = 'type = case position '
    set_title = 'title = case position '
    set_link = 'link = case position '
    where_string = 'where position in ('
    for item in records:
        set_type = set_type + f" when {item['position']} then '{item['type']}'"
        set_title = set_title + f" when {item['position']} then '{item['title']}'"
        set_link = set_link + f" when {item['position']} then '{item['link']}'"
        where_string = where_string + f" {item['position']},"
    query = start_query + set_type + ' end,' + set_title + ' end,' + set_link + ' end ' + where_string + ' 0)'
    statement = text(query)
    db_session.execute(statement)
    db_session.commit()
    return { 'success': True }


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug= DEBUG)

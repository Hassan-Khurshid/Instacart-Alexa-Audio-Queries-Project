from flask import *
from flask_ask import Ask, statement, question, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import exc
import db_functions as db_functions
import time
import json
import requests
import unidecode

import logging
import threading
import time

import pymysql
import csv
import sys

app = Flask(__name__)
application=app

ask = Ask(application, "/")
# # Database setup #

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/alexaresults", methods=['GET','POST'])
def runQuery():
    if request.method == 'POST':

        query = request.args.get('query')
        service_type = 'MySQL'
        db_type = request.args.get('db_type')

        # execute user query #
        result = db_functions.executeQuery(query, service_type, db_type)
        
        # render result #
        #print(query, ',', result[0], ',', service_type, ',' ,db_type)
        msg =  render_template('index.html', 
                            query=result[1], 
                            col_names=result[0], 
                            service_type='MySQL', 
                            db_type=db_type)
        return msg



## alexa decorators and setup ##
@ask.launch
def start_skill():
    welcome_msg = 'Hello! Invoke execute query to execute a sequel query!'
    return statement(welcome_msg)

# @ask.intent('ExecuteQuery')
# def countQuery(table, database):
#     db = 'abc_retail' if database=='a. b. c. retail' else 'cs527_instacart'
#     query = 'select count(*) from {}.{}'.format(db, table)
#     print(db)
#     result = db_functions.executeQuery(query, 'MySQL', db)

#     text = render_template('alexa.html', 
#                             query=result[1], 
#                             col_names=result[0], 
#                             service_type='MySQL', 
#                             db_type=db)

#     return statement('There are {} {}s'.format(result[1], table))


@ask.intent('SelectAllQuery')
def selectQuery(table, database, attribute=None, value=None, comparison=None, stringvalue=None):
    db = 'abc_retail' if database=='a. b. c. retail' else 'cs527_instacart'
    query = "select * from {}.{}".format(db, table)

    newattrib = attribute
    attributenew = attribute.split(' ')

    if len(attributenew)>1:
        newattrib = ""
        for i in range(len(attributenew)):
            if i == len(attributenew)-1:
                newattrib+=attributenew[i]
            else:
                newattrib+=attributenew[i]+'_'
    print(newattrib)

    if newattrib is not None:
        query += ' where {}'.format(newattrib)

        if stringvalue is not None:
            query += ' = \'{}\''.format(stringvalue)
        elif value is not None:
            if comparison == 'less':
                query += ' < {}'.format(value)
            elif comparison == 'greater':
                query += ' > {}'.format(value)
            elif 'less than or equal' in comparison:
                query += ' <= {}'.format(value)
            elif 'greater than or equal' in comparison:
               query += ' >= {}'.format(value) 
            elif 'not equal' in comparison:
                query += ' != {}'.format(value)
            else:
                query += ' = {}'.format(value)

    
    # payload = {'query':query, 'service_type':'MySQL', 'db_type':db}
    # headers = {'Content-type': 'text/html'}
    # request_url = 'http://127.0.0.1:5000/alexaresults?query={}&db_type={}'.format(query, db)

    #session = requests.Session()

    print(query)
    
    createResultCSV(query, 'MySQL', db)

    return statement('View directory to see results!')

def createResultCSV(query, service_type, db_type):
    result = db_functions.executeQuery(query, service_type, db_type)

    if len(result[1])>0:
        rows = list()
        for row in result[1]:
            rows.append(row)

        with open('queryresults.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=result[0], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for row in rows:
                row_dict = dict(zip(result[0],list(row)))
                #print(row_dict)

                writer.writerow(row_dict)



# def sendPostRequest(name, payload, headers, request_url):
#     time.sleep(2)
#     requests.post(url=request_url, headers = headers, allow_redirects=True)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)



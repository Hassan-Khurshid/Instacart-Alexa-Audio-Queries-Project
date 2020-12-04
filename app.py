from flask import *
from flask_ask import Ask, statement, question, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import exc
#from flask_migrate import Migrate 
#from config import DevelopmentConfig
import db_functions as db_functions
import time
import json
import requests
import unidecode


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

        mydata = request.args.get('query')
        print(mydata)

        # query = session['query']
        # if query == "":
        #     return render_template('index.html')
        # service_type = session['service_type']
        # database_type = session['db_type']
        # col_names = session['col_names']

        # capture start time #
        start_time = time.time()

        # execute user query #
        #result = db_functions.executeQuery(query, service_type, database_type)
       
        # capture end time #
        end_time = time.time()

        # render result #
        
        return render_template('index.html', 
                                query=result[1], 
                                col_names=result[0], 
                                service_type=service_type, 
                                db_type=database_type, 
                                time=(end_time-start_time))

## alexa decorators and setup ##
@ask.launch
def start_skill():
    welcome_msg = 'Hello! Invoke execute query to execute a sequel query!'
    return statement(welcome_msg)

@ask.intent('ExecuteQuery')
def countQuery(table, database):
    db = 'abc_retail' if database=='a. b. c. retail' else 'cs527_instacart'
    query = 'select count(*) from {}.{}'.format(db, table)
    print(db)
    result = db_functions.executeQuery(query, 'MySQL', db)

    text = render_template('alexa.html', 
                            query=result[1], 
                            col_names=result[0], 
                            service_type='MySQL', 
                            db_type=db)

    return statement('There are {} {}s'.format(result[1], table))


@ask.intent('SelectAllQuery')
def selectQuery(table, database, attribute=None, value=None, comparison=None, stringValue=None):
    db = 'abc_retail' if database=='a. b. c. retail' else 'cs527_instacart'
    query = "select * from {}.{}".format(db, table)

    if attribute is not None:
        query += ' where {}'.format(attribute)

        if stringValue is not None:
            query += ' = \'{}\''.format(stringValue)
        elif value is not None:
            if comparison == 'less':
                query += ' < {}'.format(value)
            elif comparison == 'greater':
                query += ' > {}'.format(value)
            elif comparison == 'less than or equal':
                query += ' <= {}'.format(value)
            elif comparison == 'greater than or equal':
               query += ' >= {}'.format(value) 
            elif comparison == 'not equal':
                query += ' != {}'.format(value)
            else:
                query += ' = {}'.format(value)

        
    print(query)
    result = db_functions.executeQuery(query, 'MySQL', db)

    headers = {}
    payload = {'query':result[1],'col_names':result[0], 'service_type':'MySQL', 'db_type':db}

    #session = requests.Session()
    requests.post(url='http://127.0.0.1:5000/alexaresults',data=payload)

    #print(result)
    # with app.app_context():
    #     msg = render_template('index.html', 
    #                         query=result[1], 
    #                         col_names=result[0], 
    #                         service_type='MySQL', 
    #                         db_type=db)

    #print(msg)
    return statement('View website to see results!')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)

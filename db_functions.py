import pymysql
import psycopg2

mysql_insta = pymysql.connect(
    host = 'instacart-db.cbujeonilgtq.us-east-2.rds.amazonaws.com',
    port = 3306,
    user = 'group3',
    password = 'group3pw!',
    db = 'cs527_instacart'
)

mysql_abc = pymysql.connect(
    host = 'instacart-db.cbujeonilgtq.us-east-2.rds.amazonaws.com',
    port = 3306,
    user = 'group3',
    password = 'group3pw!',
    db = 'abc_retail'
)

redshift = psycopg2.connect(
    user = "group3",
    password = "group3PW!",
    host = "redshift-cluster-1.cw5prwl0hut7.us-east-2.redshift.amazonaws.com",
    port = '5439',
    database = "instacart_red"
)

"""
Executes query requested by user. 
"""

def executeQuery(query, service_type, db_type):
    if service_type == 'MySQL':
        if db_type =='ABCRetail':
            cursor = mysql_abc.cursor()
        else:
            cursor = mysql_insta.cursor()
    else:
        cursor = redshift.cursor()

    cursor.execute(query)
    result = cursor.fetchall() 
    
    cols = cursor.description
    colNames = [col[0] for col in cols]
    
    cursor.close()
    return [colNames, result]

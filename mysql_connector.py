import pymysql

config = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila'
}

connection = pymysql.connect(**config)

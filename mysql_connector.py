import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'connect_timeout': 5
}


try:
    connection = pymysql.connect(**config)
except pymysql.MySQLError:
    print("No connection to MySQL server")
except pymysql.err.OperationalError:
    print("No connection to MySQL server")

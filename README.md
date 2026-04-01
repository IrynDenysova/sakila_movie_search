**Sakila Movie Search Console App**

A Python console application to search movies in the Sakila MySQL sample database. 
All searches are logged to MongoDB for analytics and statistics. 

 **Features**
* Search movies by keyword (title search)
* Filter movies by genre and year range
* Search movies by rating
* View recent queries
* View most popular searches
* Paginated results for better readability
* Query logging into MongoDB

 **Tech Stack**
* Python 3
* MySQL (Sakila database)
* MongoDB (logging system)
* PyMySQL
* python-dotenv
* tabulate

 **Installation**

1. Clone the repository:
 
```bash
git clone git@github.com:IrynDenysova/sakila_movie_search.git
cd sakila_movie_search
```
2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Create a .env file in the root directory with MySQL credentials:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=sakila

MONGO_URI=mongodb_connection_string
MONGO_COLLECTION=collection_name
MONGO_DB_NAME=db_name
```

 **Configuration**

- MySQL Connection is handled via pymysql and environment variables loaded using python-dotenv.
- MongoDB Logging stores search metadata: type, parameters, timestamp, and result count.

 **How to Run**

```bash
python main.py
```

_Menu Options:_
```
1. Search by keyword
2. Search by genre and year range
3. Search by rating
4. View last queries
5. View popular queries
0. Exit
```


 **Project Structure**

```
project
├── DB
│   └── mysql_connector.py
├── main.py
├── README.md
├── requirements.txt
├── run_pylint.sh
└── services
    ├── log_stats.py
    ├── log_writer.py
    ├── paginationer.py
    └── searcher.py
```

 **Logging**

Searches are logged to MongoDB:

```JS
{
    "timestamp": datetime.now(),
    "search_type": search_type,
    "params": params,
    "results_count": count
}
```
 **Statistics Features**

* Last queries grouped by parameters and timestamp
* Most frequent searches using aggregation pipelines

 **Example Query Flow**
* User selects search option
* SQL query executed with filters
* Results displayed in table format (tabulate)
* Query logged to MongoDB
* Stats updated automatically


 **Error Handling**
* MySQL connection errors handled safely
* MongoDB connection issues caught with specific exceptions
* Graceful fallback messages shown to user



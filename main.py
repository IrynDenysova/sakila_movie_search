from DB import mysql_connector
import pymysql
from services.searcher import search_by_title, search_by_genre_years, search_by_rating, view_genre_years, view_rating
from services.log_stats import get_unique_queries, get_stats_queries

try:
    with pymysql.connect(**mysql_connector.config) as connection:
        with connection.cursor() as cursor:
            while True:

                print("\n" + "*" * 50)
                print("FILM FINDER")
                print("*" * 50)
                print("1. Search by keyword")
                print("2. Search by genre and year range")
                print("3. Search by rating")
                print("4. View last queries")
                print("5. View popular queries")
                print("0. Exit")

                choice = input("ENTER YOUR CHOICE: ")
                if choice == "1":
                    search_by_title(connection)


                elif choice == "2":
                    genres = view_genre_years(connection)
                    search_by_genre_years(connection, genres)


                elif choice == "3":
                    view_rating(connection)
                    search_by_rating(connection)


                elif choice == "4":
                    get_unique_queries()


                elif choice == "5":
                    get_stats_queries()


                elif choice == "0":
                    break
                else:
                    print("Invalid choice")
except pymysql.MySQLError:
    print("No connection to MySQL server")
except pymysql.err.OperationalError:
    print("No connection to MySQL server")
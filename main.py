from DB import mysql_connector
import pymysql
from services.searcher import search_by_title, search_by_genre_years, search_by_rating, view_genre_years, view_rating
from services.log_stats import get_unique_queries, get_stats_queries

try:
    # Establish connection to MySQL database
    with pymysql.connect(**mysql_connector.config) as connection:
        # Create a cursor (not directly used here but keeps context consistent)
        with connection.cursor() as cursor:
            # Main application loop
            while True:
                # Display menu
                print("\n" + "*" * 50)
                print("FILM FINDER".center(50))
                print("*" * 50)
                print("1. Search by keyword")
                print("2. Search by genre and year range")
                print("3. Search by rating")
                print("4. View last queries")
                print("5. View popular queries")
                print("0. Exit")
                print("*" * 50)
                choice = input("ENTER YOUR CHOICE: ")
                # Handle menu options
                if choice == "1":
                    # Search films by title
                    search_by_title(connection)


                elif choice == "2":
                    # Show genres and then search by genre + years
                    genres = view_genre_years(connection)
                    search_by_genre_years(connection, genres)


                elif choice == "3":
                    # Show ratings and search by rating
                    view_rating(connection)
                    search_by_rating(connection)


                elif choice == "4":
                    # Show last executed queries
                    get_unique_queries()


                elif choice == "5":
                    # Show most popular queries
                    get_stats_queries()


                elif choice == "0":
                    break
                else:
                    print("Invalid choice")
# Handle database connection errors
except pymysql.MySQLError:
    print("No connection to MySQL server")
except pymysql.err.OperationalError:
    print("No connection to MySQL server")
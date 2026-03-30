import mysql_connector
import pymysql
from searcher import search_by_title, search_by_genre_years, search_by_rating, view_genre_years, view_rating
from log_stats import get_unique_queries, get_stats_queries


# def paginate_query(connection, query, count_query, params, limit=10):
#     """
#         Executes a paginated SQL query and prints results page by page.
#         :param connection: database connection
#         :param query: SQL query with LIMIT and OFFSET placeholders
#         :param params: tuple of query parameters
#         :param limit: number of records per page
#         :return: total number of fetched records
#         """
#
#     offset = 0
#     page = 1
#
#     try:
#             # Получаем общее количество записей
#         with connection.cursor() as cursor:
#             cursor.execute(count_query, params)
#             total = cursor.fetchone()[0]
#
#         if total == 0:
#             print("No films found.")
#             return 0
#
#         while offset < total:
#             print(f"\n----- Found {total} film(s) -----")
#             print(f"------ Page {page} ------")
#             with connection.cursor(DictCursor) as cursor:
#                 cursor.execute(query, params + (limit, offset))
#                 rows = cursor.fetchall()
#
#             if not rows:
#                 print("No more results.")
#             else:
#                 data = []
#                 for i, row in enumerate(rows, start=offset + 1):
#                     data.append([i,row['title'],row['release_year']])
#                 headers = ["Film ID","Title","Year"]
#                 print(tabulate(data,headers= headers ,tablefmt="outline"))
#
#             offset += len(rows)
#             page += 1
#
#             if offset < total:
#                 if input("\nShow more? (y/N): ").lower() != "y":
#                     break
#
#         return total
#
#     except Exception as e:
#         print(f"Error: {e}")
#         return 0
    


# def search_by_title(connection):
#     """Searches films by title with pagination."""
#     try:
#         title = input("Enter film title or part of title: ").strip()
#         if not title:
#             print("Empty input.")
#             return
#
#         query = """
#                 SELECT title, release_year
#                 FROM film
#                 WHERE title LIKE %s
#                 ORDER BY title
#                 LIMIT %s OFFSET %s
#             """
#         count_query = """SELECT COUNT(*)
#                 FROM film
#                 WHERE title LIKE %s"""
#         try:
#             total = paginate_query(connection, query, count_query,(f"%{title}%",))
#         except Exception as pagination_error:
#             print(f"Error during pagination: {pagination_error}")
#             return
#         try:
#             log_film("keyword", {"keyword": title}, total)
#         except Exception as log_error:
#             print(f"Logging error: {log_error}")
#
#     except Exception as input_error:
#         print(f"Unexpected error: {input_error}")
#
#
#
# def view_genre_years(connection) -> dict[str, tuple[int, int]]:
#     """ Displays min and max release years for each genre."""
#     genres_with_years = {}
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                     SELECT MIN(f.release_year), MAX(f.release_year), c.name
#                     FROM film as f
#                     JOIN film_category as fc
#                     ON f.film_id = fc.film_id
#                     JOIN category as c
#                     ON c.category_id = fc.category_id
#                     GROUP BY c.name""")
#
#             all_found_genres_years = cursor.fetchall()
#             table_data = []
#             for i,(min_year ,max_year, genre )in enumerate(all_found_genres_years,1):
#                 table_data.append([i,genre,f"{min_year}-{max_year}"])
#                 headers = ["Film ID","Genre","Years"]
#                 genres_with_years[genre] = (min_year,max_year)
#             print(tabulate(table_data,headers= headers ,tablefmt="outline"))
#     except Exception as e:
#         print(f"Error fetching genre data: {e}")
#     return genres_with_years
#
#
# def search_by_genre_years(connection, genres: dict[str, tuple[int, int]]):
#     """ Searches films by genre and year range with pagination."""
#     try:
#         while True:
#             search_genre = input("Enter the genre: ").strip().title()
#             if search_genre not in genres:
#                 print("Genre not found.")
#                 continue
#             elif not search_genre:
#                 print("Invalid genre.")
#                 continue
#             break
#
#         while True:
#             min_year = genres[search_genre][0]
#             max_year = genres[search_genre][1]
#             start_year = input(f"Enter start year from (default {min_year}): ").strip() or str(min_year)
#             end_year = input(f"Enter end year to (default {max_year}): ").strip() or str(max_year)
#
#             if not start_year.isdigit() or not end_year.isdigit():
#                 print("Year must be numeric.")
#                 continue
#             elif int(start_year) > int(end_year):
#                 print("Start year must be greater than end year.")
#                 continue
#             break
#
#         query = """
#             SELECT f.title, f.release_year
#             FROM film AS f
#             JOIN film_category AS fc ON f.film_id = fc.film_id
#             JOIN category AS c ON c.category_id = fc.category_id
#             WHERE c.name LIKE %s
#             AND f.release_year BETWEEN %s AND %s
#             ORDER BY f.title
#             LIMIT %s OFFSET %s
#         """
#         count_query = """SELECT COUNT(*)
#             FROM film AS f
#             JOIN film_category AS fc ON f.film_id = fc.film_id
#             JOIN category AS c ON c.category_id = fc.category_id
#             WHERE c.name LIKE %s
#             AND f.release_year BETWEEN %s AND %s
#             """
#
#         try:
#             total = paginate_query(
#                     connection,
#                     query, count_query,
#                     (search_genre, start_year, end_year))
#         except Exception as db_error:
#             print(f"Database error: {db_error}")
#             return
#         try:
#             log_film(
#                 "genre-year",
#                 {"genre": search_genre, "year from": start_year, "year to": end_year},
#                 total)
#         except Exception as log_error:
#             print(f"Logging error: {log_error}")
#
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#
#
# def view_rating(connection):
#     """ Displays all unique film ratings with descriptions."""
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("""SELECT distinct(rating),
#                                 CASE
#                                 WHEN rating = "NC-17" THEN "Adults only"
#                                 WHEN rating = "R" THEN "Restricted"
#                                 WHEN rating = "R-13" THEN "Parents Strongly Cautioned"
#                                 WHEN rating = "PG" THEN "Parental Guidance Suggested"
#                                 ELSE "General Audiences"
#                                 END AS description_rating
#                                 FROM film""")
#
#             all_ratings = cursor.fetchall()
#             headers = ["#", "Rating", "Description_rating"]
#             table_data = [[i, r[0], r[1]] for i, r in enumerate(all_ratings, 1)]
#
#             print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
#
#     except Exception as e:
#         print(f"Error fetching ratings: {e}")
#
#
#
#
# def search_by_rating(connection):
#     """ Searches films by rating with pagination."""
#     try:
#         rating = input("Enter rating (PG, G, NC-17...): ").strip().upper()
#
#         if not rating:
#             print("Invalid input.")
#             return
#
#         query = """
#                     SELECT title, rating, release_year
#                     FROM film
#                     WHERE rating LIKE %s
#                     ORDER BY release_year
#                     LIMIT %s OFFSET %s"""
#
#         count_query = """SELECT COUNT(*)
#                     FROM film
#                     WHERE rating LIKE %s
#                     ORDER BY rating"""
#         try:
#             total = paginate_query(connection, query, count_query,(f"%{rating}%",))
#         except Exception as db_error:
#             print(f"Database error: {db_error}")
#             return
#         try:
#             log_film("rating", {"keyword": rating}, total)
#         except Exception as log_error:
#             print(f"Logging error: {log_error}")
#
#     except Exception as e:
#         print(f"Unexpected error: {e}")


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
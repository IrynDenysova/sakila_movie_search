import mysql_connector
import pymysql
from pymysql.cursors import DictCursor
from log_writer import log_film
from log_stats import get_unique_queries, get_stats_queries
from tabulate import tabulate


def paginate_query(connection, query, params, limit=10, start_offset=0):
    offset = start_offset
    total = 0

    while True:
        with connection.cursor(DictCursor) as cursor:
            cursor.execute(query, params + (limit, offset))
            rows = cursor.fetchall()

        if not rows:
            if offset == start_offset:
                print("No films found.")
            else:
                print("No more results.")
            break

        for i, row in enumerate(rows, start=offset + 1):
            print(f"{i}. {row['title']} ({row['release_year']})")

        total += len(rows)

        if len(rows) < limit:
            break

        offset += limit

        user_input = input("\nShow more? (y/n): ").lower()
        if user_input != "y":
            break

    return total


def search_by_title(connection):
    title = input("Enter film title or part of title: ").strip()

    if not title:
        print("Empty input.")
        return

    query = """
        SELECT title, release_year
        FROM film
        WHERE title LIKE %s
        ORDER BY title
        LIMIT %s OFFSET %s
    """

    total = paginate_query(connection, query, (f"%{title}%",))

    log_film("keyword", {"keyword": title}, total)


def view_genre_years(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT MIN(f.release_year), MAX(f.release_year), c.name
            FROM film as f
            JOIN film_category as fc
            ON f.film_id = fc.film_id
            JOIN category as c
            ON c.category_id = fc.category_id
            GROUP BY c.name""")

        all_found_genres_years = cursor.fetchall()
        for film_id,(min_years ,max_year, genre )in enumerate(all_found_genres_years,1):
            print(f"{film_id}.{genre} ({min_years} -{max_year})")


def search_by_genre_years(connection):
    search_genre = input("Enter the genre: ").strip()
    start_year = input("Enter year from: ").strip()
    end_year = input("Enter year to (or Enter): ").strip() or start_year

    if not search_genre or not start_year:
        print("Invalid input.")
        return

    query = """
        SELECT f.title, f.release_year
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON c.category_id = fc.category_id
        WHERE c.name LIKE %s
        AND f.release_year BETWEEN %s AND %s
        ORDER BY f.title
        LIMIT %s OFFSET %s
    """

    total = paginate_query(
        connection,
        query,
        (f"%{search_genre}%", start_year, end_year)
    )

    log_film(
        "genre-year",
        {"genre": search_genre, "year from": start_year, "year to": end_year},
        total
    )


def view_rating(connection):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT distinct(rating),
                            CASE
                            WHEN rating = "NC-17" THEN "Adults only"
                            WHEN rating = "R" THEN "Restricted"
                            WHEN rating = "R-13" THEN "Parents Strongly Cautioned"
                            WHEN rating = "PG" THEN "Parental Guidance Suggested"
                            ELSE "General Audiences"
                            END AS description_rating
                            FROM film''')

        all_ratings = cursor.fetchall()
        headers = ["#", "Rating", "Description_rating"]
        table_data = [[i, r[0], r[1]] for i, r in enumerate(all_ratings, 1)]

        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))





def search_by_rating(connection):
    rating = input("Enter rating (PG, G, NC-17...): ").strip().upper()
    with connection.cursor() as cursor:
        cursor.execute('''
                    SELECT title, rating, release_year 
                    FROM film
                    WHERE rating LIKE %s ''', (f"%{rating}%",))
        all_ratings = cursor.fetchall()

        for i, (title, rating, release_year) in enumerate(all_ratings, 1):
            print(f"{i}. {title} ({rating}) - {release_year}")



        log_film("rating", {"keyword": rating}, len(all_ratings))




with pymysql.connect(**mysql_connector.config) as connection:
    with connection.cursor() as cursor:
        while True:
            print("\n" + "*" * 50)
            print("FILM FINDER")
            print("*" * 50)
            print("1. Search by keyword")
            print("2. Search by genre and year range")
            print("3. Search by rating")
            print("4. View popular or recent queries")
            print("0. Exit")

            choice = input("ENTER YOUR CHOICE: ")
            if choice == "1":
                search_by_title(connection)

            elif choice == "2":
                view_genre_years(connection)
                search_by_genre_years(connection)


            elif choice == "3":
                view_rating(connection)
                search_by_rating(connection)


            elif choice == "4":
                get_unique_queries()
                get_stats_queries()


            elif choice == "0":
                break
            else:
                print("Invalid choice")
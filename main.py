import mysql_connector
import pymysql
from log_writer import log_film
from log_stats import get_unique_queries, get_stats_queries


def paginate_query(connection, query, params, limit=10, start_offset=0):
    offset = start_offset
    total = 0

    while True:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
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
    end_year = input("Enter year to: ").strip() or start_year

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


with pymysql.connect(**mysql_connector.config) as connection:
    with connection.cursor() as cursor:
        while True:
            print("\n--- Sakila movie finder ---")
            print("1. Search by keyword")
            print("2. Search by genre and year range")
            print("3. View popular or recent queries")
            print("0. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                search_by_title(connection)

            elif choice == "2":
                view_genre_years(connection)
                search_by_genre_years(connection)


            elif choice == "3":
                """View popular or recent queries"""
                get_unique_queries()
                get_stats_queries()

            elif choice == "0":
                break
            else:
                print("Invalid choice")
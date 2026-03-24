import mysql_connector
import pymysql
from log_writer import log_film



def search_by_title(connection):
    title = input("Enter film title or part of title: ").strip().lower()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT title , release_year 
            FROM film
            WHERE title like %s """,
                       (f"%{title}%" ,))
        if not title:
            print(f"No film found.")
            return
        else:
            all_found_films = cursor.fetchall()
            for id_film,(film,year) in enumerate(all_found_films,1):
                print(f"{id_film}.{film}({year})")

    log_film("keyword",{"keyword": title},len(all_found_films))



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
    with connection.cursor() as cursor:
        search_genre = input("Enter the genre or tile of genre, you are looking for: ").strip().lower()
        start_year = input("Enter the year you are searching from: ").strip()
        end_year = input("Enter the year you are searching to (Enter if the year is the same): ").strip() or start_year
        cursor.execute("""
            SELECT f.title, f.release_year
            FROM film as f
            JOIN film_category as fc
            ON f.film_id = fc.film_id
            JOIN category as c
            ON c.category_id = fc.category_id
            WHERE c.name like %s AND f.release_year BETWEEN %s AND %s""",
                                    (f"%{search_genre}%",start_year,end_year,))
        all_found_movies = cursor.fetchall()
        if not all_found_movies:
            print(f"No film found.")
        for id_mov,(film, year) in enumerate(all_found_movies,1):
            print(f"{id_mov}.{film}({year})")

    log_film("genre-year",{"genre": search_genre,"year from": start_year, "year to": end_year},
             len(all_found_movies))




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
                pass

            elif choice == "0":
                break
            else:
                print("Invalid choice")
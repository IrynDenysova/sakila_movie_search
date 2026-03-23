import mysql_connector
import pymysql
from datetime import datetime


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
            for film,year in all_found_films:
                print(f"-{film},{year}")




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
        for min_years ,max_year, genre in all_found_genres_years:
            print(f"-{genre} - ({min_years} -{max_year})")


def search_by_genre_years(connection):
    with connection.cursor() as cursor:
        search_genre = input("Enter the genre, you are looking for: ").strip().lower()
        start_year = input("Enter the year you are searching from: ")
        end_year = input("Enter the year you are searching to (Enter if the year is the same): ") or start_year
        cursor.execute("""
            SELECT f.title, f.release_year
            FROM film as f
            JOIN film_category as fc
            ON f.film_id = fc.film_id
            JOIN category as c
            ON c.category_id = fc.category_id
            WHERE c.name = %s AND f.release_year BETWEEN %s AND %s""",
                                    (search_genre,start_year,end_year,))
        all_found_movies = cursor.fetchall()
        for film,year in all_found_movies:
            print(f"-{film},{year}")







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
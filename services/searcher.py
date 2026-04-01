from services.paginationer import paginate_query
from tabulate import tabulate
from .log_writer import log_film


def search_by_title(connection):
    """Searches films by title with pagination."""
    try:
        print("\n" + "-" * 35)
        print("Searching films by title.(0 to back)")
        print("-" * 35)
        title = input("Enter film title or part of title: ").strip()

        if title == "0":
            return
        if not title:
            print("Empty input.")
            return

        # Main query with pagination (LIMIT + OFFSET)
        query = """
                SELECT title, release_year
                FROM film
                WHERE title LIKE %s
                ORDER BY title
                LIMIT %s OFFSET %s
            """

        # Query to count total matching records
        count_query = """SELECT COUNT(*)
                FROM film
                WHERE title LIKE %s"""
        # Execute paginated query
        try:
            total = paginate_query(connection, query, count_query,(f"%{title}%",))
        except Exception as pagination_error:
            print(f"Error during pagination: {pagination_error}")
            return
        # Log search result
        try:
            log_film("keyword", {"keyword": title}, total)
        except Exception as log_error:
            print(f"Logging error: {log_error}")

    except Exception as input_error:
        print(f"Unexpected error: {input_error}")



def view_genre_years(connection) -> dict[str, tuple[int, int]]:
    """ Displays min and max release years for each genre."""
    genres_with_years = {}
    genres = []
    try:
        with connection.cursor() as cursor:
            # Get min/max year per genre
            cursor.execute("""
                    SELECT MIN(f.release_year), MAX(f.release_year), c.name
                    FROM film as f
                    JOIN film_category as fc
                    ON f.film_id = fc.film_id
                    JOIN category as c
                    ON c.category_id = fc.category_id
                    GROUP BY c.name""")

            all_found_genres_years = cursor.fetchall()
            table_data = []
            # Format results
            for i,(min_year ,max_year, genre )in enumerate(all_found_genres_years,1):
                table_data.append([i,genre,f"{min_year}-{max_year}"])
                headers = ["Film ID","Genre","Years"]
                genres_with_years[genre] = (min_year,max_year, i)
                genres.append(genre)
            print(tabulate(table_data,headers= headers ,tablefmt="outline"))
    except Exception as e:
        print(f"Error fetching genre data: {e}")
    return genres_with_years


def search_by_genre_years(connection, genres: dict[str, tuple[int, int]]):
    """ Searches films by genre and year range with pagination."""
    try:
        # Ask user for genre until valid
        while True:
            print("\n" + "-" * 35)
            print("Searching films by genre.(0 to back)")
            print("-" * 35)
            search_genre = input("Enter the genre: ").strip().title()

            if search_genre.isnumeric():
                genre_names = sorted(genres.keys())
                genre_id = int(search_genre) - 1
                search_genre = genre_names[genre_id]


            if search_genre == "0":
                return

            if search_genre not in genres:
                print("Genre not found.")
                continue

            elif not search_genre:
                print("Invalid genre.")
                continue
            break

        # Ask user for year range
        while True:
            min_year = genres[search_genre][0]
            max_year = genres[search_genre][1]
            print("\n" + "-" * 35)
            print("Searching films by year(s).(0 to back)")
            print("-" * 35)
            start_year = input(f"Enter start year from (default {min_year}): ").strip()
            start_year = start_year or str(min_year)
            if start_year == "0":
                return
            end_year = input(f"Enter end year to (default {max_year}): ").strip() or str(max_year)
            if end_year == "0":
                return

            # Validate input
            if not start_year.isdigit() or not end_year.isdigit():
                print("Year must be numeric.")
                continue
            elif int(start_year) > int(end_year):
                print("Start year must be greater than end year.")
                continue
            break

        query = """
            SELECT f.title, f.release_year
            FROM film AS f
            LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
            LEFT JOIN category AS c ON c.category_id = fc.category_id
            WHERE c.name LIKE %s
            AND f.release_year BETWEEN %s AND %s
            ORDER BY f.title
            LIMIT %s OFFSET %s
        """

        count_query = """SELECT COUNT(*)
            FROM film AS f
            LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
            LEFT JOIN category AS c ON c.category_id = fc.category_id
            WHERE c.name LIKE %s
            AND f.release_year BETWEEN %s AND %s
            """

        try:
            total = paginate_query(
                    connection,
                    query, count_query,
                    (search_genre, start_year, end_year))
        except Exception as db_error:
            print(f"Database error: {db_error}")
            return
        try:
            log_film(
                "genre-year",
                {"genre": search_genre, "year_from": start_year , "year_to": end_year},
                total)
        except Exception as log_error:
            print(f"Logging error: {log_error}")

    except Exception as e:
        print(f"Unexpected error: {e}")


def view_rating(connection):
    """ Displays all unique film ratings with descriptions."""
    try:
        with connection.cursor() as cursor:
            # Query with CASE to map rating descriptions
            cursor.execute("""SELECT distinct(rating),
                                CASE
                                WHEN rating = "NC-17" THEN "Adults only"
                                WHEN rating = "R" THEN "Restricted"
                                WHEN rating = "R-13" THEN "Parents Strongly Cautioned"
                                WHEN rating = "PG" THEN "Parental Guidance Suggested"
                                ELSE "General Audiences"
                                END AS description_rating
                                FROM film""")

            all_ratings = cursor.fetchall()
            headers = ["#", "Rating", "Description_rating"]
            table_data = [[i, r[0], r[1]] for i, r in enumerate(all_ratings, 1)]

            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    except Exception as e:
        print(f"Error fetching ratings: {e}")




def search_by_rating(connection):
    """ Searches films by rating with pagination."""
    try:
        print("\n" + "-" * 35)
        print("Searching films by rating.(0 to back)")
        print("-" * 35)
        rating = input("Enter rating (PG, G, NC-17...): ").strip().upper()
        if rating == "0":
            return

        if not rating:
            print("Invalid input.")
            return

        query = """
                    SELECT title, rating, release_year 
                    FROM film
                    WHERE rating LIKE %s
                    ORDER BY release_year
                    LIMIT %s OFFSET %s"""

        count_query = """SELECT COUNT(*)
                    FROM film
                    WHERE rating LIKE %s
                    ORDER BY rating"""
        try:
            total = paginate_query(connection, query, count_query,(f"%{rating}%",))
        except Exception as db_error:
            print(f"Database error: {db_error}")
            return
        try:
            log_film("rating", {"rating": rating}, total)
        except Exception as log_error:
            print(f"Logging error: {log_error}")

    except Exception as e:
        print(f"Unexpected error: {e}")

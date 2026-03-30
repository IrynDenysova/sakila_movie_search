from tabulate import tabulate
from pymysql.cursors import DictCursor



def paginate_query(connection, query, count_query, params, limit=10):
    """
        Executes a paginated SQL query and prints results page by page.
        :param connection: database connection
        :param query: SQL query with LIMIT and OFFSET placeholders
        :param params: tuple of query parameters
        :param limit: number of records per page
        :return: total number of fetched records
        """

    offset = 0
    page = 1

    try:
            # Получаем общее количество записей
        with connection.cursor() as cursor:
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]

        if total == 0:
            print("No films found.")
            return 0

        while offset < total:
            print(f"\n----- Found {total} film(s) -----")
            print(f"------ Page {page} ------")
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params + (limit, offset))
                rows = cursor.fetchall()

            if not rows:
                print("No more results.")
            else:
                data = []
                for i, row in enumerate(rows, start=offset + 1):
                    data.append([i,row['title'],row['release_year']])
                headers = ["Film ID","Title","Year"]
                print(tabulate(data,headers= headers ,tablefmt="outline"))

            offset += len(rows)
            page += 1

            if offset < total:
                if input("\nShow more? (y/N): ").lower() != "y":
                    break

        return total

    except Exception as e:
        print(f"Error: {e}")
        return 0
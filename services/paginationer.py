from tabulate import tabulate
from pymysql.cursors import DictCursor



def paginate_query(connection, query, count_query, params, limit=10):
    """ Executes a paginated SQL query and displays results in a table format."""

    offset = 0
    page = 1

    try:
        # Get total number of records using count query
        with connection.cursor() as cursor:
            cursor.execute(count_query, params) # Execute count query with parameters
            total = cursor.fetchone()[0] # Fetch total count

        # If no records found, exit early
        if total == 0:
            print("No films found.")
            return 0

        # Loop through results page by page
        while offset < total:
            print(f"\n----- Found {total} film(s) -----")
            print(f"------ Page {page} ------")

            # Fetch paginated data using LIMIT and OFFSET
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params + (limit, offset)) # Add pagination params
                rows = cursor.fetchall()  # Get rows as dictionaries

            # If no rows returned
            if not rows:
                print("No more results.")
            else:
                data = []
                # Format rows for table output
                for i, row in enumerate(rows, start=offset + 1):
                    data.append([i,row['title'],row['release_year']])
                headers = ["Film ID","Title","Year"]
                print(tabulate(data,headers= headers ,tablefmt="outline"))

            # Update offset and page number
            offset += len(rows)
            page += 1
            # Ask user if they want to continue to next page
            if offset < total:
                if input("\nShow more? (y/N): ").lower() != "y":
                    break

        return total # Return total number of records processed

    except Exception as e:
        print(f"Error: {e}")
        return 0
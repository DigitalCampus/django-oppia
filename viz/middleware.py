from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class SqlPrintMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        sqltime = 0.0 # Variable to store execution time
        for query in connection.queries:
            sqltime += float(query["time"])  # Add the time that the query took to the total
        # len(connection.queries) = total number of queries
        print("Page render: "+ str(sqltime)+ "sec for "+ str(len(connection.queries))+ " queries")
        return response
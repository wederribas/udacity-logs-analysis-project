#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""Udacity's Logs Analysis Project

This project was built as a requirement from the Udacity Full Stack Web
Developer Nanodegree.

It consists in a python script that runs against a PostgreSQL database to
retrieve useful information from logs in a web server.

@author Weder Ribas <wederribas@gmail.com>
"""

import psycopg2


def db_connect():
    """Creates a database connection and returns the connection along with
        the database instance.

        Returns:
            db, c - a tuple. The first element is a connection do the database
                    The second element is a curse for the database.
    """
    db = psycopg2.connect("dbname=news")
    conn = db.cursor()
    return db, conn


def exec_query(query):
    """Executes a given query in the database and returns all found rows as a
        list of tuples.

        Returns: a list of tuples containg the database output
    """
    db, conn = db_connect()
    conn.execute(query)
    results = conn.fetchall()
    db.close()
    return results


def print_top_articles():
    """Retrieve the three most accessed articles from the web server logs"""
    query = """
        WITH articles_logs AS (
            SELECT replace(path, '/article/', '') AS slug,
                   count(*) as total_accesses
            FROM log
            WHERE 1=1
            AND path LIKE '/article/%'
            GROUP BY path
        )
        SELECT articles.title, articles_logs.total_accesses
        FROM articles
        INNER JOIN articles_logs ON articles_logs.slug = articles.slug
        ORDER BY total_accesses DESC
        LIMIT 3;
    """
    print("1. What are the most popular three articles of all time?\n")
    results = exec_query(query)
    for title, accesses in results:
        print('{} -- {} views'.format(title, accesses))


def print_top_authors():
    """Print the rank of most popular authors based on the accesses to their
       articles.
    """
    query = """
        WITH articles_logs AS (
            SELECT replace(path, '/article/', '') AS slug,
                   count(*) as total_accesses
            FROM log
            WHERE 1=1
            AND path LIKE '/article/%'
            GROUP BY path
        ),
        author_views AS (
            SELECT author, sum(total_accesses) as total
            FROM articles
            INNER JOIN articles_logs ON articles_logs.slug = articles.slug
            GROUP BY author
        )
        SELECT authors.name, author_views.total
        FROM authors
        INNER JOIN author_views ON author_views.author = authors.id
        ORDER BY author_views.total DESC;
    """
    print("\n2. Who are the most popular article authors of all time?\n")
    results = exec_query(query)
    for name, total in results:
        print('{} -- {} views'.format(name, total))


def print_errors_over_one():
    """Prints out the days where more than 1% of logged access
       requests were errors.
    """
    query = """
        WITH status_logs AS (
        SELECT to_char(time, 'FMMonth DD, YYYY') AS log_date,
               count(
                    CASE
                        WHEN status LIKE '4%' OR status LIKE '5%' THEN 1
                    END) AS total_errors,
               count(*) AS total_accesses
        FROM log
        GROUP BY 1
        ),
        general_logs AS (
            SELECT log_date,
               round((total_errors * 100)::numeric
                    / total_accesses, 2) AS percent_error
            FROM status_logs
            GROUP BY log_date, total_errors, total_accesses
        )
        SELECT log_date, percent_error
        FROM general_logs
        WHERE percent_error > 1
        ORDER BY 2 DESC;
    """
    print("\n3. On which days did more than 1% of requests lead to errors?\n")
    results = exec_query(query)
    for date, percent_error in results:
        print('{} -- {}% errors'.format(date, percent_error))


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_errors_over_one()

#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""Udacity's Logs Analysis Project

This project was built as a requirement from the Udacity Full Stack Web
Developer Nanodegree.

It consists in a python script that runs against a PostgreSQL database to
retrieve useful information from logs in a web server.

@author Weder Ribas <wederribas@gmail.com>
"""

import psycopg2


def main():
	"""Run three SQL queries against the database and print out the results"""
	db = psycopg2.connect("dbname=news")
	conn = db.cursor()

	print("1. What are the most popular three articles of all time?")
	conn.execute("""
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
		ORDER BY total_accesses DESC;
	""")
	article_output = "\n%s -- %s views"
	article_output = "".join(article_output % (title, accesses) for title, accesses in conn.fetchall())
	print(article_output)

	print("\n2. Who are the most popular article authors of all time?")
	conn.execute("""
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
	""")
	authors_output = "\n%s -- %s views"
	authors_output = "".join(authors_output % (author, views)
							 for author, views in conn.fetchall())
	print(authors_output)

	print("\n3. On which days did more than 1% of requests lead to errors?")
	conn.execute("""
		WITH status_logs AS (
		SELECT to_char(time, 'FMMonth DD, YYYY') AS log_date,
			   count(
			   		CASE
			   			WHEN status LIKE '4%' OR status LIKE '5%' THEN 1
			   		END) AS total_errors,
			   count(*) AS total_accesses
		FROM log
		GROUP BY 1
		)
		SELECT log_date,
			   round((total_errors * 100)::numeric / total_accesses, 2) AS percent_error
		FROM status_logs
		GROUP BY log_date, total_errors, total_accesses
		ORDER BY 2 DESC;
	""")
	errors_output = '\n%s -- %s%% errors'
	errors_output = "".join(errors_output % (date, percentages)
							for date, percentages in conn.fetchall())
	print(errors_output)

if __name__ == '__main__':
	main()

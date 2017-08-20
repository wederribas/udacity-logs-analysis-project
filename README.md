# Udacity's Logs Analysis Project

This project was built as a requirement from the Udacity Full Stack Web
Developer Nanodegree.

It consists in a python script that runs against a PostgreSQL database to
retrieve useful information from logs in a web server.

## Requirements

In order to run the script, you'll need:

* **Python 3**;
* **PostgreSQL** (version 9.X);
* **Vagrant** (access the intallation instruction [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0));
* **psycopg2** python library (install it with `pip install psycopg2`);

## How to run?

Once you've downloaded and installed the Vagrant VM, you're ready to run the script.

1. Inside you recently created VM folder, at **vagrant** folder, download and unzip the sample data from [this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

2. In your terminal, start the VM with `vagrant up`

3. Access it with `vagrant ssh`

4. Go to the shared folder: `cd /vagrant`

5. Make sure you've cloned this repository in your local machine inside the **vagrant** folder

6. Import the sample data to the PostgreSQL database: `psql -d news -f newsdata.sql`

7. Access the folder where the **logs___reporting.py** is located and run it with **python3 logs_reporting.py**

## About the code

The script makes use of the psycopg2 library to connect to the database located at vagrant. Then each query perform a different search in the database and print out the result in the terminal from the list object.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/wederribas/udacity-logs-analysis-project/blob/master/LICENSE)

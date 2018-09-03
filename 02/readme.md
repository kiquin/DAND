# Wrangling OpenStreetMap Data
This project was written using python 3 and some functions had to be converted due to the new unicode support.
## Project Files
The main project files are the 4 following python scripts:

* sample.py - Takes the .osm map and produces a sample of it.
* data.py - The main file. Takes in the .osm and processes it using the functions in the following two files, then saves it to .csv.
* schema.py - The schema for the database.
* streets.py - Functions for auditing and updating the street names.

## Quiz files
Located in the 'py extras' folder, there are some files with methods and solutions from different quizzes from class. These aren't essential for the project.
* klist.py - Prints all the tags from the .osm.
* tags.py - Is the code for checking for unsupported characters.
* users.py - Prints all the users who contributed to the map.
* wrangling.py - Simply counts the number of tags of each kind.

## SQL queries
In the SQL queries there are some of the queries I ran for the project, saved in .sql files for running them easily.
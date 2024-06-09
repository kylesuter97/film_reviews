# film_reviews

Python file that allows user input to score a recently watched film based on certain criteria (e.g. Plot, Acting, Cinematography etc). Python functions call multiple film data APIs to populate database with a film's information (e.g. Director, Actors, Year of release etc). 

File reads in a txt file of existing film ratings, adds in the rating of the film review to be entered, and returns the ranking of that film versus the entire list fed in. Outputs two files, one txt file to be read in again next rating, and a seperate csv file intended for use to see the entire database of ratings. 

Seperate files are used as character formatting conversions when opening a csv file in excel resulted in increasing addition of non alphanumeric characters in data records.

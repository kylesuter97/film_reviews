
import requests
import pandas as pd
import time

input_df = pd.read_csv("input_txt.csv")

weightings = {"Plot": 4, "Screenplay": 3, "Direction": 2,
               "Characters": 2, "Dialogue": 3, "Pacing": 2,
                 "Acting": 4, "Cinematography": 3, "VFX": 4,
                   "Humour": 3, "Emotion": 2, "Ending": 3,
                     "Atmosphere": 2, "Score": 1, "Enjoyment": 4}

temp_dict = {}

def enter_rating(key):
    global temp_dict
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'n/a':
                temp_dict[key] = input(f"Enter {key} rating: ")
            elif my_error == 'value':
                temp_dict[key] = input(f"NOT A NUMBER! Enter {key} rating again: ")
            elif my_error == 'assertion':
                if key not in ['VFX', 'Humour', 'Emotion']:
                    temp_dict[key] = input(f"NOT BETWEEN 1 & 10! Enter {key} rating again: ")
                elif key in ['VFX', 'Humour', 'Emotion']:
                    temp_dict[key] = input(f"NOT BETWEEN 0 & 10! Enter {key} rating again: ")
           
            # check if value entered is a number
            temp_dict[key] = int(temp_dict[key])
            # check if value entered is in correct range
            if key not in ['VFX', 'Humour', 'Emotion']:
                assert 0 < int(temp_dict[key]) <= 10
            elif key in ['VFX', 'Humour', 'Emotion']:
                assert 0 <= int(temp_dict[key]) <= 10

        except ValueError:
            my_error = 'value'
            continue
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break

def change_scores(): 
    print("")
    change_rating = input("Please enter the category you would like to change: ")
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'assertion':
                change_rating = input("NOT A CATEGORY! Please enter the category you would like to change: ")
            assert change_rating in weightings.keys()
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break
    
    print("")
    new_rating = 0
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'n/a':
                new_rating = input(f"Enter {change_rating} rating: ")
            elif my_error == 'value':
                new_rating = input(f"NOT A NUMBER! Enter {change_rating} rating again: ")
            elif my_error == 'assertion':
                if change_rating not in ['VFX', 'Humour', 'Emotion']:
                    new_rating = input(f"NOT BETWEEN 1 & 10! Enter {change_rating} rating again: ")
                elif change_rating in ['VFX', 'Humour', 'Emotion']:
                    new_rating = input(f"NOT BETWEEN 0 & 10! Enter {change_rating} rating again: ")
           
            # check if value entered is a number
            new_rating = int(new_rating)
            # check if value entered is in correct range
            if change_rating not in ['VFX', 'Humour', 'Emotion']:
                assert 0 < int(new_rating) <= 10
            elif change_rating in ['VFX', 'Humour', 'Emotion']:
                assert 0 <= int(new_rating) <= 10

        except ValueError:
            my_error = 'value'
            continue
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break
    
    global temp_dict
    temp_dict[change_rating] = new_rating

    not_happy = input("Would you like to change any other categories? Please enter 'y' or 'n': ")
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'assertion':
                not_happy = input("NOT A VALID INPUT! Please enter 'y' or 'n': ")
            assert not_happy in ('y', 'n')
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break
    if not_happy == 'y':
        change_scores()


# initial function to return film's IMDb ID from MoviesDatabase API
def get_film_id(Title):
    
    url = f"https://moviesdatabase.p.rapidapi.com/titles/search/title/{Title}"

    querystring = {"exact":"true","titleType":"movie"}

    headers = {
	    "X-RapidAPI-Key": "0a07715ad8msheb9f739428eee24p1d7c30jsn6453488ff49f",
	    "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    result = response.json()
    output = result['results'][0]['id']
    
    return output


def get_film_data(Title='_default_kyle_title', id='_default_kyle_id'):

    if id != '_default_kyle_id':
        film_id = id
    else:
        try:
            film_id = get_film_id(Title)
            time.sleep(1)
            print("\nReturning Film data...\n")
            time.sleep(1)            
        except:
            try:
                time.sleep(1)
                print("\nReturning Film data...\n")
                time.sleep(1)
                film_id = get_film_id(input("TITLE NOT RECOGNISED! Please enter film Title again: "))
                time.sleep(1)
                print("\nReturning Film data...\n")
                time.sleep(1)
            except:
                time.sleep(1)
                print("\nReturning Film data...\n")
                time.sleep(1)
                film_id = input("THAT TITLE WAS ALSO NOT RECOGNISED! Please enter ID from IMDb: ")
                time.sleep(1)
                print("\nReturning Film data...\n")
                time.sleep(1)
    
    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {"r":"json","i":{film_id}}

    headers = {
		"X-RapidAPI-Key": "0a07715ad8msheb9f739428eee24p1d7c30jsn6453488ff49f",
		"X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
	}

    response = requests.get(url, headers=headers, params=querystring)
    result_data = response.json()
    return result_data


# function to process user inputs of film ratings, and output final ratings df as csv file
def add_new_film(Title='_default_kyle_title', id='_default_kyle_id'):
    film_data = get_film_data(Title, id)

    global temp_dict     
    temp_dict['Title'] = film_data['Title']
    temp_dict['Year of Release'] = film_data['Year']
    temp_dict['Director'] = film_data['Director']
    temp_dict['Actors'] = film_data['Actors']
    temp_dict['Genre'] = film_data['Genre']


    print(f"Title: {temp_dict['Title']}")
    print(f"Year of Release: {temp_dict['Year of Release']}")
    print(f"Director: {temp_dict['Director']}")
    print(f"Actors: {temp_dict['Actors']}")
    print(f"Genre(s): {temp_dict['Genre']}\n")

    film_happy = input("Is the Film correct? Enter 'y' or 'n': ")
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'assertion':
                film_happy = input("NOT A VALID INPUT! Please enter 'y' or 'n': ")
            assert film_happy in ('y', 'n')
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break
    if film_happy == 'n':
        film_data_update = get_film_data(id=input("Please enter ID from IMDB: "))
        print("\nUpdating Film data...")
        temp_dict['Title'] = film_data_update['Title']
        temp_dict['Year of Release'] = film_data_update['Year']
        temp_dict['Director'] = film_data_update['Director']
        temp_dict['Actors'] = film_data_update['Actors']
        temp_dict['Genre'] = film_data_update['Genre']
        time.sleep(1)
        print("\n...")
        time.sleep(1)
        print(f"\nTitle: {temp_dict['Title']}")
        print(f"Year of Release: {temp_dict['Year of Release']}")
        print(f"Director: {temp_dict['Director']}")
        print(f"Actors: {temp_dict['Actors']}")
        print(f"Genre(s): {temp_dict['Genre']}\n")


    print("")
    temp_dict['Sub-Genre'] = input("Enter any Sub-Genres: ")
    print("")


    title_happy = input("Are you happy with the Title? Enter 'y' or 'n': ")
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'assertion':
                title_happy = input("NOT A VALID INPUT! Please enter 'y' or 'n': ")
            assert title_happy in ('y', 'n')
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break
    if title_happy == 'n':
        temp_dict['Title'] = input("Please enter your preferred Title: ")
    print("")

 
    for key in weightings.keys():
        enter_rating(key)
    
    print("")
    ratings_happy = input("Are you happy with your Ratings? Enter 'y' or 'n': ")
    my_error = 'n/a'
    while True:
        try:
            if my_error == 'assertion':
                ratings_happy = input("NOT A VALID INPUT! Please enter 'y' or 'n': ")
            assert ratings_happy in ('y', 'n')
        except AssertionError:
            my_error = 'assertion'
            continue
        else:
            break
    if ratings_happy == 'n':
        change_scores()


    overall_rating = 0
    denominator = 0
    for key, value in temp_dict.items():
        if (key in weightings.keys()) and (int(value) > 0):
            overall_rating += (int(weightings[key]) * int(value))
            denominator += int(weightings[key])


    final_dict = temp_dict
    final_dict['Overall Rating'] = round(overall_rating / denominator, 4)
    
    if final_dict['VFX'] == 0:
        final_dict['VFX'] = ''
    if final_dict['Humour'] == 0:
        final_dict['Humour'] = ''
    if final_dict['Emotion'] == 0:
        final_dict['Emotion'] = ''


    print("\nCalculating...")
    time.sleep(1)

    row_df = pd.DataFrame(final_dict, index=[0])

    output_df = pd.concat([input_df, row_df], ignore_index=True)
    output_df = output_df.sort_values('Overall Rating', ascending=False).reset_index(drop=True)
    
    mask = (output_df['Title']==final_dict['Title'])&(output_df['Overall Rating']==final_dict['Overall Rating'])  # create a mask of multiple statements (& = and)
    
    rank = int(output_df[mask].index.to_list()[0]) + 1
    count_films = len(output_df)

    print(f"\nTitle: {final_dict['Title']}")
    time.sleep(1)
    print(f"Overall Rating: {final_dict['Overall Rating']}")
    time.sleep(1)
    print(f"Rank: {rank} / {count_films}\n")
    time.sleep(1)
    print("Generating file...\n")

    output_df.to_csv("input_txt.csv", index=False)
    output_df.to_csv("film_ratings_view.csv", index=False, encoding='mbcs')
    time.sleep(1)
    print("File 'film_ratings_view.csv' generated!")


add_new_film(Title=input("\nEnter film Title: "))
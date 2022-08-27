import json
import sqlite3


def connect_database(query):

    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()
        return result


def search_title(title):
    query = f"select title, country, release_year, listed_in, description \
    from netflix \
    where title = '{title}' \
    order by release_year desc \
    limit 1"
    result = connect_database(query)
    dict_data = {}
    for key in result:
        dict_data = {"Название": key[0],
                    "Страна": key[1],
                    "Год выпуска": key[2],
                    "Жанр": key[3],
                    "Краткое описание": key[4]
                    }
    return dict_data

def search_by_years(years_1, years_2):
    query = f"select title, release_year \
    from netflix \
    where release_year between {years_1} and {years_2} \
    order by release_year desc \
    limit 100"

    result = connect_database(query)
    list_data = []
    for key in result:
        key_dict = {
            "title": key[0],
            "release_year": key[1]
        }
        list_data.append(key_dict)

    return list_data


def search_movie_rating(rating):
    my_dict ={
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    query = f"""SELECT distinct title, rating, release_year \
             FROM netflix \
             where rating in {my_dict.get(rating, ("R", "R"))}""" \

    result = connect_database(query)
    list_data = []
    for key in result:
        key_dict = {
            "title": key[0],
            "rating": key[1],
            "description": key[2]
        }
        list_data.append(key_dict)

    return list_data

def search_genre(genre):
    query = f"select title, description \
    from netflix \
    where listed_in like '%{genre}%'\
    order by release_year desc \
    limit 10"

    result = connect_database(query)
    list_data = []
    for key in result:
        key_dict = {
            "title": key[0],
            "description": key[1]
        }
        list_data.append(key_dict)

    return list_data

def search_by_actors(actor_1, actor_2):
    query = f"""select "cast"\
    from netflix
    where "cast" like '%{actor_1}%' and "cast" like '%{actor_2}%'"""
    result = connect_database(query)

    names_dict = {}
    for item in result:
        names = set(dict(item).get('cast').split(",")) - set([actor_1, actor_2])

        for name in names:
            names_dict[str(name).strip()] = names_dict.get(str(name).strip(), 0) + 1

    result_list = []
    for key, value in names_dict.items():
        if value >= 2:
            result_list.append(key)

    return result_list

print(search_by_actors('Rose McIver', 'Ben Lamb'))


def search_by_type_movie(type_movie, release_year, genre):
    query = f"""select title, description, listed_in \
    from netflix \
    where "type" = '{type_movie}' \
    and release_year = '{release_year}' \
    and listed_in like '%{genre}%'"""

    result = connect_database(query)

    list_movie = []
    for key in result:
        list_movie.append(dict(key))

    return json.dumps(list_movie)


print(search_by_type_movie('TV Show', '2020', 'Dramas'))








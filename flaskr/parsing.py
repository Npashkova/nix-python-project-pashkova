def films_parsing(data):
    title = data.get('title')
    release_date = data.get('release_date')
    rating = data.get('rating')
    poster = data.get('poster')
    description = data.get('description')
    user_input = {"title": title, "release_date": release_date, "rating": rating, "poster": poster,
                  "description": description}
    return user_input

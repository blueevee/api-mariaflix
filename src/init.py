from models import user, gender, films ,series, seasons , episodes, user_episode, user_film


user.createTable()
user.populateTable()
user.restartSequence()

gender.createTable()
gender.populateTable()
gender.restartSequence()

films.createTable()
films.populateTable()
films.restartSequence()

series.createTable()
series.populateTable()
series.restartSequence()

seasons.createTable()
seasons.populateTable()
seasons.restartSequence()

episodes.createTable()
episodes.populateTable()
episodes.restartSequence()

user_episode.createTable()
user_episode.populateTable()

user_film.createTable()
user_film.populateTable()

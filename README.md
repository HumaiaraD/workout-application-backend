# Workout API Backend Application

# Project Description
This app lets users create workouts and exercises, link exercises to workouts, and record sets, reps, or duration. It uses Flask, SQLAlchemy, Marshmallow, Flask-Migrate, and SQLite.
# Installation
From the folder containing app.py, install dependencies, apply the database migrations, and add sample data:
pipenv install
pipenv run flask --app app db upgrade
pipenv run python seed.py

If your project has no migrations folder yet, run pipenv run flask --app app db init and pipenv run flask --app app db migrate -m "Create workout tables" before db upgrade.
# Run
Start the server on port 5555:
pipenv run flask --app app run --port 5555

The API runs at http://127.0.0.1:5555. You can also use pipenv run python app.py. Rerun pipenv run python seed.py to reset the sample data.
# Endpoints
Method	Path	Description
GET	/workouts	List workouts
GET	/workouts/<id>	Show one workout and its associated exercises
POST	/workouts	Create a workout
DELETE	/workouts/<id>	Delete a workout and its join records
GET	/exercises	List exercises
GET	/exercises/<id>	Show one exercise and its associated workouts
POST	/exercises	Create an exercise
DELETE	/exercises/<id>	Delete an exercise and its join records
POST	/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises	Add an existing exercise to a workout


Example request body for the last endpoint:
{"sets": 3, "reps": 12}

For a timed exercise, send {"sets": 2, "duration_seconds": 30} instead. The URL IDs must refer to an existing workout and exercise.
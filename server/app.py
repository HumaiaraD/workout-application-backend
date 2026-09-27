from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route("/", methods=["GET"])
def index():
    return "<h1>Welcome to my workout app.</h1>"


@app.route("/workouts", methods=["GET"])
def get_all_workouts():
    workouts = Workout.query.all()
    body = WorkoutSchema(many=True).dump(workouts)
       
    return make_response(body, 200)

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()
    if workout is None:
            return make_response({"error": "Workout not found."}, 404)
        
    body = WorkoutSchema().dump(workout)
    return make_response(body, 200)



@app.route("/workouts", methods=["POST"])
def create_workout():
    data = WorkoutSchema().load(request.get_json())

    w = Workout(**data)
    db.session.add(w)
    db.session.commit()

    return make_response(WorkoutSchema().dump(w), 201)



@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    w = Workout.query.filter(Workout.id == id).first()

    if w is None:
        return make_response({"error": "Workout doesn't exist"}, 404)

    db.session.delete(w)
    db.session.commit()
    return "", 204



@app.route("/exercises", methods=["GET"])
def get_all_exercises():
    exercises = Exercise.query.all()
    
    body = ExerciseSchema(many=True).dump(exercises)
    return make_response(body, 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    if exercise is None:
        return make_response({"error": "Exercise not found."}, 404)
            
    body = ExerciseSchema().dump(exercise)
    return make_response(body, 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = ExerciseSchema().load(request.get_json())

    e = Exercise(**data)
    db.session.add(e)
    db.session.commit()

    return make_response(ExerciseSchema().dump(e), 201)

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    e = Exercise.query.filter(Exercise.id == id).first()

    if e is None:
        return make_response({"error": "Exercise doesn't exist"}, 404)

    db.session.delete(e)
    db.session.commit()
    return "", 204

@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_workout_exercise(exercise_id, workout_id):
    e = Exercise.query.filter(Exercise.id == exercise_id).first()
    w = Workout.query.filter(Workout.id == workout_id).first()

    if e is None or w is None:
        return make_response({"error": "None of the exercise or workout exists."}, 404)

    data = WorkoutExercisesSchema().load(request.get_json())
    add_on = WorkoutExercises(
        workout=w,
        exercise=e,
        sets = data["sets"],
        reps = data.get("reps"),
        duration_seconds = data.get("duration_seconds"),
    )
    db.session.add(add_on)
    db.session.commit()

    return make_response(WorkoutExercisesSchema().dump(add_on), 201)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
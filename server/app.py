from flask import Flask, make_response, request
from flask_migrate import Migrate

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
    body = []
    for w in workouts:
        body.append({
            "id": w.id,
            "date": w.date.isoformat(),
            "duration_minutes": w.duration_minutes,
            "notes": w.notes
        })
    return make_response(body, 200)

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()
    if workout:
        body = {
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes,
            "exercises": [{
                "id": workout_exercise.exercise.id,
                "name": workout_exercise.exercise.name,
                "category": workout_exercise.exercise.category,
                "sets": workout_exercise.sets,
                "reps": workout_exercise.reps,
                "duration_seconds": workout_exercise.duration_seconds,
            } for workout_exercise in workout.workout_exercises]
        }

        return make_response(body, 200)
    else:
        return make_response({"error": "Workout not found."}, 404)

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    w = Workout(
        date=date.fromisoformat(data["date"]),
        duration_minutes=data["duration_minutes"],
        notes=data["notes"]
    )

    db.session.add(w)
    db.session.commit()

    return make_response({
        "id": w.id,
        "date": w.date.isoformat(),
        "duration_minutes": w.duration_minutes,
        "notes": w.notes,
    }, 201)

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
    exercise = Exercise.query.all()
    body = []
    for e in exercise:
        body.append({
            "id": e.id,
            "name": e.name,
            "category": e.category,
            "equipment_needed": e.equipment_needed,
        })
    return make_response(body, 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    if exercise:
        body = {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed,
            "workouts": [{
                "id": workout_exercise.workout.id,
                "date": workout_exercise.workout.date.isoformat(),
                "duration_minutes": workout_exercise.workout.duration_minutes,
                "sets": workout_exercise.sets,
                "reps": workout_exercise.reps,
                "duration_seconds": workout_exercise.duration_seconds,
            } for workout_exercise in exercise.workout_exercises]
        }

        return make_response(body, 200)
    else:
        return make_response({"error": "Exercise not found."}, 404)

@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    e = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data["equipment_needed"]      
    )
    db.session.add(e)
    db.session.commit()
    
    return make_response({
        "id": e.id,
        "name": e.name,
        "category": e.category,
        "equipment_needed": e.equipment_needed,
    }, 201)

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

    data = request.get_json()
    add_on = WorkoutExercises(
        workout=w,
        exercise=e,
        sets = data["sets"],
        reps = data.get("reps"),
        duration_seconds = data.get("duration_seconds"),
    )
    db.session.add(add_on)
    db.session.commit()

    return make_response({
        "id": add_on.id,
        "workout_id": add_on.workout_id,
        "exercise_id": add_on.exercise_id,
        "sets": add_on.sets,
        "reps": add_on.reps,
        "duration_seconds": add_on.duration_seconds,
    }, 201)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
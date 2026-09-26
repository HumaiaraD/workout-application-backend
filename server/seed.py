#!/usr/bin/env python3

from datetime import date, timedelta

from app import app
from models import db, Exercise, Workout, WorkoutExercises


def seed():
    with app.app_context():
        # reset data and add new example data, committing to db
        WorkoutExercises.query.delete()
        Exercise.query.delete()
        Workout.query.delete()

		# adding some data to database
        
        squat = Exercise(
            name="Squat",
            category="Strength",
            equipment_needed=False,
        )
        plank = Exercise(
            name="Plank",
            category="Core",
            equipment_needed=False,
        )
        dumbbell_press = Exercise(
            name="Dumbbell Press",
            category="Strength",
            equipment_needed=True,
        )

        strength_day = Workout(
            date=date.today() - timedelta(days=2),
            duration_minutes=45,
            notes="Strength session with squats and dumbbell presses.",
        )
        core_day = Workout(
            date=date.today() - timedelta(days=1),
            duration_minutes=20,
            notes="Core session with a timed plank.",
        )

        db.session.add_all([
            squat, plank, dumbbell_press,
            strength_day, core_day,
        ])
        db.session.flush()

        db.session.add_all([
            WorkoutExercises(
                workout=strength_day,
                exercise=squat,
                sets=3,
                reps=12,
            ),
            WorkoutExercises(
                workout=strength_day,
                exercise=dumbbell_press,
                sets=3,
                reps=10,
            ),
            WorkoutExercises(
                workout=core_day,
                exercise=plank,
                sets=2,
                duration_seconds=30,
            ),
        ])

        db.session.commit()
        print("Seeded 3 exercises, 2 workouts, and 3 workout exercise records.")


if __name__ == "__main__":
    seed()
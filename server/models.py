from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import date
from marshmallow import Schema, fields, validate

# Define Models here

class Exercise(db.Model):
    __tablename__ = "exercise"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship("WorkoutExercises", back_populates="exercise", cascade="all, delete-orphan")
    workouts = association_proxy("workout_exercises", "workout")

    @validates("name")
    def validate_name(self, key, value):
        if value is None or not value.strip():
            raise ValueError("Name is required!")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value is None or not value.strip():
            raise ValueError("Category is required")
        return value

    @validates("equipment_needed")
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("Equipment needed must be True or False.")
        return value

    def __repr__(self):
        return f"<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}>"

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True,)
    category = fields.String(required=True,)
    equipment_needed = fields.Bool(required=True,)

    workout_exercises = fields.Nested(lambda: WorkoutExercisesSchema(exclude=("exercise",)), many=True,)

    
class Workout(db.Model):
    __tablename__ = "workout"

    __table_args__ = (db.CheckConstraint("duration_minutes > 0"),)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercises", back_populates="workout", cascade="all, delete-orphan")
    exercises = association_proxy("workout_exercises", "exercise")

    @validates("date")
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError("Workout date is required.")
        if value > date.today():
            raise ValueError("Workout date cannot be in the future")
        return value

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Duration must be greater than 0.")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is None or not value.strip() or len(value) > 250:
            raise ValueError("Notes must be within 250 letters and not empty")
        return value

    def __repr__(self):
        return f"<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}>"

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True,)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.String(required=True,)

    workout_exercises = fields.Nested(lambda: WorkoutExercisesSchema(exclude=("workout",)), many=True,)


class WorkoutExercises(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (db.CheckConstraint("duration_seconds > 0"),)

    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout_id = db.Column(db.Integer, db.ForeignKey("workout.id"))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"))

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and (type(value) is not int or value <= 0):
            raise ValueError("Reps must be a positive whole number when provided.")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if type(value) is not int or value <= 0:
            raise ValueError("Sets must be a positive whole number")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and (type(value) is not int or value <= 0):
            raise ValueError("Duration must be a positive whole number when provided.")
        return value

    def __repr__(self):
        return f"<Workout Exercises {self.id}, {self.reps}, {self.sets}, {self.duration_seconds}>"


class WorkoutExercisesSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, required=True,)

    workout = fields.Nested(lambda: WorkoutSchema(exclude=("workout_exercises",)))
    exercise = fields.Nested(lambda: ExerciseSchema(exclude=("workout_exercises",)))

from mongoengine import Document, StringField, ListField, ReferenceField, IntField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  #TODO: Hash passwords
    workout_list = ListField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # After initialization, set `self.id` to the MongoDB `_id`
        if not hasattr(self, 'id'):
            self.id = None  # Initialize to None until saved

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving, assign MongoDB `_id` to `self.id`
        self.id = self.pk


    def update_password(self, password):
        self.password = password #TODO: Hash passwords

    def add_workout(self, workout):
        from .workout import Workout
        self.workout_list.append(workout)

    def __repr__(self):
        return f"User(username={self.username}, workout_list={self.workout_list})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def to_dict(self):
        return {
            "exercise_name": self.exercise_name,
            "reps": self.reps,
            "loading": self.loading,
            "rest": self.rest,
            "performance_notes": self.performance_notes,
        }